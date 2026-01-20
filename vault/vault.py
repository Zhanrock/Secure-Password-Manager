# vault/vault.py

import json
from pathlib import Path

from .format import (
    create_vault_header,
    serialize_header,
    parse_header,
)

from .kdf import derive_key
from .crypto import encrypt_vault, decrypt_vault


def create_vault(path: str, password: str) -> None:
    """
    Create a new encrypted vault file.
    """
    path = Path(path)

    if path.exists():
        raise FileExistsError("Vault already exists")

    # 1. Create header
    header = create_vault_header()
    header_bytes = serialize_header(header)

    # 2. Initial vault content
    vault_data = {
        "version": header["version"],
        "entries": {}
    }
    plaintext = json.dumps(vault_data).encode("utf-8")

    # 3. Derive encryption key
    key = derive_key(
        password=password,
        salt=header["salt"],
        time_cost=header["kdf_params"]["time_cost"],
        memory_cost=header["kdf_params"]["memory_cost"],
        parallelism=header["kdf_params"]["parallelism"],
    )

    # 4. Encrypt vault
    ciphertext = encrypt_vault(
        key=key,
        nonce=header["nonce"],
        plaintext=plaintext
    )

    # 5. Write file
    with open(path, "wb") as f:
        f.write(header_bytes)
        f.write(ciphertext)


def open_vault(path: str, password: str) -> dict:
    """
    Open and decrypt an existing vault.
    Returns decrypted vault data.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError("Vault not found")

    data = path.read_bytes()

    # 1. Parse header
    header = parse_header(data)

    header_size = header["header_size"]
    ciphertext = data[header_size:]

    # 2. Derive key
    key = derive_key(
        password=password,
        salt=header["salt"],
        time_cost=header["kdf_params"]["time_cost"],
        memory_cost=header["kdf_params"]["memory_cost"],
        parallelism=header["kdf_params"]["parallelism"],
    )

    # 3. Decrypt vault
    try:
        plaintext = decrypt_vault(
            key=key,
            nonce=header["nonce"],
            ciphertext=ciphertext
        )
    except Exception:
        raise ValueError("Invalid password or corrupted vault")

    # 4. Load JSON
    return json.loads(plaintext.decode("utf-8"))

def save_vault(vault_data: dict, path: str, password: str) -> None:
    """
    Save updated vault data back to file, re-encrypting it.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError("Vault not found")

    # 1. Read existing file header
    data = path.read_bytes()
    header = parse_header(data)
    header_size = header["header_size"]

    # 2. Serialize vault JSON
    plaintext = json.dumps(vault_data).encode("utf-8")

    # 3. Derive key (reuse salt & KDF params from header)
    key = derive_key(
        password=password,
        salt=header["salt"],
        time_cost=header["kdf_params"]["time_cost"],
        memory_cost=header["kdf_params"]["memory_cost"],
        parallelism=header["kdf_params"]["parallelism"],
    )

    # 4. Encrypt vault
    ciphertext = encrypt_vault(
        key=key,
        nonce=header["nonce"],
        plaintext=plaintext
    )

    # 5. Atomic write
    temp_path = path.with_suffix(".tmp")
    with open(temp_path, "wb") as f:
        f.write(data[:header_size])  # original header
        f.write(ciphertext)
    temp_path.replace(path)

