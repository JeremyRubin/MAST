#!/usr/bin/python
import mast.mast as mast
import mast.crypto as crypto
import mast.sim as sim
from pprint import pprint


ex = lambda x: """
def testfn(x, y, z):
    if x > y:
        print x, y, z
    else:
        print %s
ret = Valid("print 1")
"""%(x)
if __name__ == "__main__":
    code = map(ex, xrange(20)) 
    m = mast.Mast("compile", "print 1")
    n = m
    for i, c in enumerate(code):
        if i%10000 == 0:
            print '.'
        for i in xrange(100):
            n.addBr(c)
        n = n.addBr(c)
    mt = mast.MerkleTreeList(m.children)

    orig_len = len("".join(code))*101*10.0
    print "original length", orig_len
    pr = n.generateFullProofUpward(m.hash())
    comp_len = len(str(pr))
    pct_comp = 1 - orig_len/comp_len
    print "compression length", comp_len
    print "compression percentage", pct_comp
    print sim.merkleVerifyExec(None, m.hash(), [pr])
