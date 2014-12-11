#!/usr/bin/python
import mast.mast as mast
import mast.crypto as crypto
import decimal as dec

ex = """
def testfn(x, y, z):
    if x > y:
        print x, y, z
    else:
        print %s
"""
N= 100000
if __name__ == "__main__":
    code = list(ex%x for x in xrange(N))
    m = mast.Mast("compile", "print 1")
    bot = None
    for i, c in enumerate(code):
        if i%10000 == 0:
            print '.',
        bot = m.addBr(c)
    print
    print "Generating Hash"
    mh = m.hash()
    print "Hash is", mh
    proof = bot.generateFullProofUpward(mh)
    c = crypto.hashable(ex%60)
    dec.getcontext().prec = 30
    compressed_size = dec.Decimal(len(str(proof)))

    initial_size = dec.Decimal(N*sum(map(len,code)))
    print "Compression achieved for %d branches"%N
    rate = dec.Decimal(1) - (compressed_size / initial_size)
    print rate
    print "%s %%" %rate
    assert mast.upwardProve(proof, mh)






