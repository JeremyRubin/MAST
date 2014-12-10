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

    
    print len("".join(code))*101*10
    pr = n.generateFullProofUpward(m.hash())
    print len(str(pr))
    print sim.merkleVerify(None, m.hash(), [pr])






