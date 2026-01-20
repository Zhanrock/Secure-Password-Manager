# vault/kdf.py

from argon2.low_level import hash_secret_raw, Type

ARGON2_TIME_COST = 3
ARGON2_MEMORY_COST = 64 * 1024  # KB
ARGON2_PARALLELISM = 2
KEY_SIZE = 32  # 256-bit key


def derive_key(
    password: str,
    salt: bytes,
    *,
    time_cost: int,
    memory_cost: int,
    parallelism: int,
) -> bytes:
    """
    Derive encryption key from password using Argon2id.
    """
    if isinstance(password, str):
        password = password.encode("utf-8")

    return hash_secret_raw(
        secret=password,
        salt=salt,
        time_cost=time_cost,
        memory_cost=memory_cost,
        parallelism=parallelism,
        hash_len=KEY_SIZE,
        type=Type.ID,
    )
