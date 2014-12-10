from mast.sim import *
from mast.mast import *
from mast.nodes import *
from pprint import pprint as pretty
import sys
import copy
def mkM(s, ic=None):
    return Mast('compile', s, initialChildren=ic)
def normal(key):
    m = mkM('')
    return m, m.addBr("if (signed([%r], sig)):\n"
                      "    ret = Valid(args[-1])"%key)

def normalS(key):
    return ("if (signed([%r], sig)):\n"
                      "    ret = Valid(args[-1])"%key)
def mkMerkleWill(alice, bob, carol):
    nbob = normalS(bob)
    ncarol = normalS(carol)
    will = mkM("ret=10\n")
    will.addBr("if (signed([%r], sig)): ret = Valid([args[-1]])"%alice)
    c = will.addBr("if (signed([%r, %r], sig)):\n"%(bob, carol))
    btwn = c.addBr("""    ret = Valid([(%r,args[0]), (%r, amt-args[0])]) if (3 < args[0] < 10) else Invalid()"""%(nbob, ncarol))
    gt20 = c.addBr("""    ret = Valid([(%r, amt/2 + amt%%2),(%r, amt/2)]) if ( 20 < args[0]) else Invalid()"""%(nbob, ncarol))
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

    proof2 = gt20.generateFullProofUpward(m.hash())
    argsSpend = [21, proof2]
    sig = crypto.hashArr(argsSpend)
    argsSpend.append(SignedHash(sig, signatories[5].pubKey).sign(signatories[30].pubKey))


    txnstream = [[   (inittxn[0], args)     ], [ (Txn(m.hash(), 100), argsSpend) ]]
    # TODO: Make interesting output for demo
    # Make Nodes
    goodNodes = [GoodNode() for x in xrange(100)] 
    badNodes = [EvilNode() for x in xrange(10)]
    inconsistentNodes = [InconsistentNode() for x in xrange(20)]
    nodes = inconsistentNodes + badNodes + goodNodes
    print
    print "RUN SIMULATION"
    raw_input()
    for txnSet in txnstream:
        for (txn, args) in txnSet:
            [n.receive(txn, copy.deepcopy(args)) for n in nodes]
        [n.tick() for n in nodes]
        GlobalConsensus.consensus_tick(nodes)
    print
    print "PROCESS COMPLETE"
    print
    pretty(map(lambda z: map(lambda y: y.nextTxn(), filter(lambda x: x.args is not None, z)), GlobalConsensus.ledger.ledger))
    print 
    print m.hash()

