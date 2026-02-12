#  Secure Password Vault (Python)

A **local, encrypted password manager** implemented from scratch using modern cryptography primitives.  
Designed as a **security-focused portfolio project** demonstrating cryptographic engineering, clean architecture, and defensive programming.

---

##  Features

-  **Master password–protected vault**
-  Argon2 key derivation (memory-hard)
-  AES-256-GCM authenticated encryption
-  Structured binary vault format
-  Interactive CLI interface
-  Search & filter entries
-  Tamper detection & wrong-password rejection

---

##  Architecture Overview

```bash
vault/
├── kdf.py          # Argon2 key derivation
├── crypto.py       # AES-256-GCM encryption/decryption
├── format.py       # Vault header serialization/parsing
└── vault.py        # Create/open/save vault workflows
main.y        # For testing
cli.py        # User-facing CLI
```

### Separation of concerns
- **Crypto code** is isolated and testable
- **CLI never touches raw keys**
- **Vault format is versioned and extensible**

---

##  Cryptographic Design

| Component   | Choice       | Reason |
|------------|-------------|--------|
| KDF        | Argon2id     | Memory-hard, GPU-resistant |
| Encryption | AES-256-GCM  | Confidentiality + authentication |
| Salt       | 128-bit random | Prevents rainbow tables |
| Nonce      | 96-bit random  | GCM best practice |

Wrong passwords or modified files **fail safely**.

---

##  Usage

```bash
python cli.py

 Secure Password Vault
1. Create new vault
2. Open existing vault
3. Exit
```

#  Security Notes

Vault is encrypted at rest

Keys are derived per vault

Authentication tags detect tampering

No plaintext passwords written to disk

See SECURITY.md for full threat model.

#  Educational Goals

This project was built to:

Understand real-world cryptographic workflows

Practice secure file formats

Apply defensive programming techniques

Build portfolio-ready systems code

#  Future Improvements

Clipboard auto-clear

Password strength checks

Vault locking timeout

Hardware-backed key storage

GUI frontend
