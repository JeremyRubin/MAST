from crypto import *
import crypto
class Mast():

    def __init__(self, mode, content, parent=None, honest=True, addNonces=False, debug=True, leaf=False):
        modes = ["run","compile"]
        if mode not in modes:
            raise ValueError("Mode not in %s "%modes)
        self.mode = mode
        self.content = __Content__(content, mode)
        self.parent = parent
        self.honest = honest
        self.addNonces = addNonces
        self.debug = debug
        self.children = []  #TODO: make this a tree!
        self.leaf = leaf

    #TODO: return new node
    def addBr(self, content, leaf=False):
        if self.leaf:
            raise ValueError("Leaf node cannot have children")
        newBr = Mast(self.mode, content, parent=self, honest=self.honest,addNonces=self.addNonces, debug=self.debug, leaf=leaf)    #create new mast
        self.children.append(newBr)
        return newBr

    def hash(self):
        l = []
        if self.children:
            l.append(MerkleTreeList(self.children))
        l.append(self.content)
        return MerkleTreeList(l).hash()

    # Verifies and executes the code for the current node
    # Returns the next hash in the path
    def execCode(self, code, IO):
        if self.mode != "run":
            raise ValueError("Illegal mode: %s"%self.mode)
        self.content.verifyAdd(code).execute(IO)
        nextHash = IO.getReturn() # assume this is a hash for now
        return nextHash

    # Given the hash for a particular child node and a proofList, adds
    # the child node if the hash's existence can be proven
    # Returns the resulting child node
    def addToChildren(self, childHash, proofList):
        if self.mode != "run":
            raise ValueError("Illegal mode: %s"%self.mode)
        if prove(proofList, childHash, self.content.hash()):
            child = self.addBr(childHash)
            return child
        else:
            raise ValueError("Proof failed on hash: %s"%childHash)

    def expandChild(self):
        pass


    #TODO: make this prettier? Maybe add coloring? Maybe output to a graph viewer?
    def __str__(self):
        return "%s\nMerkle Root:%s\n%s%s"%( str(self.content)
                                          , self.hash()
                                          , "Children:\n" if self.children else ""
                                          , "\n".join(map(lambda x: "\n    ".join(("    "+str(x)).split('\n')), self.children)))

    #TODO: this will be moved
    def construct(self, port=8000, host="localhost"):
        if self.mode == "run":
            pass    #TODO
        else:
            pass    #TODO
def indent(s):
    return "    "+"\n    ".join(s.split('\n'))
class MerkleNode():
    def __init__(self, data, parent=None, c1=None, c2=None):
        self.parent = parent
        self.data = data
        self.c1 = c1
        self.c2 = c2
    def hash(self):
        return self.data.hash()
    def __str__(self):
        return "%s\n%s\n%s"%(str(self.data), indent(str(self.c1)), indent(str(self.c2)))
class MerkleTreeList():
    def __init__(self, items):
        self.items = [MerkleNode(i) for i in items]
        things = list(self.items)
        if len(things) == 0:
            raise ValueError("Cannot Construct Merkle Tree with empty list")
        while things:
            fst = things.pop(0)
            if things:
                snd = things.pop(0)
                p = MerkleNode(crypto.hashable(fst.hash()+snd.hash()), c1=fst, c2=snd)
                snd.parent = p
                fst.parent = p
                things.append(p)
            else:
                self.node = fst
                break
    def __str__(self):
        return str(self.node)
    def hash(self):
        return self.node.hash()
    def proofList(self, item):
        """Provide the minimum set of hashes needed to prove hash's existence"""
        f = MerkleNode(item)
        h = f.hash()
        filt = (filter(lambda x: h == x.hash(), self.items))
        if len(filt) == 0:
            raise ValueError("Not Found")
        else:
            result = []
            f = filt[0]
            while f.parent is not None:
                f = f.parent
                result.append((f.c1.hash(), f.c2.hash()))
            return result
def prove(proofList, data, mroot):
    lastHash = data.hash()
    for c1, c2 in proofList:
        if lastHash not in [c1,c2]:
            return False
        lastHash = crypto.hashable(c1+c2).hash()
    return lastHash == mroot

class __IO__():
    def __init__(self):
        self.history = []
        self.stack = []
        self.returnstack = []
        self.heap = {}
    def push(self, x):
        self.stack.append(x)
        self.history.append(x)
    def pop(self):
        return self.stack.pop()
    def peek(self):
        return self.stack[-1]
    def dup(self):
        self.push(self.peek())
    def setReturn(self, x):
        self.returnstack.push(x)
    def getReturn(self):
        return self.returnstack.pop()
    def __str__(self):
        return """\nStack (Top->Bottom): %s\n
                Heap: %s \n
                Execution History (Top->Bottom): %s\n"""%(", ".join(str(x) for x in self.stack[::-1]), 
                    self.heap, 
                    ", ".join(str(x) for x in self.history[::-1]))

class __Content__():
    """
    Constructs some content following some rules.

    Calling convention:
        All communication should be with a global IO object, which has some special methods
    """
    allowed_type = set([Mast, str])
    def __init__(self, raw, mode):
        self.mode = mode
        if not any(map(lambda x: isinstance(raw, x), __Content__.allowed_type)):
            raise ValueError("Cannot have content of this type")
        if mode == "compile":
            if isinstance(raw, str):
                if not self.syntax_check(raw):
                    raise SyntaxError("Invalid syntax for content: %s"%raw)
                self.compiled = compile(raw, '', 'exec')
            else:
                self.compiled = None
            self.code = raw
            self._hash = crypto.hash(raw)
        if mode == "run":
            self.code = None
            self._hash = raw
    def verifyAdd(self, s):
        if self.code == None:
            if crypto.verify(s, self._hash):
                self.compiled = compile(s, '', 'exec')
                self.code = s
                return self
            else:
                raise ValueError("Verification failed, string '%s' did not match hash %s"%(s, self._hash))
        else:
            raise Exception("Code already loaded into object")
    def execute(self, IO=None):
        if IO is None:
            IO = __IO__()
        if self.compiled:
            exec(self.compiled)
    def syntax_check(self, s):
        """ TODO: If any syntax checking/ast transforms are desired..."""
        return True
    def hash(self):
        return self._hash
    def __str__(self):
        return "Hash: %s\nMode:%s\nCode:\n\"\"\"\n%s\n\"\"\""%(self.hash(),self.mode, self.code)
def testPhase(s):

    print "#"*(len(s)+12)
    print "#     %s     #"%s
    print "#"*(len(s)+12)
if __name__ == "__main__":
    testPhase("Verifying Content Behavior")
    IO = __IO__()
    IO.push(10)
    IO.push(100)
    IO.heap[1] = 100
    print "Verifying Content Execution"
    __Content__(crypto.hash("IO.heap[100] = 10"), 'run').verifyAdd("IO.heap[100] = 10").execute(IO)
    assert IO.heap[100] == 10
    print "...Content Executed"
    print "Verifying bad Content Rejection"
    try:
        __Content__("Fail", 'run').verifyAdd("IO.heap[100] = 10").execute(IO)
        raise Exception("Should have failed to verifyAdd")
    except ValueError:
        print "... Bad Content Rejected"
    a = Mast('compile', "print 10")
    a.addBr('print 10').addBr('print 100')
    b = a.addBr('print 10').addBr('print 100')
    b.addBr('print 1000')
    b.addBr('print 1')
    testPhase("Printing Tree from MAST")
    print a
    testPhase("Printing Merkle Proof List")
    a = MerkleTreeList(map(crypto.hashable, xrange(1024)))
    print a
    testPhase("Testing Merkle Proof List")
    pl = a.proofList(crypto.hashable(3))
    assert len(pl)==10
    print "...Proof list is log2(n_elems) long"
    assert prove(pl, crypto.hashable(3), a.hash())
    print "...proof 1 passed, positive"
    pl[2] = ("bad","bad")
    assert not prove(pl, crypto.hashable(3), a.hash())
    print "...proof 2 passed, negative"
