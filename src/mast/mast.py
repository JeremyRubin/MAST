from crypto import *
class Mast():

	def __init__(self, mode, content, honest=True, addNonces=True, debug=True, leaf=False):
		modes = ["client","server"]
		if mode not in modes:
			raise ValueError("Mode not in %s "%modes)
		self.mode = mode
		self.content = content
		self.contenthash = _hash(content)	#TODO: syntax check content
		self.honest = honest
		self.addNonces = addNonces
		self.debug = debug
		self.children = set()
		self.leaf = leaf

	#TODO: return new node
	def addBr(self, content, leaf=False):	
		if self.leaf:
			raise ValueError("Leaf node cannot have children")
		if isInstance(content, Mast):
			pass	#TODO
		elif isInstance(content, str):
			pass 	#TODO
		else:
			raise ValueError("Illegal content type: %s"%str(content))

	#TODO: make this pretty
	def __str__(self):
		pass

	def run(self, port=8000, host="localhost"):
		if self.mode == "client":
			pass	#TODO
		else:
			pass	#TODO
