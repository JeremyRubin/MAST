from mast.sim import *
from mast.mast import *
import mast.script
from mast.nodes import *
from pprint import pprint as pretty
import sys
import copy
def mkM(s, ic=None, debug=True):
    return Mast('compile', s, initialChildren=ic, debug=True)
def normal(key):
    m = mkM('#NORMAL TXN\n')
    return m, m.addBr("if (signed([%r], sig)):\n"
                      "    ret = Valid(args[-1])"%key)

def normalS(key):
    return ("if (signed([%r], sig)):\n"
                      "    ret = Valid(args[-1])"%key)
def pause(msg, p=True, p1 = False):

    if p: raw_input()
    print (len(msg)+60)*"#"
    print 10*"#",20*" ",msg, 16*" ", 10*"#"
    print (len(msg)+60)*"#"
    if p1: raw_input()
    print
def mkMerkleWill(alice, bob, carol, debug=True):
    nbob = normalS(bob)
    ncarol = normalS(carol)
    will = mkM("#WILL TYPE TXN\n", debug=True)
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
    pause("Welcome to bitsim", False)
    m, time, gt20, btwn = mkMerkleWill(signatories[0].pubKey, signatories[30].pubKey,signatories[5].pubKey)
    top, bot = normal(signatories[0].pubKey)
    proof = bot.generateFullProofUpward(top.hash())
    print "CONTRACT 1"
    print """

def normal(key):
    m = mkM('#NORMAL TXN')
    return m, m.addBr("if (signed([%r], sig)): ret = Valid(args[-1])"%key)


    """
    pretty(proof[::-1])
    print
    print
    print "".join(proof[1][::-1])
    print
    print

    args = [[(m.hash(), 100)],proof]
    sig = crypto.hash("".join(map(str, args)))
    args.append(SignedHash(sig, signatories[0].pubKey))
    print "How to spend?"
    pretty(args)
    print
    pause("CONTRACT 2")
    proof2 = gt20.generateFullProofUpward(m.hash())
    parts = toScript(proof2, m.hash())
    print run("".join(map(chr,chain(parts[0],parts[1]))))
    sys.exit()
    pause('DOING COOL SHIT ^^^', True, True)

    print """

def mkMerkleWill(alice, bob, carol):
    nbob = normalS(bob)
    ncarol = normalS(carol)
    will = mkM("#WILL TYPE TXN")
    will.addBr("if (signed([%r], sig)): ret = Valid([args[-1]])"%alice)
    c = will.addBr("if (signed([%r, %r], sig)):"%(bob, carol))
    btwn = c.addBr(\"""    ret = Valid([(%r,args[0]), (%r, amt-args[0])]) if (3 < args[0] < 10) else Invalid()\"""%(nbob, ncarol))
    gt20 = c.addBr(\"""    ret = Valid([(%r, amt/2 + amt%%2),(%r, amt/2)]) if ( 20 < args[0]) else Invalid()\"""%(nbob, ncarol))
    time = will.addBr("if (dt.now() > dt(2013,1,1)) and (signed([%r]) or signed([%r])): ret = Valid(args[-1])"%(bob, carol))
    return will, time, gt20, btwn


"""
    pretty(proof2[::-1])
    print
    print "***ID of this TXN:", m.hash(), "***"
    print
    print "".join(proof2[1][::-1])
    argsSpend = [21, proof2]
    sig = crypto.hashArr(argsSpend)
    argsSpend.append(SignedHash(sig, signatories[5].pubKey).sign(signatories[30].pubKey))


    txnstream = [[   (inittxn[0], args)     ], [ (Txn(m.hash(), 100), argsSpend) ]]
    # TODO: Make interesting output for demo
    # Make Nodes
    const = lambda x: lambda c: x()
    goodNodes = map(const(GoodNode),xrange(100))
    badNodes = map(const(EvilNode),xrange(10))
    inconsistentNodes = map(const(InconsistentNode), xrange(20))
    nodes = inconsistentNodes + badNodes + goodNodes
    pause("RUN SIMULATION", False, True)
    for txnSet in txnstream:
        for (txn, args) in txnSet:
            [n.receive(txn, copy.deepcopy(args)) for n in nodes]
        [n.tick(debug=True) for n in nodes]
        GlobalConsensus.consensus_tick(nodes)
    print
    pause("PROCESS COMPLETE")
    print
    pretty(map(lambda z: map(lambda y: y.nextTxn(), filter(lambda x: x.args is not None, z)), GlobalConsensus.ledger.ledger))
    print 

