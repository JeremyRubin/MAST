#!/usr/bin/python
import mast.mast as mast
prelude = """
IO = mast.__IO__()
def execTxn(txn):
    print txn
def getSig(txn):
    return txn
def checkSig(sig):
    return sig == "abcd"
"""
A_0 = """
import datetime
IO.push(datetime.datetime.now())
"""
A = """
if IO.peek() > datetime.datetime(2014, 11, 27, 2, 22, 14, 135182):
    print "unlocked"
    execTxn("baloney")
"""
B_0 = """
IO.push('abcd')
IO.dup()
"""
B_1 = """ 
IO.push(getSig(IO.pop()))
"""
B = """
if checkSig(IO.pop()):
    print "unlocked"
    execTxn(IO.pop())
"""
startup = """print "mast begin" """
if __name__ == "__main__":
    exec(prelude)
    exec(A_0)
    exec(A)
    exec(B_0)
    exec(B_1)
    exec(B)
    m = mast.Mast("compile", startup)
    m.addBr(B_0).addBr(B_1).addBr(B)
    m.addBr(A_0).addBr(A)

else:
    raise Exception("Not Importable")
