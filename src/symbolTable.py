class Scope:
	def __init__(self):
		self.outterTable = None
		self.curTable = dict()

	def __repr__(self):
		return str(self.curTable)


class SymbolTable:
	"""docstring for SymbolTable"""
	def __init__(self):
		self.curScope = Scope()
	def lookup(self, name):
		return self.curScope.curTable.get(name, None)

	def insert(self, name, sym):
		self.curScope.curTable[name] = sym
		
	def createScope(self):
		self.curScope.outterTable = self.curScope.curTable
		self.curScope.curTable = dict()

	def destroyScope(self):
		self.curScope.curTable = self.curScope.outterTable
		self.curScope.outterTable = None

	def __repr__(self):
		return str(self.curScope)

