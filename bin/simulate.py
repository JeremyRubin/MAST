from mast.sim import *
from mast.mast import *
from mast.nodes import *
from pprint import pprint as pretty
def mkM(s, ic=None):
    return Mast('compile', s, initialChildren=ic)
def normal(key):
    return mkM("if (signed(%r, sig)):\n"
               "    ret = Valid([args[-1]])"%key)
def mkMerkleWill(alice, bob, carol):
    will = mkM("ret=10\n")
    will.addBr("if (signed(%r, sig)): ret = Valid([args[-1]])"%alice)
    c = will.addBr("if (signed([%r, %r], sig)):\n"%(bob, carol))
    btwn = c.addBr("    ret = Valid([]) if (3 < args[0] < 10) else Invalid()")
    gt20 = c.addBr("    ret = Valid() if ( 20 < args[0]) else Invalid()")
    time = will.addBr("if (dt.now() > dt(2013,0,0)) and (signed([%r]) or signed([%r])): ret = Valid(args[-1])"%(bob, carol))
    return will, time, gt20, btwn

if __name__ == "__main__":

    #generate will
    w, time, gt20, btwn= mkMerkleWill('1','2','3')
    proof = gt20.generateFullProofUpward(w.hash())
    print upwardProve(proof, w.hash())

    print "".join(code for _, code, _ in proof[::-1])
    print merkleVerifyExec({'h':crypto.hash("".join(map(str,[1,2,3]))), 's':["a", "b", "c"]}, w.hash(), [1,2,3,proof])
    #initialize txnstream
    txnstream = []
    # TODO: Finish writing the will
    # TODO: Generate a txn stream which is a list of simulation frames of txns
    # TODO: Generate a set of signatories
    # TODO: Genrate an initial state of TXN's (GlobalConsensus init) for the signatories 
    # TODO: Verify behavior
    # TODO: Make interesting output for demo
    # Make Nodes
    goodNodes = [GoodNode() for x in xrange(100)] 
    badNodes = [EvilNode() for x in xrange(10)]
    inconsistentNodes = [InconsistentNode() for x in xrange(20)]
    nodes = inconsistentNodes + badNodes + goodNodes
    for txnSet in txnstream:
        for txn in txnSet:
            [n.receive(txn) for n in nodes]
        [n.tick() for n in nodes]
        GlobalConsensus.consensus_tick(nodes)
    GlobalConsensus.consensus_tick(goodNodes)
