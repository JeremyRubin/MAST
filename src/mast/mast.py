from crypto import *
import crypto
class Mast():

    def __init__(self, mode, content, parent=None, honest=True, addNonces=True, debug=True, leaf=False):
        modes = ["run","compile"]
        if mode not in modes:
            raise ValueError("Mode not in %s "%modes)
        self.mode = mode
        self.content = __Content__(content, mode)
        self.parent = parent
        self.honest = honest
        self.addNonces = addNonces
        self.debug = debug
        self.children = set()
        self.leaf = leaf

    #TODO: return new node
    def addBr(self, content, hash=None, leaf=False):
        newBr = None    #create new mast
        if self.mode == "compile":
            if self.leaf:
                raise ValueError("Leaf node cannot have children")
            if isInstance(content.raw, Mast):
                pass    #TODO
            elif isInstance(content.raw, str):
                pass    #TODO
            else:
                raise ValueError("Illegal content type: %s"%str(content))
            return newBr

        else:   #TODO: All different    
            return newBr

    #TODO: make this pretty
    def __str__(self):
        pass

    #TODO: this will be moved
    def construct(self, port=8000, host="localhost"):
        if self.mode == "run":
            pass    #TODO
        else:
            pass    #TODO
class __Content__():
    allowed_type = set([Mast, str])
    def __init__(self, raw, mode):
        self.mode = mode
        if not any(map(lambda x: isInstance(raw, x), allowed_type)):
            raise ValueError("Cannot have content of this type")
        if mode == "compile" and isIntance(raw, str) and not self.syntax_check(raw):
            raise SyntaxError("Invalid syntax for content: %s"%raw)
        if mode == "compile":
            self._raw = raw #TODO: Syntax checking
            self.hash = _hash(raw)   #TODO: syntax check content
        if mode == "run":
            self._raw = None
            self.hash = raw
    #TODO: Make this real
    def verify(s):
        if self._raw == None and crypto.verify(s, self.hash):
            self._raw = s
         #   return s #TODO: Maybe not?
        #else:
         #   raise ValueError("Verification failed, string '%s' did not match hash %s"%(s, self.hash) # TODO: What here?
    def exec():
        if self._raw:
            pass #TODO: Exec raw
    def syntax_check(self, s):
        return True
