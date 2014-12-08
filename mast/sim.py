import random
import mast

#TODO: Nitya
class GlobalConsensus():
    # List of frozensets , where a[i] corresponds to the new blocks from a tick stored in a 
# frozenset
    self.ledger = []
    @classmethod
    def consensus_tick(cls, nodes):
        update_ledger(nodes)

    def update_ledger(nodes):
        for node in nodes:
            for entry in node.ledger_copy:
                if entry not in self.ledger:
                    self.ledger.push(entry)

    # run global consensus, update ledger

class ConsensusNode():
    # Simulated consensus node
    # Make a local copy of the ledger
    def __init__(GlobalConsensus):
        self.ledger_copy = GlobalConsensus.ledger
        self.txn_queue = []

    def includeTxn(self, c): # SignedHash c
        #include c in ledger if c not in ledger
        if c not in self.ledger_copy:
            self.ledger_copy.push(c)

    def verifyExecTxn(c, arglist): # regular hash c
        #  obvi
        #    execute txn
        c.execute(arglist)
        #TODO: what is returned here? How do we know if valid?

    # Canonicalize rule, checking TXN's, excluding ones as needed
    # put to local ledger if valid
    def tick():
        for c, arglist in self.txn_queue:
            verifyExecTxn(c, arglist)
            #TODO: what is returned? How to know if valid?

    def useGlobalConsensus(ledger):
        # sync with global
        self.ledger_copy = GlobalConsensus.ledger

    def receive(self, c, arglist):
        # receive should add to processing queue
        self.txn_queue.push((c,arglist))


class GoodNode(ConsensusNode):
    #faithful impl of methods
    
    

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
            if random.random() > 0.5:
                self.ledger_copy.push(c)

#TODO: Manali
class SignedHash():
    # A linked-list with a base case hash, and 
    # as for the key function, just use a unique identifier 
    def __init__(self, nestedSignedHash):
        self.val = nestedSignedHash
        self.next = None
    def hash(self):
        cur = self
        while cur.next:
            cur = cur.next
        return cur.val
    def sign(self, pubKey):
        self.next = self.val
        self.val = pubKey
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
        if hash(tuple(args)) != signature.hash():
            return Invalid()
        pl = args[0] # prooflist for mRootHash
        cl = args[1] # list of branches to Execute
        merkleVerify(self.mRootHash, args) # defines ret when executing, pass all args?
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
    def isValid():
        pass
class Valid(Maybe):
    def __init__(self, value):
        self.value = value
    def isValid():
        return True
class Invalid(Maybe):
    def isValid():
        return False

class Ledger():
    def __init__():
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

# implement some consistent version from Mast.py
def prove(a, b, c):
    pass
    #merkleroot matches pl
    #pl matches cl
def merkelVerify(merkleroot, pl, cl):
    if prove(mekrleroot, pl, cl):
        map(exec, cl)
prelude = """
signature  = a.pop()
if hash(a) != signature.content:
    return Invalid()
# Args[1] is a prooflist for merklehash
# Args[2] is the list of branches to Execute
merkleVerify(merkelhash, args[1], args[2])
"""
