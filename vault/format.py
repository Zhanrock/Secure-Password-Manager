# vault/format.py

import struct
import os
from .kdf import (
    ARGON2_TIME_COST,
    ARGON2_MEMORY_COST,
    ARGON2_PARALLELISM,
)

# ---- VAULT FORMAT CONSTANTS ----
VAULT_MAGIC = b"PMGR"
VAULT_VERSION = 1
NONCE_SIZE = 12  # AES-GCM standard
SALT_SIZE = 16



def create_vault_header() -> dict:
    """
    Create a new vault header with fresh randomness.
    """
    return {
        "magic": VAULT_MAGIC,
        "version": VAULT_VERSION,
        "salt": os.urandom(SALT_SIZE),
        "nonce": os.urandom(NONCE_SIZE),
        "kdf_params": {
            "time_cost": ARGON2_TIME_COST,
            "memory_cost": ARGON2_MEMORY_COST,
            "parallelism": ARGON2_PARALLELISM,
        },
    }


def serialize_header(header: dict) -> bytes:
    """
    Serialize vault header into bytes.
    """
    return b"".join([
        header["magic"],
        struct.pack(">I", header["version"]),
        header["salt"],
        header["nonce"],
        struct.pack(">I", header["kdf_params"]["time_cost"]),
        struct.pack(">I", header["kdf_params"]["memory_cost"]),
        struct.pack(">I", header["kdf_params"]["parallelism"]),
    ])

def parse_header(data: bytes) -> dict:
    """
    Parse vault header from bytes.
    """
    offset = 0

    magic = data[offset:offset+4]
    offset += 4

    if magic != VAULT_MAGIC:
        raise ValueError("Invalid vault file")

    version = struct.unpack(">I", data[offset:offset+4])[0]
    offset += 4

    salt = data[offset:offset+SALT_SIZE]
    offset += SALT_SIZE

    nonce = data[offset:offset+NONCE_SIZE]
    offset += NONCE_SIZE

    time_cost = struct.unpack(">I", data[offset:offset+4])[0]
    offset += 4

    memory_cost = struct.unpack(">I", data[offset:offset+4])[0]
    offset += 4

    parallelism = struct.unpack(">I", data[offset:offset+4])[0]
    offset += 4

    return {
        "version": version,
        "salt": salt,
        "nonce": nonce,
        "kdf_params": {
            "time_cost": time_cost,
            "memory_cost": memory_cost,
            "parallelism": parallelism,
        },
        "header_size": offset,
    }

