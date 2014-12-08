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
    code = list(ex%x for x in xrange(10))
    m = mast.Mast("compile", "print 1")
    n = m
    for i, c in enumerate(code):
        if i%10000 == 0:
            print '.'
        n.addBr(c)
        n.addBr(c)
        n = n.addBr(c)
    mt = mast.MerkleTreeList(m.children)

    
    
    pprint(n.generateFullProofUpward(m.hash()))
    print mast.Mast.upwardProve(n.generateFullProofUpward(m.hash()))






