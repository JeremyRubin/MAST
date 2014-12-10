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
        self.ledger_copy = copy.deepcopy(l.ledger)
        self.txn_queue = []


    def includeTxn(self, c): # SignedHash c
        #include c in ledger if c not in ledger
        if not any(c in block for block in self.ledger_copy):
            self.ledger_copy[-1].addtxn(set([c]))

    def verifyExecTxn(self, c, arglist): # regular hash c
        c.execute(arglist)
        return c.nextTxn().isValid()
        #TODO: what is returned here? How do we know if valid?

    # Canonicalize rule, checking TXN's, excluding ones as needed
    # put to local ledger if valid
    def tick(self):
        self.ledger_copy.add_txn(set())
        for c, arglist in self.txn_queue:
            if not verifyExecTxn(c, arglist):
                print "invalid argument", c, arglist

    def useGlobalConsensus(self,ledger):
        # sync with global
        self.ledger_copy = copy.deepcopy(ledger)

    def receive(self, c, arglist):
        # receive should add to processing queue
        self.txn_queue.append((c,arglist))


class GoodNode(ConsensusNode):
    #faithful impl of methods
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
    def __init__(self, nestedSignedHash, pubKey=None):
        if isinstance(nestedSignedHash, str):
            self.val = nestedSignedHash
            self.next = None
        else:
            self.next = nestedSignedHash
            self.val = pubKey
    def hash(self):
        cur = self
        while cur.next:
            cur = cur.next
        return cur.val
    def sign(self, newPubKey):
        return SignedHash(self, newPubKey)
    def signedBy(self, pubKey):
        cur = self
        while cur.next:
            if cur.val == pubKey:
                return True
            cur = cur.next
        return False

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
    def __init__(self, mRootHash):
        self.mRootHash = mRootHash
        self.nextTxn = None
    # run the prelude
    def execute(self, args):
        signature  = args.pop()
        if crypto.hash(tuple(args)) != signature.hash():
            self.nextTxn = Invalid()
            return
        # args[0] - prooflist for mRootHash
        # args[1] - list of branches to Execute
        merkleVerify(self.mRootHash, args) # defines ret when executing, pass all args
        self.nextTxn = ret
        if not ret:
            raise ValueError("Invalid ret")
    # the result of Execute
    def nextTxn():
        return self.nextTxn
    # the id of the txn
    def hash():
        return self.mRootHash

#TODO: Jeremy
class Maybe():
    # ABC for a maybe type
    def isValid(self):
        pass
    def __str__(self):
        if self.isValid():
            return "Valid(%s)"%repr(self.value)
        else:
            return "Invalid()"
class Valid(Maybe):
    def __init__(self, value):
        self.value = value
    def isValid(self):
        return True
class Invalid(Maybe):
    def isValid(self):
        return False

def merkleVerify(mroot, args):
    pr = args.pop()
    if mast.Mast.upwardProve(pr):
        for _, code, _ in pr:
            exec code
    return ret
prelude = """
signature  = a.pop()
if hash(a) != signature.content:
    return Invalid()
# Args[1] is a prooflist for merklehash
# Args[2] is the list of branches to Execute
merkleVerify(merkelhash, args[0], args[1])
"""
