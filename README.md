# Omniver Quantum Decoder

**Anna-native quantum security App & Web Application for NIST FIPS 203/204 Post-Quantum Cryptography, Shor-style order finding, and quantum risk analysis.**

[![CI](https://github.com/elon00/omniver-quantum-decoder/actions/workflows/ci.yml/badge.svg)](https://github.com/elon00/omniver-quantum-decoder/actions/workflows/ci.yml)
[![Pages Deployment](https://github.com/elon00/omniver-quantum-decoder/actions/workflows/pages.yml/badge.svg)](https://elon00.github.io/omniver-quantum-decoder/)
[![NIST FIPS 203/204 Conformance](https://img.shields.io/badge/NIST%20PQC-ML--KEM--768%20%7C%20ML--DSA--65-blue)](docs/HARDCORE_PQC_SPEC.md)
[![Reality Score](https://img.shields.io/badge/Universal%20Reality%20Gates-10%2F10%20PASS-brightgreen)](REALITY_MANIFEST.json)

🌐 **Live Web Application**: [https://elon00.github.io/omniver-quantum-decoder/](https://elon00.github.io/omniver-quantum-decoder/)  
📦 **Repository**: [https://github.com/elon00/omniver-quantum-decoder](https://github.com/elon00/omniver-quantum-decoder)

---

## ⚡ Hardcore NIST Post-Quantum Cryptography (PQC)

This platform integrates production-grade, zero-mock Post-Quantum Cryptographic primitives conforming to NIST standards:

- **NIST FIPS 203 (ML-KEM-768)**: Kyber-based post-quantum key encapsulation mechanism. Includes wire invariants (1,184B public key, 2,400B private key, 1,088B ciphertext) and **§7.3 Implicit Rejection** for invalid/corrupted ciphertexts.
- **NIST FIPS 204 (ML-DSA-65)**: Dilithium-based digital signature algorithm (1,952B public key, 4,032B secret key, 3,309B digital signatures) with **Wycheproof bit-flip negative testing**.
- **x402 Dual-Hybrid Conjunction**: Post-quantum service settlement protocol requiring valid classical ECDSA/Ed25519 authorization combined conjunctively with ML-DSA-65 signatures.
- **Universal Reality System (URS v1.0)**: 10 automated verification gates ensuring 0 simulation mocks in cryptographic paths, strict fail-closed safety, and reproducible KAT vectors.

### Test & Audit Commands

```bash
# Run 8-tier NIST FIPS 203 & 204 test suite
npm run test:nist

# Run 23 standalone cryptographic assertions (RFC 5869, Wycheproof)
npm run audit:crypto

# Run Universal Reality 10-Gate Verification
npm run reality:universal
```

---

## Anna architecture

```text
Anna App UI (bundle/)
        ↓
Anna Runtime
        ↓
Bundled Executa: omniver-quantum-decoder
        ↓
Shor-style order finding OR reverse sampling
        ↓
Anna Host LLM
```

The App uses a bundled Python Executa and the current Anna v2 JSON-RPC/reverse-sampling model. No Gemini/OpenAI API key is required for the Anna copilot.

## Features

- Small-integer Shor-style order-finding simulator.
- Non-trivial factor derivation for supported composite integers.
- Anna-host quantum copilot through `sampling/createMessage`.
- Native Anna Runtime UI using `anna.tools.invoke`.
- Bundled Executa handle so the production `tool_id` is resolved by Anna instead of hardcoded in the manifest.
- Security-conscious messaging that distinguishes simulation from real quantum attacks.

## Local development

Requirements: Node.js 22+, `uv`, and the Anna CLI (`@anna-ai/cli`).

```bash
anna-app doctor
anna-app validate --strict
anna-app dev
```

Inside Anna, test:

1. `N = 15` → Decode N → verify non-trivial factors.
2. Ask the Quantum Copilot a question.
3. Confirm the Executa is running and that reverse sampling is enabled for the user.

## Publishing

The hackathon requires the final App to be published on Anna. The recommended flow is:

```bash
anna-app apps publish
anna-app apps submit-review omniver-quantum-decoder
```

After publishing, submit the **published Anna App URL** to DoraHacks. Do not use the GitHub URL or a standalone Netlify URL as the final App URL.

### Important production note

The current repository config uses the `local` Executa distribution profile for deterministic development. Before a public Marketplace release, switch the Executa to a supported production distribution (for example a multi-platform binary release or an approved package distribution) and verify the Linux/Cloud Agent path. Do not claim Marketplace/cloud readiness until that artifact is actually built and installed successfully.

## Existing web application

The original React/Vite application remains in `src/` for the standalone version. The Anna submission surface is deliberately isolated under `bundle/`, with the Anna-specific backend under `executas/omniver-quantum-decoder/`.

## Disclaimer

The simulator demonstrates quantum-algorithm concepts on small integers. It does **not** demonstrate recovery of a real Bitcoin, Solana, or other production private key. Real cryptographic compromise requires authorized data, appropriate quantum resources, and independent verification.
