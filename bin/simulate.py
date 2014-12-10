from mast.sim import *
import mast.mast as mast
first = Mast("""
if (signed(frank, signature)):
    # Allow alice to pass in a new txn, not hard coded(ContractTxn)
    ret Valid([args[-1]])
""")


will = Mast("""
if (signed(alice, signature)):
    # Allow alice to pass in a new txn, not hard coded(ContractTxn)
    ret = Valid([args[-1]])
if (signed([bob and carol], signature)):
    if (args[1] > 3 and args[1] < 10):
        ret = Valid(["output txn doing something specific"])
    #? more conditions
if (date.time.now() > year100000)
    ret = Valid(args[-1])
""")


mWill = Mast(prelude)
map(mWill.addBr,
["""
if (signed(alice, signature)):
    # Allow alice to pass in a new txn, not hard coded(ContractTxn)
    ret = Valid([args[-1]])
""",
"""
if (signed([bob and carol], signature)):
    if (args[1] > 3 and args[1] < 10):
        ret = Valid(["output txn doing something specific"])
    #? more conditions
""",
"""
if (date.time.now() > year100000)
    ret = Valid(args[-1])
"""])


if __name__ == "__main__":
    #initialize txnstream

    # Make Nodes
    goodNodes = [GoodNode() for x in xrange(100)] 
    badNodes = [EvilNode() for x in xrange(10)]
    inconsistentNodes = [InconsistentNode for x in xrange(20)]
    nodes = inconsistentNodes + badNodes + goodNodes
    for txnSet in txnstream:
        for txn in txnSet:
            [n.receive(txn) for n in nodes]
        [n.tick() for n in nodes]
        GlobalConsensus.consensus_tick(nodes)
    GlobalConsensus.consensus_tick(goodNodes)
