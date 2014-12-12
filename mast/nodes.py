import sys
import random
import copy
import collections
from sim import Ledger

class GlobalConsensus():
    # List of frozensets , where a[i] corresponds to the new blocks from a tick stored in a 
# frozenset
    ledger = Ledger()
    @classmethod
    def init(cls, txns):
        for txn in txns:
            cls.ledger.add_txn(txn)
        cls.ledger.commit()
    @classmethod
    def consensus_tick(cls, nodes):
        cls.update_ledger(nodes)
    @classmethod
    def update_ledger(cls, nodes):
        count = collections.Counter([frozenset(node.ledger_copy.ledger) for node in nodes]).most_common(1)[0][0]
        cls.ledger.add_txn(count)

    # run global consensus, update ledger

class ConsensusNode():
    # Simulated consensus node
    # Make a local copy of the ledger
    def __init__(self, l=GlobalConsensus):
        self.global_ledger = l
        self.ledger_copy = copy.deepcopy(l.ledger)
        self.txn_queue = []


    def includeTxn(self, c): # SignedHash c
        #include c in ledger if c is unspent
        if not any(c in block for block in self.ledger_copy.ledger):
            self.ledger_copy.add_txn(c)

    def verifyExecTxn(self, c, arglist, debug=False): # regular hash c
        print
        print arglist
        c.execute(copy.deepcopy(arglist), debug=debug)
        return c.nextTxn().isValid()

    # Canonicalize rule, checking TXN's, excluding ones as needed
    # put to local ledger if valid
    def tick(self, debug=False):
        for c, arglist in self.txn_queue:
            if self.verifyExecTxn(c, arglist, debug=debug):
                self.includeTxn(c)
            else:
                print "invalid argument", c, arglist
        self.ledger_copy.commit()

    def useGlobalConsensus(self):
        # sync with global
        self.ledger_copy.sync(self.global_ledger)

    def receive(self, c, arglist):
        # receive should add to processing queue
        self.txn_queue.append((c,copy.deepcopy(arglist)))


#faithful impl of methods: inherits all behaviors from ConsensusNode
class GoodNode(ConsensusNode):
   pass 

class EvilNode(ConsensusNode):
    # tries to inject bad things into consensus
    def includeTxn(self, c): # SignedHash c
        #malicious, if c is already in ledger, remove the item from ledger
        if c in self.ledger_copy.ledger:
            self.ledger_copy.pop(c)

class InconsistentNode(ConsensusNode):
    # unpredictably behaves like either a goodnode or evilnode
    def includeTxn(self, c): # SignedHash c
        #inconsistent, add c to the ledger probablistically
        if c not in self.ledger_copy.ledger:
            if random.random() > 0.9:
                self.ledger_copy.add_txn(c)
