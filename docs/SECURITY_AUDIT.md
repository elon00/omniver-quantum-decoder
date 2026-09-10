# Security Audit Status

## Repository status

**Independent security audit: NOT COMPLETED.**

The repository contains substantial automated cryptographic testing, including NIST FIPS 203/204 wire-invariant checks, signature verification and negative tests, ML-KEM implicit-rejection checks, RFC 5869 known-answer testing, and URS automation.

These tests are engineering evidence. They are not a substitute for a qualified independent security audit.

## Required review scope

- Cryptographic implementation and dependency review.
- Randomness, key generation, key storage and lifecycle.
- Input parsing, serialization and malformed-input behavior.
- ML-KEM-768 and ML-DSA-65 integration boundaries.
- Hybrid classical/PQC authorization logic.
- Web application and server attack surface.
- Python Executa / Anna integration and packaging.
- CI/CD and supply-chain controls.
- Secrets and deployment configuration.
- Denial-of-service and resource exhaustion paths.

## Evidence standard

A future auditor should record methodology, commit SHA, environment, tools, findings, severity, remediation status, and retest results. Only then may the independent-audit URS dimension move to verified.
