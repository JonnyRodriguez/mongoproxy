from hashlib import blake2b
from hmac import compare_digest


def sign(msg: bytes, key: bytes):
    return blake2b(msg, key=key).hexdigest()


def verify(msg: bytes, sig: bytes, key: bytes):
    return compare_digest(sign(msg, key).encode('utf-8'), sig)
