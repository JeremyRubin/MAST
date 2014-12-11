#!/usr/bin/python
import mast.mast as mast
import mast.crypto as crypto

ex = """
def testfn(x, y, z):
    if x > y:
        print x, y, z
    else:
        print %s
"""
if __name__ == "__main__":
    code = list(ex%x for x in xrange(100))
    m = mast.Mast("compile", "print 1")
    for i, c in enumerate(code):
        if i%10000 == 0:
            print '.'
        m.addBr(c)

    mt = mast.MerkleTreeList(m.children)
    
    h = crypto.ishash(mast.crypto.hash(ex%60))
    pl = mt.proofList(h)
    pl_size = sum(len(a)+len(b) for a,b in pl)

    c = crypto.hashable(ex%60)
    compressed_size = 100 - 100*pl_size+len(mt.hash())+len(c.data)
    initial_size = float(sum(len(co) for co in code))

    print "Compression achieved for 100,000 branches"
    print "%f %%" % (compressed_size / initial_size)

    assert mast.prove(pl, [c], mt.hash())






