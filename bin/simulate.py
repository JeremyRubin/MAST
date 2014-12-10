from mast.sim import *
from mast.mast import *
from mast.nodes import *
from pprint import pprint as pretty
import sys
def mkM(s, ic=None):
    return Mast('compile', s, initialChildren=ic)
def normal(key):
    m = mkM('')
    return m, m.addBr("if (signed([%r], sig)):\n"
                      "    ret = Valid(args[-1])"%key)
def mkMerkleWill(alice, bob, carol):
    nbob = normal(bob)
    ncarol = normal(carol)
    will = mkM("ret=10\n")
    will.addBr("if (signed([%r], sig)): ret = Valid([args[-1]])"%alice)
    c = will.addBr("if (signed([%r, %r], sig)):\n"%(bob, carol))
    btwn = c.addBr("""    ret = Valid([(%r,args[0]), (%r, amnt-args[0])]) if (3 < args[0] < 10) else Invalid()"""%(nbob, ncarol))
    gt20 = c.addBr("""    ret = Valid([(%r, amnt/2 + amnt%%2),(%r, amnt/2)]) if ( 20 < args[0]) else Invalid()"""%(nbob, ncarol))
    time = will.addBr("if (dt.now() > dt(2013,1,1)) and (signed([%r]) or signed([%r])): ret = Valid(args[-1])"%(bob, carol))
    return will, time, gt20, btwn

if __name__ == "__main__":
    """
    #generate will
    w, time, gt20, btwn= mkMerkleWill('1','2','3')
    proof = gt20.generateFullProofUpward(w.hash())
    print upwardProve(proof, w.hash())

    print "".join(code for _, code, _ in proof[::-1])
    print merkleVerifyExec({'h':crypto.hash("".join(map(str,[1,2,3]))), 's':["a", "b", "c"]}, w.hash(), [1,2,3,proof], 199)
    """
    # init users
    signatories = [Signatory(str(i)) for i in range(100)]

    #initialize txn
    inittxn = map(lambda x: Txn(normal(x.pubKey)[0].hash(), 100), signatories)

    GlobalConsensus.init(inittxn)
    #initialize txnstream

    m, time, gt20, btwn = mkMerkleWill(signatories[0].pubKey, signatories[30].pubKey,signatories[5].pubKey)
    top, bot = normal(signatories[0].pubKey)
    proof = bot.generateFullProofUpward(top.hash())
    print "".join(code for _, code, _ in proof[::-1])
    args = [[(m.hash(), 100)],proof]
    sig = crypto.hash("".join(map(str, args)))
    args.append(SignedHash(sig, signatories[0].pubKey))
    txnstream = [[   (inittxn[0], args)     ]]
    # TODO: Generate a txn stream which is a list of simulation frames of txns
    # TODO: Verify behavior
    # TODO: Make interesting output for demo
    # Make Nodes
    goodNodes = [GoodNode() for x in xrange(100)] 
    badNodes = [EvilNode() for x in xrange(10)]
    inconsistentNodes = [InconsistentNode() for x in xrange(20)]
    nodes = inconsistentNodes + badNodes + goodNodes
    for txnSet in txnstream:
        for (txn, args) in txnSet:
            [n.receive(txn, args) for n in nodes]
        [n.tick() for n in nodes]
        GlobalConsensus.consensus_tick(nodes)
    GlobalConsensus.consensus_tick(goodNodes)
