# Security Policy & Design Notes

This document describes the security goals, threat model, design decisions, and limitations of the **Secure Password Vault** project.

This project is intended as a **learning and portfolio project** demonstrating applied cryptography and secure software design principles. It is **not intended to replace production-grade password managers**.

---

## Security Goals

The primary security goals of this project are:

- Protect stored credentials against offline attacks if the vault file is stolen
- Ensure confidentiality and integrity of vault data at rest
- Detect incorrect passwords and file tampering reliably
- Avoid unsafe cryptographic practices and common implementation pitfalls

---

## Threat Model

### In-Scope Threats

The system is designed to defend against:

- **Offline attackers** who obtain a copy of the encrypted vault file
- **Brute-force and dictionary attacks** against the master password
- **File tampering or corruption**, including malicious modification of vault contents
- **Accidental data exposure** via plaintext storage

---

### Out-of-Scope Threats

The following threats are **not** addressed by this project:

- Malware, keyloggers, or compromised operating systems
- Side-channel attacks (timing, power analysis, cache attacks)
- Physical attacks on hardware
- Online attacks or remote exploitation
- Shoulder surfing or social engineering

---

## Cryptographic Design

### Key Derivation

- Master password is processed using **Argon2id**
- Memory-hard parameters are chosen to resist GPU and ASIC attacks
- A unique random salt is generated per vault

This design slows down offline brute-force attempts and prevents rainbow table attacks.

---

### Encryption & Authentication

- Vault data is encrypted using **AES-256-GCM**
- GCM provides both confidentiality and integrity
- Authentication tags ensure that modified or corrupted vaults are detected

If decryption or authentication fails, the vault is rejected without revealing sensitive information.

---

### Vault Format

- Vaults use a **custom binary format** consisting of:
  - Magic bytes and version number
  - Random salt and nonce
  - KDF parameters
  - Encrypted payload

- Versioning allows future format upgrades without breaking compatibility

---

## Key Lifecycle & Memory Safety

- Encryption keys are derived only when needed
- Keys are not written to disk
- Plaintext data exists only temporarily in memory
- Vault contents are decrypted only after successful authentication

---

## Error Handling

- Incorrect passwords result in a generic failure message
- Authentication failures do not reveal whether the password or file is incorrect
- Input validation and exception handling prevent undefined behavior

---

## Known Limitations

This project intentionally avoids certain features for simplicity:

- No clipboard auto-clearing
- No password strength enforcement
- No automatic vault locking timeout
- No secure memory wiping guarantees (Python limitation)
- No multi-factor authentication

---

## Responsible Use

This project is intended for:
- Educational purposes
- Demonstrating cryptographic and security engineering skills
- Portfolio and internship applications

It should **not** be used to store highly sensitive or production credentials.

---

## Reporting Issues

If you discover a security flaw or implementation issue, please open an issue on the repository with a clear description of the problem and steps to reproduce it.
