class Symbol:
	def __init__(self, name, tokenType, dataType, address):
		self.name = name
		self.tokenType = tokenType
		self.dataType = dataType
		self.addr = address

	def __repr__(self):
		return f'{self.name}, {self.dataType}, {self.tokenType}, {self.addr}'
