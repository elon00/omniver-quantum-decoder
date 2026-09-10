# Omniver Quantum Decoder: Hardcore PQC Technical Specification

**Standards:** NIST FIPS 203 (ML-KEM-768), NIST FIPS 204 (ML-DSA-65), RFC 5869 (HKDF-SHA256)  
**Security Level:** NIST Security Category 3 (AES-192 / SHA-384 Classical Equivalent)  
**Library Foundation:** `@noble/post-quantum`, `@noble/hashes`, `@noble/curves` (Pure TypeScript, Zero Native C/Wasm Vulnerabilities, Constant-Time Primitives)  

---

## 1. Cryptographic Primitive Architecture

Omniver Quantum Decoder integrates state-of-the-art Module Lattice Cryptography across both encryption (KEM) and authentication (DSA):

```
+-----------------------------------------------------------------------------------+
|                        OMNIVER QUANTUM DECODER CRYPTO ENGINE                      |
+-----------------------------------------+-----------------------------------------+
|      NIST FIPS 203 (ML-KEM-768)         |       NIST FIPS 204 (ML-DSA-65)         |
|   Module-Lattice Key Encapsulation      |    Module-Lattice Digital Signatures    |
+-----------------------------------------+-----------------------------------------+
| - Public Key:  1,184 Bytes (9,472 bits) | - Public Key:  1,952 Bytes (15,616 bits)|
| - Secret Key:  2,400 Bytes              | - Secret Key:  4,032 Bytes              |
| - Ciphertext:  1,088 Bytes              | - Signature:   3,309 Bytes              |
| - Shared Key:  32 Bytes (256 bits)      | - Context:     Deterministic Attestation|
| - Implicit Rejection: FIPS 203 §7.3     | - Attack Matrix: 9/9 Invariant Vectors  |
+-----------------------------------------+-----------------------------------------+
```

---

## 2. NIST FIPS 203 ML-KEM-768 Wire Invariants

- **Key Generation:** Deterministic derivation from 64-byte seed $d || z$ or secure CSPRNG.
- **Encapsulation:** 
  $$\text{ML-KEM.Encaps}(pk) \to (c, K)$$
  where $c$ is exactly 1,088 bytes and $K$ is exactly 32 bytes (256-bit AES/ChaCha key).
- **Implicit Rejection (§7.3):**
  When an adversary supplies an altered or malformed ciphertext $c'$, the decapsulation algorithm does not crash or reveal error side-channels; instead, it deterministically outputs a pseudorandom key derived from the secret key seed $z$:
  $$K \gets \text{J}(z || c')$$
  This guarantees IND-CCA2 security against chosen-ciphertext quantum and classical attacks.

---

## 3. NIST FIPS 204 ML-DSA-65 Wire Invariants

- **Key Generation:** Deterministic matrix expansion over ring $R_q = \mathbb{Z}_q[X]/(X^{256} + 1)$ with modulus $q = 8380417$.
- **Signing:** Generates 3,309-byte lattice signatures with rejection sampling ensuring uniform distribution independent of private key elements.
- **Verification:** Strict verification rejecting out-of-range polynomial coefficients and altered message digests.

---

## 4. Wycheproof Negative & Adversarial Vectors

The suite executes 23 automated invariant assertions:
1. Bit-flipped signature rejection.
2. Truncated signature buffer rejection.
3. Malformed public key size rejection.
4. Altered message payload verification failure.
5. RFC 5869 Test Case 1 byte-for-byte Known Answer Test (KAT).
