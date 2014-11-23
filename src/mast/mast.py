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
        child_hash = [child.hash() for child in self.children]
        while child_hash:
            c1 = child_hash.pop(0)
            if child_hash:
                c2 = child_hash.pop(0)
                root = crypto._hash(c1+c2)
                child_hash.append(root)
            else:
                return crypto._hash(self.content.hash()+c1)
        return self.content.hash()

    #given string code and all children, build branches 
    #and decide which to traverse on
    def execBr(self, hash):
        if self.mode != "run":
            raise ValueError("Illegal mode: %s")
        else:   #TODO: execute down a given branch(from client side only)
            pass

    #Move this to its own iterator
    def initTraversal(self):
        pass    #store some current branch, can move this to a separate class

    #given current branch, return next branch(or all its children?)
    def getNextBr(self, content):
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
class __IO__():
    def __init__(self):
        self.stack = []
        self.returnstack = []
        self.heap = {}
    def push(self, x):
        self.stack.append(x)
    def pop(self):
        return self.stack.pop()
    def setReturn(self, x):
        self.returnstack.push(x)
    def getReturn(self):
        return self.returnstack.pop()
    def __str__(self):
        return """
        Stack (Top->Bottom): %s
        Heap: %s
        """%(", ".join(str(x) for x in self.stack[::-1]), self.heap)

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
            self._hash = crypto._hash(raw)
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
if __name__ == "__main__":
    a =     __Content__("print IO.heap[1]\nIO.heap[10] = 100\n", 'compile')
    print a
    IO = __IO__()
    IO.push(10)
    IO.push(100)
    IO.heap[1] = 100
    a.execute(IO)
    print IO
    __Content__(crypto._hash("IO.heap[100] = 10"), 'run').verifyAdd("IO.heap[100] = 10").execute(IO)
    print IO
    try:
        __Content__("Fail", 'run').verifyAdd("IO.heap[100] = 10").execute(IO)
        raise Exception("Should have failed to verifyAdd")
    except ValueError:
        print "verifyAdd as planned!"
    a = Mast('compile', "print 10")
    a.addBr('print 10').addBr('print 100')
    b = a.addBr('print 10').addBr('print 100')
    b.addBr('print 1000')
    b.addBr('print 1')
    print a
