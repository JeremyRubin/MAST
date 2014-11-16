from crypto import *
class Mast():

	def __init__(self, mode, content, parent=None, honest=True, addNonces=True, debug=True, leaf=False):
		modes = ["run","compile"]
		if mode not in modes:
			raise ValueError("Mode not in %s "%modes)
		self.mode = mode
		self.content = content
		if self.mode =="compile":
			self.contenthash = _hash(content)	#TODO: syntax check content
		self.parent = parent
		self.honest = honest
		self.addNonces = addNonces
		self.debug = debug
		self.children = set()
		self.leaf = leaf

	#TODO: return new node
	def addBr(self, content, hash=None, leaf=False):
		newBr = None	#create new mast
		if self.mode == "compile":
			if self.leaf:
				raise ValueError("Leaf node cannot have children")
			
			if isInstance(content, Mast):
				pass	#TODO
			elif isInstance(content, str):
				pass 	#TODO
			else:
				raise ValueError("Illegal content type: %s"%str(content))
			return newBr

		else:	#TODO: All different	
			return newBr

	#TODO: make this pretty
	def __str__(self):
		pass

	#TODO: this will be moved
	def construct(self, port=8000, host="localhost"):
		if self.mode == "run":
			pass	#TODO
		else:
			pass	#TODO
