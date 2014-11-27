#!/usr/bin/python
import mast.mast as mast
class Contract:
    def __init__(self, name, date, purpose):
        self.name = name
        self.date = date
        self.purpose = purpose
    def render(self):
        pass
A = """
class Alpha(Contract):
    def render(self):
        return "On %s, %s was sent to %s"%(self.date, self.name, self.purpose)
"""

B = """
class Alpha(Contract):
    def render(self):
        return "On redacted, %s was sent to %s"%( self.name, self.purpose)
"""
startup = """print "mast begin" """
com = "print Alpha(1,2,3).render()"
if __name__ == "__main__":
    exec(A)
    print Alpha(1, 2, 3).render()
    exec(B)
    print Alpha(1, 2, 3).render()
    m = mast.Mast("compile", startup)
    m.addBr(B).addBr(com)
    m.addBr(A).addBr(com)
    print m
    m2 = mast.Mast("run", m.hash()) 
    print m2

else:
    raise Exception("Not Importable")
