import random
import mast
import copy 
import collections
import crypto
from types import *
from nodes import *

#TODO: Nitya
class Ledger():
    def __init__(self):
        self.ledger = []
        self.tmp = set()
        self.unspent = set()#TODO
    def add_txn(self, txn):
        self.tmp.add(txn)
    def commit(self):
        self.ledger.append(frozenset(self.tmp))
        self.abort()
    def abort(self):
        self.tmp = set()
    def sync(self, consensus):
        self.ledger[-1] = consensus[-1]

#TODO: Manali
class SignedHash():
    # A linked-list with a base case hash, and 
    # as for the key function, just use a unique identifier 
    def __init__(self, nestedSignedHash, pubKey):
        if isinstance(nestedSignedHash, str):
            self.h = nestedSignedHash
            self.k = pubKey
            self.next = None
        else:
            self.h = nestedSignedHash.h
            self.next = nestedSignedHash
            self.k = pubKey
    def hash(self):
        return self.h
    def sign(self, newPubKey):
        return SignedHash(self, newPubKey)
    def signedBy(self, pubKey):
        return pubKey in self
    def __iter__(self):
        cur = self
        while cur.next:
            yield cur.k
            cur = cur.next
        yield cur.k

    def serial(self):
        return {'h':self.hash(),'s':list(self)}
    @staticmethod
    def deserial(d):
        s = SignedHash(d['h'],d['s'].pop())
        return reduce(lambda x,y: x.sign(y), d['s'], s)


class Signatory():
    # This is an entity which builds contracts. They can 'sign' strings with their pubKey
    # And we can see if they signed a string
    def __init__(self, id):
        self.pubKey  = id
        self.__secKey__ = id
    def __sign__(string):
        return SignedHash(string).sign(self.pubKey)
    def checkSig(signed_hash):
        return signed_hash.signedBy(self.pubKey)

class Txn():
    # The main deal for a contract
    def __init__(self, mRootHash, amt):
        self.mRootHash = mRootHash
        self.nextTxn = None
        self.amt = amt
    # run the prelude
    def execute(self, args):
        signature  = args.pop()
        if crypto.hash("".join(map(str, args))) != signature.hash():
            self.nextTxn = Invalid()
            return
        # args[0] - prooflist for mRootHash
        # args[1] - list of branches to Execute
        ret = merkleVerifyExec(signature, self.mRootHash, args) # defines ret when executing, pass all args
        if not ret:
            raise ValueError("Invalid ret")
        self.nextTxn = verify(ret)
    # the result of Execute
    def nextTxn():
        return self.nextTxn
    # the id of the txn
    def hash():
        return self.mRootHash
    def verify(ret):
        def check_pred(pairs):
            total = sum([pair[1] for pair in pairs])
            return Valid(pairs) if (0 < total) and (total <= self.amnt) else Invalid()
        return ret.map(check_pred).map(lambda x: map([Txn(a,b) for (a,b) in x]))


def merkleVerifyExec(sig, mroot, args):
    pr = args.pop()
    # Set up API
    from datetime import datetime as dt
    signed = lambda key, sig: frozenset(key) <= frozenset(SignedHash.deserial(sig)) # test that key is a subset
    if mast.Mast.upwardProve(pr):
        try:
            code = "".join(code for _, code, _ in pr[::-1])
            glob = {"signed":signed, "dt":dt}
            loc = {}
            print loc, glob
            exec code in glob, loc
            return glob['ret']
        except Exception as e:
            print "merkleVerify fails with:%s"%e
            return Invalid()
    else:
        return Invalid()
