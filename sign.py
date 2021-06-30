from hashlib import blake2b
from hmac import compare_digest


def sign(msg: bytes, key: bytes = b'secretkey1234567890'):
    return blake2b(msg, key=key).hexdigest()


def verify(msg: bytes, sig: bytes):
    return compare_digest(sign(msg).encode('utf-8'), sig)
