from mast.sim import *
from mast.mast import *
from pprint import pprint as pretty
def mkM(s, ic=None):
    return Mast('compile', s, initialChildren=ic)
def normal(key):
    return mkM("if (signed(%r, signature)):\n"
               "    ret = Valid([args[-1]])"%key)
will = Mast('compile', """
if (signed(alice, signature)):
    # Allow alice to pass in a new txn, not hard coded(ContractTxn)
    ret = Valid([args[-1]])
if (signed([bob and carol], signature)):
    if (args[1] > 3 and args[1] < 10):
        ret = Valid(["output txn doing something specific"])
    #? more conditions
if (date.time.now() > year(100000)):
    ret = Valid(args[-1])
""")

def mkMerkleWill(alice, bob, carol):
    will = mkM("print 'begin'\n")
    will.addBr("if (signed(alice, signature)): ret = Valid([args[-1]])")
    c = will.addBr("if (signed([%r, %r], signature)):\n"%(bob, carol))
    c.addBr("    if (3 < args[0] < 10): ret = Valid([])")
    e = c.addBr("    ret = Valid() if ( 20 < args[0]) else Invalid()")
    will.addBr("if (date.time.now() > year(100000)): ret = Valid(args[-1])")
    return will, e
w, c= mkMerkleWill('1','2','3')
proof = c.generateFullProofUpward(w.hash())
print  "".join([code for _,code,_ in proof[::-1]])

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
