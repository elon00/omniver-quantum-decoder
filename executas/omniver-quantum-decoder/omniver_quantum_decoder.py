#!/usr/bin/env python3
"""Omniver Quantum Decoder — Anna Executa.

Provides deterministic Shor-style order finding for small composite integers and
an Anna-host LLM copilot through reverse sampling. No provider API key is kept
in the project.
"""
from __future__ import annotations

import asyncio
import json
import math
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from executa_sdk import PROTOCOL_VERSION_V2, SamplingClient, SamplingError

MANIFEST = {
    "display_name": "Omniver Quantum Decoder",
    "version": "2.5.0",
    "description": "Shor-style order finding, factorization risk analysis, and Anna-host quantum copilot.",
    "author": "Omniver Quantum Decoder",
    "host_capabilities": ["llm.sample"],
    "tools": [
        {
            "name": "shor_factor",
            "description": "Run a deterministic small-integer Shor-style order-finding simulation and return non-trivial factors.",
            "parameters": [
                {"name": "n", "type": "integer", "description": "Composite integer to factor; recommended 4..9999", "required": True},
                {"name": "a", "type": "integer", "description": "Optional coprime base. If omitted, a suitable base is selected.", "required": False},
            ],
        },
        {
            "name": "quantum_copilot",
            "description": "Ask Anna's host LLM for a concise quantum-cryptography explanation grounded in the decoder context.",
            "parameters": [
                {"name": "prompt", "type": "string", "description": "Question or analysis request", "required": True},
                {"name": "max_tokens", "type": "integer", "description": "Maximum response tokens, 64..1024", "required": False, "default": 512},
            ],
        },
    ],
    "runtime": {"type": "uv", "min_version": "0.1.0"},
}

_stdout_lock = threading.Lock()

def write_frame(message: dict) -> None:
    with _stdout_lock:
        sys.stdout.write(json.dumps(message, ensure_ascii=False, separators=(",", ":")) + "\n")
        sys.stdout.flush()

sampling = SamplingClient(write_frame=write_frame)


def gcd(a: int, b: int) -> int:
    return math.gcd(a, b)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    p = 3
    while p * p <= n:
        if n % p == 0:
            return False
        p += 2
    return True


def order_mod(a: int, n: int, limit: int = 20000) -> int | None:
    if gcd(a, n) != 1:
        return None
    value = 1
    for r in range(1, min(limit, n * n) + 1):
        value = (value * a) % n
        if value == 1:
            return r
    return None


def factor_with_order(n: int, requested_a: int | None = None) -> dict:
    if n < 4 or n > 9999:
        raise ValueError("n must be between 4 and 9999 for the built-in simulator")
    if is_prime(n):
        return {"n": n, "prime": True, "factors": [n], "status": "prime"}
    if n % 2 == 0:
        return {"n": n, "prime": False, "factors": [2, n // 2], "status": "factored", "method": "trivial-even"}

    candidates = [requested_a] if requested_a else list(range(2, min(n, 32)))
    attempts = []
    for a in candidates:
        if a is None or a <= 1 or a >= n:
            continue
        g = gcd(a, n)
        if g != 1:
            return {"n": n, "prime": False, "factors": sorted([g, n // g]), "status": "factored", "method": "gcd shortcut", "a": a}
        r = order_mod(a, n)
        attempts.append({"a": a, "order": r})
        if r is None or r % 2 != 0:
            continue
        x = pow(a, r // 2, n)
        if x in (1, n - 1):
            continue
        p = gcd(x - 1, n)
        q = gcd(x + 1, n)
        if 1 < p < n and 1 < q < n:
            return {
                "n": n,
                "prime": False,
                "factors": sorted([p, q]),
                "status": "factored",
                "method": "Shor-style order finding",
                "base": a,
                "order": r,
                "modular_power": x,
                "attempts": attempts,
            }
    return {"n": n, "prime": False, "status": "retry", "factors": [], "attempts": attempts,
            "message": "No useful even order was found; choose another coprime base a."}


async def copilot(prompt: str, max_tokens: int, invoke_id: str) -> dict:
    max_tokens = max(64, min(1024, int(max_tokens)))
    result = await sampling.create_message(
        messages=[{"role": "user", "content": {"type": "text", "text": (
            "You are Omniver Quantum Decoder Copilot. Explain quantum computing, "
            "Shor's algorithm, post-quantum cryptography, ECDSA/secp256k1 risk, and "
            "quantum-safe migration accurately. Never claim that a classical simulator "
            "has broken a real Bitcoin/Solana key. Distinguish simulation from real quantum hardware.\n\n"
            + prompt
        )}}],
        max_tokens=max_tokens,
        system_prompt="Be technically precise, concise, and security-conscious.",
        metadata={"executa_invoke_id": invoke_id, "tool": "quantum_copilot"},
        timeout=60.0,
    )
    content = result.get("content") or {}
    text = content.get("text", "") if isinstance(content, dict) else ""
    return {"text": text, "model": result.get("model"), "usage": result.get("usage"), "stopReason": result.get("stopReason")}


def response(req_id, result=None, error=None):
    out = {"jsonrpc": "2.0", "id": req_id}
    if error is not None:
        out["error"] = error
    else:
        out["result"] = result
    return out


def initialize(req_id, params):
    offered = (params or {}).get("protocolVersion") or PROTOCOL_VERSION_V2
    proto = PROTOCOL_VERSION_V2 if offered == PROTOCOL_VERSION_V2 else offered
    return response(req_id, {
        "protocolVersion": proto,
        "serverInfo": {"name": MANIFEST["display_name"], "version": MANIFEST["version"]},
        "client_capabilities": {"sampling": {}} if proto == PROTOCOL_VERSION_V2 else {},
        "capabilities": {},
    })


def invoke(req_id, params):
    tool = params.get("tool")
    args = params.get("arguments") or {}
    invoke_id = params.get("invoke_id") or ""
    try:
        if tool == "shor_factor":
            data = factor_with_order(int(args.get("n")), args.get("a"))
        elif tool == "quantum_copilot":
            fut = asyncio.run_coroutine_threadsafe(
                copilot(str(args.get("prompt", "")), int(args.get("max_tokens", 512)), invoke_id), loop
            )
            data = fut.result(timeout=120)
        else:
            return response(req_id, error={"code": -32601, "message": f"Unknown tool: {tool}"})
        return response(req_id, {"success": True, "tool": tool, "data": data})
    except SamplingError as exc:
        return response(req_id, error={"code": exc.code, "message": exc.message, "data": exc.data})
    except (ValueError, TypeError) as exc:
        return response(req_id, error={"code": -32602, "message": str(exc)})
    except Exception as exc:  # keep the long-lived process alive
        print(f"invoke error: {exc}", file=sys.stderr)
        return response(req_id, error={"code": -32603, "message": "Internal Executa error"})


loop = asyncio.new_event_loop()
threading.Thread(target=loop.run_forever, daemon=True).start()
pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="omniver-invoke")


def dispatch_message(raw: str):
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError:
        write_frame(response(None, error={"code": -32700, "message": "Parse error"}))
        return
    if "method" not in msg:
        if not sampling.dispatch_response(msg):
            print(f"unmatched reverse-RPC response id={msg.get('id')!r}", file=sys.stderr)
        return
    method = msg.get("method")
    req_id = msg.get("id")
    params = msg.get("params") or {}
    if method == "initialize":
        out = initialize(req_id, params)
    elif method == "describe":
        out = response(req_id, MANIFEST)
    elif method == "health":
        out = response(req_id, {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat(), "version": MANIFEST["version"], "tools_count": 2})
    elif method == "invoke":
        out = invoke(req_id, params)
    elif method == "shutdown":
        out = response(req_id, {"ok": True})
    else:
        out = response(req_id, error={"code": -32601, "message": f"Method not found: {method}"})
    if req_id is not None:
        write_frame(out)


def main():
    print("Omniver Quantum Decoder Executa ready", file=sys.stderr)
    try:
        for raw in sys.stdin:
            line = raw.strip()
            if line:
                pool.submit(dispatch_message, line)
    finally:
        pool.shutdown(wait=False, cancel_futures=True)
        loop.call_soon_threadsafe(loop.stop)


if __name__ == "__main__":
    main()
