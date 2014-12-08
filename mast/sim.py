#TODO: Nitya
class GlobalConsnesus:
    # List of frozensets , where a[i] corresponds to the new blocks from a tick stored in a 
# frozenset
    ledger = []
    @classmethod
    def consensus_tick(cls, nodes):
        pass
    # run global consensus, update ledger

class ConsensusNode():
    # Simulated consensus node
    # Make a local copy of the ledger
    def __init__(GlobalConsnesu):
        ledger

    def includeTxn(self, c): # SignedHash c
        #include c in ledger if c not in ledger
        pass
    def verifyExecTxn(c, arglist): # regular hash c
        #  obvi
        #    execute txn
        pass
    # Canonicalize rule, checking TXN's, excluding ones as needed
    # put to local ledger if valid
    def tick():
        #runs a tick of simulation 
        pass
    def useGlobalConsensus(ledger):
        # sync with global
        pass
    def recieve(self, hash, arglist):
        # recieve should add to processing queue
        pass


class GoodNode(ConsensusNode):
    #faithful impl of methods
    pass
class EvilNode(ConsensuseNode):
    # tries to inject bad things into consensus
    pass
class InconsistentNode(ConsensusNode):
    # unpredictably behaves like either a goodnode or evilnode
    pass

#TODO: Manali
class SignedHash:
    # Implement this as a linked-list with a base case hash, and 
    # as for the key function, just use a unique identifier 
    def __init__(self, nestedSignedHash):
        pass        
    def hash(self):
        pass
    def sign(self, pubKey):
        pass
    def signedBy(self):
        pass

class Signatory():
    # This is a enttity which builds contracts. They can 'sign' strings with their pubKey
    # And we can see if they signed a string
    def __init__(self):
        self.pubKey  = ?
        self.__secKey__ = ?
    def __sign__(string):
        pass
    def checkSig(string):

class Txn():
    # The main deal for a contract
    def __init__(data):
        pass
    # run the prelude
    def execute(self, [arglist]):
        pass
    # the result of Execute
    def nextTxn():
        pass
    # the id of the txn
    def hash():
        pass

#TODO: Jeremy
class Maybe():
    # ABC for a maybe type
    def isValid():
        pass
    def validValue():
        pass
class Valid(Maybe):
    def __init__(self, value):
        self.value = value
    def isValid():
        return True
    def validValue():
        return self.value
class Invalid(Maybe):
    def isValid():
        return False

class Ledger():
    def __init__():
        self.ledger = []
        self.tmp = frozenset()
    def add_txn(self, txn):
        self.tmp.add(txn)
    def commit(self):
        self.ledger.append(self.tmp)
        self.abort()
    def abort(self):
        self.tmp = frozenset()
    def sync(self, consensus):
        self.ledger[-1] = consensus[-1]

# implement some consistent version from Mast.py
def prove(a, b, c):
    pass
    #merkleroot matches pl
    #pl matches cl
def merkelVerify(merkleroot, pl, cl):
    if not prove(mekrleroot, pl, cl):
        map(exec, cl)
prelude = """
signature  = a.pop()
if hash(a) != signature.content:
    return Invalid()
# Args[1] is a prooflist for merklehash
# Args[2] is the list of branches to Execute
merkleVerify(merkelhash, args[1], args[2])
"""
