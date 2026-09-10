# Omniver Quantum Decoder

**Anna-native quantum security App & Web Application for NIST FIPS 203/204 Post-Quantum Cryptography, Shor-style order finding, and quantum risk analysis.**

[![CI](https://github.com/elon00/omniver-quantum-decoder/actions/workflows/ci.yml/badge.svg)](https://github.com/elon00/omniver-quantum-decoder/actions/workflows/ci.yml)
[![Pages Deployment](https://github.com/elon00/omniver-quantum-decoder/actions/workflows/pages.yml/badge.svg)](https://elon00.github.io/omniver-quantum-decoder/)
[![NIST FIPS 203/204 Conformance](https://img.shields.io/badge/NIST%20PQC-ML--KEM--768%20%7C%20ML--DSA--65-blue)](docs/HARDCORE_PQC_SPEC.md)
[![URS Internal Verification](https://img.shields.io/badge/URS-internal%20verification%20defined-blue)](REALITY_MANIFEST.json)

🌐 **Live Web Application**: https://elon00.github.io/omniver-quantum-decoder/  
📦 **Repository**: https://github.com/elon00/omniver-quantum-decoder

---

## Reality Status — September 2026

| Area | Status | Evidence boundary |
|---|---|---|
| Source code | 🟢 **REAL** | Executable TypeScript/Python/React code is present in the repository. |
| PQC ML-KEM-768 | 🟢 **TESTED** | Repository tests exercise key sizes, encapsulation/decapsulation and corrupted-ciphertext behavior. |
| PQC ML-DSA-65 | 🟢 **TESTED** | Repository tests exercise key sizes, signatures, verification and negative cases. |
| Shor-style mathematics | 🟢 **TESTED** | Small-integer number-theory/order-finding invariants are asserted in the URS suite. |
| Quantum hardware execution | 🟡 **INTEGRATION PATH** | Qiskit/IBM Runtime integration is represented in code; successful production hardware execution must be separately evidenced. |
| Anna integration | 🟡 **VALIDATION PATH** | CI validates the Anna project and Python Executa compilation; public Marketplace/cloud readiness still requires the production distribution artifact. |
| Independent security audit | 🔴 **NOT COMPLETED** | Repository testing is not an independent audit. See `docs/SECURITY_AUDIT.md`. |
| Production certification | 🔴 **NOT CERTIFIED** | Production requires external evidence and human review. See `docs/PRODUCTION_READINESS.md`. |
| Market readiness | 🔴 **NOT PROVEN** | Requires real-user, sustained-usage and operational evidence. |

### Current Reality Verdict

**Omniver Quantum Decoder is a substantial, testable quantum/PQC software project. Its cryptographic and mathematical test paths are real and executable in principle, but it is not honestly certifiable as 100% production-ready or market-ready until independent security, deployment, operational and product evidence exists.**

## ⚡ PQC Test Surface

The repository includes NIST-aligned tests for:

- ML-KEM-768: public key 1,184 bytes, secret key 2,400 bytes, ciphertext 1,088 bytes, shared secret 32 bytes, decapsulation and implicit-rejection behavior.
- ML-DSA-65: public key 1,952 bytes, secret key 4,032 bytes, signature 3,309 bytes, verification and tamper/format rejection.
- RFC 5869 HKDF-SHA256 known-answer testing.
- Hybrid authorization checks using classical authorization + ML-DSA-65.

These claims describe what the repository tests; they are not a substitute for third-party certification.

### Verification commands

```bash
npm ci
npm run lint
npm run build
npm run test:nist
npm run audit:crypto
npm run reality:universal
```

The CI workflow runs lint, build, NIST PQC tests, cryptographic audit, URS verification and Anna validation/Executa compilation.

## 🧠 Shor-style Quantum Decoder

The URS suite verifies classical number-theory invariants used by the small-integer Shor-style implementation, including GCD, modular exponentiation, order finding and continued fractions. This is a simulator/research capability, not evidence of a real-world cryptographic break.

## 🤖 Anna Architecture

```text
Anna App UI
   ↓
Anna Runtime
   ↓
Bundled Executa
   ↓
Shor-style order finding / reverse sampling
   ↓
Anna Host LLM
```

The repository separates the Anna submission surface under `bundle/` and the bundled Python Executa under `executas/omniver-quantum-decoder/`.

## 🔐 Production Safety

Production and market status are intentionally **fail-closed**.

Do not represent this repository as independently audited, production-certified, marketplace/cloud-ready, or market-proven until the corresponding evidence is independently produced and reviewed.

See:

- [`docs/EXTERNAL_VERIFICATION.md`](docs/EXTERNAL_VERIFICATION.md)
- [`docs/SECURITY_AUDIT.md`](docs/SECURITY_AUDIT.md)
- [`docs/PRODUCTION_READINESS.md`](docs/PRODUCTION_READINESS.md)
- [`docs/HARDCORE_PQC_SPEC.md`](docs/HARDCORE_PQC_SPEC.md)
- [`REALITY_MANIFEST.json`](REALITY_MANIFEST.json)

## 📜 URS Interpretation

The repository's URS framework uses a weakest-link model across execution, inputs, outputs, verification, reproducibility, claim honesty, provenance, fail-closed safety, adversarial security and human audit. The internal automated engine can prove specific software assertions, but it cannot manufacture independent human audit evidence. Final status must follow the evidence.

## Disclaimer

The simulator demonstrates quantum-algorithm concepts on small integers. It does **not** demonstrate recovery of a real Bitcoin, Solana, or other production private key. Real cryptographic compromise requires authorized data, appropriate quantum resources, and independent verification.

## License

See repository license files.
