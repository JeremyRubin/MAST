#!/usr/bin/python
import mast.mast as mast
import mast.crypto as crypto
import mast.sim as sim
import mast.script as script
from pprint import pprint
from base64 import b64encode as enc

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
    orig_len = float(len("".join(code))*101)
    print "original length", orig_len
    pr = n.generateFullProofUpward(m.hash())
    code, _script = mast.toScript(pr, m.hash())
    together = enc("".join(map(chr,code+_script)))
    comp_len = len(str(pr))
    pct_comp = 1 - comp_len/orig_len
    print sim.merkleVerifyExec(None, m.hash(), [pr], 10)
    print script.run("".join(map(chr,code+_script)))
    print orig_len
    print "compression length", comp_len
    print "compression length for blockchain ready version", len(together)
    print "compression percentage", pct_comp
    print "compression percentage for blockchain version", 1-len(together)/orig_len
