from crypto import *
import base64
from script import *
import crypto
import io
from io import *
from pprint import pprint as pretty
from collections import deque
from itertools import *
def indent(s):
    return "    "+"\n    ".join(s.split('\n'))
class MerkleNode():
    def __init__(self, data, parent=None, c1=None, c2=None):
        self.parent = parent
        self.data = data
        self.c1 = c1
        self.c2 = c2
        self.__cached_hash__ = self.data.hash()
    def hash(self):
        return self.__cached_hash__
    def __str__(self):
        return "%s\n%s\n%s"%(str(self.data), indent(str(self.c1)), indent(str(self.c2)))
class MerkleTreeList():
    def __init__(self, items):
        self.items = map(MerkleNode, items)
        things = deque(self.items)
        if len(things) == 0:
            raise ValueError("Cannot Construct Merkle Tree with empty list")
        while True:
            fst = things.popleft()
            if things:
                snd = things.popleft()
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
class Mast():

    def __init__(self, mode, content, parent=None, initialChildren=None, honest=True, addNonces=False, debug=True, leaf=False):
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
        if initialChildren:
            map(self.addBr, initialChildren)
        self.changed = True
        self.__cached_hash__ = self.hash()

    #TODO: return new node
    def addBr(self, content, leaf=False):
        if self.leaf:
            raise ValueError("Leaf node cannot have children")
        newBr = Mast(self.mode, content, parent=self, honest=self.honest,addNonces=self.addNonces, debug=self.debug, leaf=leaf)    #create new mast
        self.children.append(newBr)
        self.changed=True
        return newBr

    def batch_addBr(self, contents, leaf=False):
        if self.leaf:
            raise ValueError("Leaf node cannot have children")
        self.changed = True
        newBr = map(lambda c: Mast(self.mode, c, parent=self, honest=self.honest,addNonces=self.addNonces, debug=self.debug, leaf=leaf), contents)
        self.children.extend(newBr)
        return newBr
    def hash(self):
        if self.changed:
            if self.children:
                self.__cached_hash__ = MerkleTreeList([MerkleTreeList(self.children), self.content]).hash()
            else:
                self.__cached_hash__ = MerkleTreeList([self.content]).hash()
        return self.__cached_hash__

    def childrenHash(self):
        return MerkleTreeList(self.children).hash()
    # RUN-SIDE EXECUTION METHODS

    # Calling convention:
    # nextHash = IO.getReturn()
    # client sends nextHash to server
    # server sends back (code, proofList)
    # client: child = execBr(nextHash, code, proofList, IO)
    
    # Wrapper function to be called by client for execution
    # Verifies that nextHash (returned from previous execution) is valid
    # Creates new child node if hash can be verified
    # Adds code content to the child node and executes it
    def executeBr(self, childCode, proofList, IO):
        if self.mode != "run":
            raise ValueError("Illegal mode: %s"%self.mode)
        nextHash = IO.getReturn()
        child = self.__addToChildren(nextHash, proofList)
        childCodeHash = proofList[-1][1] # get the hash of the code from proofList
        child.__execCode(self, childCode, childCodeHash, IO)
        return child

    # Given the hash for a particular child node and a proofList, adds
    # the child node if the hash's existence can be proven
    # Returns the resulting child node whose content is childHash
    def __addToChildren(self, childHash, proofList):
        if self.mode != "run":
            raise ValueError("Illegal mode: %s"%self.mode)
        if prove(proofList, childHash, self.content.hash()):
            child = self.addBr(childHash)
            return child
        else:
            raise ValueError("Proof failed on hash: %s"%childHash)

    # Executes the code for the current node if it matches the given codeHash
    # Returns the next hash in the path
    def __execCode(self, code, codeHash, IO):
        if self.mode != "run":
            raise ValueError("Illegal mode: %s"%self.mode)
        # Make new Content for verification/execution, don't save the code locally
        codeContent = __Content__(codeHash, self.mode)
        codeContent.verifyAdd(code).execute(IO)
        nextHash = IO.getReturn() # this is the hash of the next MAST child
        return nextHash

    # COMPILE-SIDE EXECUTION METHODS

    # Wrapper function to be called by server
    # Finds the node corresponding the given hash amongst its direct children
    # Returns the child node (for server pointer updates), child code content,
    #   and a proofList that verifies the existence of the child hash
    def searchChildren(self, hash):
        if self.mode != "compile":
            raise ValueError("Illegal mode: %s"%self.mode)
        child = self.__getChildByHash(hash)
        code = child.content.code
        proofList = self.__getChildProofList(child)
        return child, code, proofList

    # Searches for child node by the given hash
    def __getChildByHash(self, h):
        if self.mode != "compile":
            raise ValueError("Illegal mode: %s"%self.mode)
        for child in self.children:
            if child.hash() == h:
                return child
        raise ValueError("Hash not found: %s"%h)

    # Generates proof list for existence of a child node
    # Appends proof list from children Merkle tree with (childrenTree.hash, self.content.hash())
    # This connects the proof list to the current node
    def __getChildProofList(self, childHash):
        if self.mode != "compile":
            raise ValueError("Illegal mode: %s"%self.mode)
        if not self.children:
            raise ValueError("Cannot get child proof list on leaf node")
        #Get proof list of the children Merkle tree
        childrenTree = MerkleTreeList(self.children)
        childrenProof = childrenTree.proofList(crypto.ishash(childHash))
        # Get proof list for existence of children Merkle tree from current node
        curNodeProof = [(childrenTree.hash(), self.content.hash())]
        return childrenProof + curNodeProof
    # Given the parent's merkle root, crawl up the tree generating
    # a Proof List which contains all of the code path
    def generateFullProofUpward(self, merkleRoot):
        if self.mode != "compile":
            raise ValueError("Illegal mode: %s"%self.mode)
        proofs = []
        parent = self.parent
        child = self
        pl = []
        data = []
        while parent.hash() != merkleRoot:
            pl.extend(parent.__getChildProofList(child.hash()))
            data.append(child.content.code)
            child = parent
            parent = parent.parent
            if parent == None:
                return None
        mroot = parent.hash()
        pl.extend(parent.__getChildProofList(child.hash()))
        data.append(child.content.code)
        data.append(parent.content.code)
        return (pl, data, mroot)
    #TODO: make this prettier? Maybe add coloring? Maybe output to a graph viewer?
    def __str__(self):
        return "%s\nMerkle Root:%s\n%s%s"%( str(self.content)
                                          , self.hash()
                                          , "Children:\n" if self.children else ""
                                          , "\n".join(map(lambda x: "\n    ".join(("    "+str(x)).split('\n')), self.children)))


def prove(proofList, data, mroot, debug=False):
    if debug:
        print
        print "---- Prove Root"
        print "mr = ", mroot
        print
    lastHash = proofList[0][0]
    dataQ = deque(data)
    for c1, c2 in proofList:
        if debug:
            print "PROVE:", lastHash
            print "HASHES:", c1, c2
            print "HASH TO:", crypto.hashable(c1+c2).hash()
            print
        if lastHash not in [c1,c2]:
            return False
        if dataQ and dataQ[0].hash() in [c1,c2]:
            dataQ.popleft()
        lastHash = crypto.hashable(c1+c2).hash()
    if debug:
        print "FINAL HASH:", lastHash, lastHash ==mroot
        print
    return (not dataQ) and lastHash == mroot

# Given a megaproof from generateFullProofUpward,
# Verify all of the content is correct and everying can be proved
def upwardProve((proofList, data, mroot), megaroot, debug=False):
    if debug:
        print
        print "##################"
        print "###Begin Proof####"
        print "##################"
    # THe map hashable is critical as data gets popped
    if not prove(proofList, map(hashable,data[:-1]), mroot, debug=debug):
        return False
    l = proofList[-1] # TODO is there a reason this can't just go into prove?
    return crypto.hashable(l[0]+l[1]).hash() == megaroot and hashable(data[-1]).hash() in l[-1]
def toScript((pl, data, mroot), megaroot):
     dataQ = deque(data[1:])
     code = putStr(data[0])
     code.extend([OP_DUP, OP_TOALTSTACK, OP_SHA256, OP_NOP, OP_NOP])
     lastHash = hashable(data[0]).hash()
     b = base64.b64encode
     for i, (c1, c2) in enumerate(pl):
         h = hashable(dataQ[0]).hash() if dataQ else None
         print map(base64.b64encode,[c1, c2, lastHash])
         if dataQ and h in [c1,c2]:
             d = dataQ.popleft()
             if hashable(d).hash() == c1:
                 code.extend(putStr(c1))
                 code.extend(putStr(d))
                 code.extend([OP_2DUP, OP_SHA256, OP_EQUALVERIFY, OP_DROP, OP_TOALTSTACK])
                 code.extend(putStr(c2))
                 code.extend([OP_ROT, OP_OVER, OP_EQUALVERIFY, OP_DROP, OP_CAT,OP_SHA256]) 
             elif hashable(d).hash() == c2:
                 print
                 print b(c2), b(c1), b(hashable(d).hash())
                 print
                 code.extend(putStr(c1))
                 code.extend([OP_2DUP, OP_EQUALVERIFY, OP_DROP])
                 code.extend(putStr(c2))
                 code.extend(putStr(d))
                 code.extend([OP_2DUP, OP_SHA256, OP_EQUALVERIFY, OP_DROP, OP_TOALTSTACK, OP_CAT,OP_SHA256]) 
                 # l, c1
                 # l, c1, l, c1
                 # l, c1, eq
                 # l, c1
                 # l, c1, c2
                 # l, c1, c2, d
                 # l, c1, c2, d, c2, d
                 # l, c1, c2, d, c2, h(d)
                 # l, c1, c2, d, eq
                 # l, c1, c2, d
                 # l, c1, c2, d
             else:
                 print c1, c2, d, hashable(d).hash()
                 raise ValueError()
         else:
             if lastHash == c1:
                 print
                 print b(c2), b(c1), b(lastHash)
                 print
                 code.extend(putStr(c1))
                 code.extend([OP_DUP, OP_ROT, OP_EQUALVERIFY, OP_DROP])
                 code.extend(putStr(c2))
                 code.extend([OP_CAT,OP_SHA256])
             elif lastHash == c2:
                 print
                 print b(c2), b(c1), b(lastHash)
                 print
                 code.extend(putStr(c1))
                 code.extend(putStr(c2))
                 code.extend([OP_ROT,OP_OVER, OP_EQUALVERIFY, OP_DROP, OP_CAT,OP_SHA256])
                 # l
                 # l, c1
                 # l, c1, c2
                 # c1, c2, l
                 # c1, c2, l, c2
                 # c1, c2, l, c2
             else:
                 print c1, c2, base64.b64encode(lastHash)
                 raise ValueError()
         lastHash = hashable(c1+c2).hash()
     script = []
     script = [OP_SHA256]
     script.extend(putStr(hashable(megaroot).hash()))
     script.extend([OP_EQUALVERIFY])
     print b(hashable(c1+c2).hash())
     print b(megaroot)
     return code, script



class __Content__():
    """
    Constructs some content following some rules.

    Calling convention:
        All communication should be with a global IO object, which has some special methods
    """
    allowed_type = set([str, Mast])
    def __init__(self, raw, mode):
        self.mode = mode
        if not any(map(lambda x: isinstance(raw, x), __Content__.allowed_type)):
            raise ValueError("Cannot have content of this type")
        if mode == "compile":
            self.code = raw
            if isinstance(raw,str):
                self._hash = hashable(raw).hash()
            else:
                self._hash = raw.hash()
        if mode == "run":
            self.code = None
            self._hash = raw
    def verifyAdd(self, s):
        if self.code == None:
            if crypto.verify(s, self._hash):
                self.code = s
                return self
            else:
                raise ValueError("Verification failed, string '%s' did not match hash %s"%(s, self._hash))
        else:
            raise Exception("Code already loaded into object")
    def execute(self, IO=None):
        if IO is None:
            IO = __IO__()
        if self.code:
            exec(self.code)
    def syntax_check(self, s):
        """ TODO: If any syntax checking/ast transforms are desired..."""
        return True
    def hash(self):
        return self._hash
    def __str__(self):
        return "Hash: %s\nMode:%s\nCode:\n\"\"\"\n%s\n\"\"\""%(self.hash().encode('hex'),self.mode, self.code)
def testPhase(s):

    print "#"*(len(s)+12)
    print "#     %s     #"%s
    print "#"*(len(s)+12)
if __name__ == "__main__":
    testPhase("Verifying Content Behavior")
    IO = io.__IO__()
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
    assert prove(pl, [crypto.hashable(3)], a.hash())
    print "...proof 1 passed, positive"
    pl[2] = ("bad","bad")
    assert not prove(pl, [crypto.hashable(3)], a.hash())
    print "...proof 2 passed, negative"
