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
    def execute(self, state):
        if self.compiled:
            exec(self.compiled)
    def syntax_check(self, s):
        return True
    def hash(self):
        return self._hash
if __name__ == "__main__":
    state = {'1':10}
    __Content__("print state['1']\nstate[10] = 100\n", 'compile').execute(state)
    print state
    __Content__(crypto._hash("state[100] = 10"), 'run').verifyAdd("state[100] = 10").execute(state)
    print state
    try:
        __Content__("Fail", 'run').verifyAdd("state[100] = 10").execute(state)
        raise Exception("Should have failed to verifyAdd")
    except ValueError:
        print "verifyAdd as planned!"
