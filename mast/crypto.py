from hashlib import sha256

def _hash(s):
    return sha256(s).digest().encode('hex')

def verify(c, h):
    return _hash(c) == h

