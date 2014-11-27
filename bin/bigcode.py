#!/usr/bin/python
import mast.mast as mast
ex = """
def testfn(x, y, z):
    if x > y:
        print x, y, z
    else:
        print %s
"""
if __name__ == "__main__":
    code = list(ex%x for x in xrange(100000))
    m = mast.Mast("compile", "print 1")
    for i, c in enumerate(code):
        if i%10000 == 0:
            print '.'
        m.addBr(c)
    mt = mast.MerkleTreeList(m.children)

    
    
    h = mast.ishash(mast.crypto._hash(ex%60))
    pl = mt.proofList(h)

    c = mast.hashable(ex%60)
    print
    print "Compression achieved for 100,000 branches"
    print "%f %%"%(100 - 100*(sum(len(a)+len(b) for a,b in pl)+len(mt.hash())+len(c.data) )/ float(sum(len(co) for co in code)))

    assert mast.prove(pl, c, mt.hash())






