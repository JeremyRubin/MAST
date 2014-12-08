#!/usr/bin/python
import mast.mast as mast
import mast.crypto as crypto
from pprint import pprint
ex = """
def testfn(x, y, z):
    if x > y:
        print x, y, z
    else:
        print %s
"""
if __name__ == "__main__":
    code = list(ex%x for x in xrange(20))
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
    print mast.Mast.upwardProve(pr)






