# messaging.py
def xor_encrypt_decrypt(message: str, key: str) -> str:
    """
    Simple XOR encryption/decryption using BB84 shared key.
    Key is repeated to match the message length.
    """
    key_expanded = (key * (len(message) // len(key) + 1))[:len(message)]
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, key_expanded))
