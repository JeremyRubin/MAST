from hashlib import sha256

class hashable:
    def __init__(self, data):
        self.data = data
        self.h = hash(str(data))
    def __str__(self):
        return "{data:%s\n,hash:%s}"%(self.data, self.h)
    def hash(self):
        return self.h
class ishash:
    def __init__(self, data):
        self.data = data
    def hash(self):
        return self.data
def hash(s):
    return sha256(s).digest().encode('hex')

def verify(c, h):
    return hash(c) == h

