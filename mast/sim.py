import random
import mast
import copy 
import collections
import crypto

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

class GlobalConsensus():
    # List of frozensets , where a[i] corresponds to the new blocks from a tick stored in a 
# frozenset
    
    ledger = Ledger()
    @classmethod
    def consensus_tick(cls, nodes):
        cls.update_ledger(nodes)
    @classmethod
    def update_ledger(cls, nodes):
        cls.ledger.addtxn(collections.Counter([frozenset(node.ledger_copy) for node in nodes]).most_common(1)[0][0])


    # run global consensus, update ledger

class ConsensusNode():
    # Simulated consensus node
    # Make a local copy of the ledger
    def __init__(self, l=GlobalConsensus):
        self.global_ledger = l
        self.ledger_copy = copy.deepcopy(l.ledger)
        self.txn_queue = []


    def includeTxn(self, c): # SignedHash c
        #include c in ledger if c not in ledger
        if not any(c in block for block in self.ledger_copy):
            self.ledger_copy.add_txn(c)

    def verifyExecTxn(self, c, arglist): # regular hash c
        c.execute(arglist)
        return c.nextTxn().isValid()


    # Canonicalize rule, checking TXN's, excluding ones as needed
    # put to local ledger if valid
    def tick(self):
        for c, arglist in self.txn_queue:
            if self.verifyExecTxn(c, arglist):
                self.includeTxn(c)
            else:
                print "invalid argument", c, arglist
        self.ledger_copy.commit()

    def useGlobalConsensus(self):
        # sync with global
        self.ledger_copy.sync(self.global_ledger)

    def receive(self, c, arglist):
        # receive should add to processing queue
        self.txn_queue.append((c,arglist))


class GoodNode(ConsensusNode):
    #faithful impl of methods: inherits all behaviors from ConsensusNode
   pass 
    

class EvilNode(ConsensusNode):
    # tries to inject bad things into consensus
    def includeTxn(self, c): # SignedHash c
        #malicious, if c is already in ledger, remove the item from ledger
        if c in self.ledger_copy:
            self.ledger_copy.pop(c)

class InconsistentNode(ConsensusNode):
    # unpredictably behaves like either a goodnode or evilnode
    def includeTxn(self, c): # SignedHash c
        #inconsistent, add c to the ledger probablistically
        if c not in self.ledger_copy:
            if random.random() > 0.9:
                self.ledger_copy.push(c)

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
        if crypto.hash(tuple(args)) != signature.hash():
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

#TODO: Jeremy
class Maybe():
    # ABC for a maybe type
    def isValid(self):
        pass
    def map(self, fn):
        pass
    def __str__(self):
        if self.isValid():
            return "Valid(%s)"%repr(self.value)
        else:
            return "Invalid()"
class Valid(Maybe):
    def __init__(self, value):
        self.value = value
    def map(self, fn):
        return Valid(fn(self.value))
    def isValid(self):
        return True
class Invalid(Maybe):
    def isValid(self):
        return False
    def map(self, fn):
        return Invalid()
def merkleVerifyExec(sig, mroot, args):
    pr = args.pop()
    # Set up API
    from datetime import datetime as dt
    signed = lambda key, sig: frozenset(key) <= frozenset(SignedHash.deserial(sig)) # test that key is a subset
    if mast.Mast.upwardProve(pr):
        try:
            code = "".join(code for _, code, _ in pr[::-1])
            exec code
            return ret
        except Exception as e:
            print "merkleVerify fails with:%s"%e
            return Invalid()
    else:
        return Invalid()
