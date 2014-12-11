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