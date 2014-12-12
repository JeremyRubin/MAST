import sys
import traceback
import random
import mast
import copy 
import collections
import crypto
from pprint import pprint as pretty
from maybetypes import *
import base64
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
        return pubKey in list(self)
    def __getitem__(self, i):
        return list(self)[i]
    def __iter__(self):
        cur = self
        while cur.next:
            yield cur.k
            cur = cur.next
        yield cur.k
    def __str__(self):
        return str(self.serial())
    def __repr__(self):
        return str(self)
    def serial(self):
        return {'type':'SignedHash','h':self.hash(),'s':list(self)}
    @staticmethod
    def deserial(d):
        print d
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
        self._nextTxn = Invalid()
        self.amt = amt
        self.args = None
    # run the prelude
    def execute(self, args, debug=False):
        print "ARRRGHS",args
        self.args = copy.deepcopy(args)
        signature  = args.pop()
        print signature
        if crypto.hash("".join(map(str, args))) != signature.hash():
            self.nextTxn = Invalid()
            return
        # args[0] - prooflist for mRootHash
        # args[1] - list of branches to Execute
        ret = merkleVerifyExec(signature, self.mRootHash, args, self.amt, debug=debug) # defines ret when executing, pass all args
        if not ret:
            raise ValueError("Invalid ret")
        print ret
        self._nextTxn = self.verify(ret)
    # the result of Execute
    def nextTxn(self):
        return self._nextTxn
    def __hash__(self):
        return int(base64.b16encode(self.mRootHash),36)
    def verify(self, ret):
        def check_pred(pairs):
            total = sum([pair[1] for pair in pairs])
            return Valid(pairs) if (0 < total) and (total <= self.amt) else Invalid()
        return ret.map(check_pred).map(lambda x: Valid([Txn(a,b) for (a,b) in x]))

    def __repr__(self):
        return "TXN: {hash:%r, args:%r, amt: %r"%(self.mRootHash, self.args, self.amt)

def merkleVerifyExec(sig, mroot, args, amt, debug=False):
    pr = args.pop()
    # Set up API
    from datetime import datetime as dt
    signed = lambda key, user_sig: frozenset(list(key)) <= frozenset(list(user_sig)) # test that key is a subset
    if mast.upwardProve(pr, mroot, debug=debug):
        code = "".join(pr[1][::-1])
        try:
            glob = {"signed":signed, "dt":dt, "sig":sig, "args":args, "amt":amt, "Valid":Valid, "Invalid":Invalid}
            loc = {}
            exec code in glob, loc
            return loc['ret'] if 'ret' in loc else Invalid()
        except Exception as e:
            print "merkleVerify fails with:%s"%e
            print code
            traceback.print_exc(e)
            print 
            print 
            return Invalid()
    else:
        return Invalid()
