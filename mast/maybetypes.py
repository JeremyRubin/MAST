#TODO: Jeremy
class Maybe():
    # ABC for a maybe type
    def isValid(self):
        pass
    def map(self, fn):
        pass
    def __str__(self):
        if self.isValid():
            return "Valid(%s)"%repr(self.value)
        else:
            return "Invalid()"

class Valid(Maybe):
    def __init__(self, value):
        self.value = value
    def map(self, fn):
        return fn(self.value)
    def isValid(self):
        return True

class Invalid(Maybe):
    def isValid(self):
        return False
    def map(self, fn):
        return Invalid()
