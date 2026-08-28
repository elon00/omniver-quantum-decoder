# Omniver Quantum Decoder

**Anna-native quantum security App for Shor-style order finding, factorization risk analysis, and an Anna-hosted quantum copilot.**

> **Hackathon requirement:** the final submission is the published **Anna App**, not this GitHub repository or the standalone web app. This repository is the source/build project for the Anna App.

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
