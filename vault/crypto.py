# vault/crypto.py

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

TAG_SIZE = 16  # AES-GCM standard (128-bit authentication tag)


def encrypt_vault(key: bytes, nonce: bytes, plaintext: bytes) -> bytes:
    """
    Encrypt vault plaintext using AES-256-GCM.
    Returns: ciphertext + auth_tag
    """
    if len(key) != 32:
        raise ValueError("Key must be 256 bits (32 bytes)")

    aesgcm = AESGCM(key)

    # associated_data = None (we are not authenticating extra metadata yet)
    ciphertext = aesgcm.encrypt(
        nonce=nonce,
        data=plaintext,
        associated_data=None
    )

    return ciphertext


def decrypt_vault(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    """
    Decrypt vault ciphertext using AES-256-GCM.
    Raises exception if authentication fails.
    """
    if len(key) != 32:
        raise ValueError("Key must be 256 bits (32 bytes)")

    aesgcm = AESGCM(key)

    plaintext = aesgcm.decrypt(
        nonce=nonce,
        data=ciphertext,
        associated_data=None
    )

    return plaintext
