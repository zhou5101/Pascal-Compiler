from opCode import Opcodes, ops
from symbolTable import SymbolTable
from symbol import Symbol
from struct import pack

class Parser(object):
	def __init__(self, tokenLists):
		self.tokenLists = tokenLists
		self.index = 0
		self.curToken = None
		self.byteArray = bytearray(1000)
		self.symbolTable = SymbolTable()
		self.operations = ops

		self.dp = 0
		self.ip = 0

	def getToken(self):
		# return current token
		if self.index < len(self.tokenLists):
			self.curToken = self.tokenLists[self.index]
			self.index+=1
	
	def match(self, tokenType):
		# move to next token
		if self.curToken[1] == tokenType:
			self.getToken()
		else:
			raise SyntaxError(f'Token:{self.curToken[1]} doest not macth {tokenType} at row: {self.curToken[2]}, col: {self.curToken[3]}')

	def emitOpcodes(self, op):
		# emit opcodes as a byte
		self.byteArray[self.ip] = op
		self.ip+=1

	def emitByte(self, var):
		# emite value as four bytes
		if isinstance(var, int):
			self.byteArray[self.ip] = (int(var) >> 24) & 0xFF
			self.ip+=1
			self.byteArray[self.ip] = (int(var) >> 16) & 0xFF
			self.ip+=1
			self.byteArray[self.ip] = (int(var) >> 8) & 0xFF
			self.ip+=1
			self.byteArray[self.ip] = (int(var) >> 0) & 0xFF
			self.ip+=1
		else:
			temp = pack(">f", var)
			self.byteArray[self.ip] = temp[0]
			self.ip+=1
			self.byteArray[self.ip] = temp[1]
			self.ip+=1
			self.byteArray[self.ip] = temp[2]
			self.ip+=1
			self.byteArray[self.ip] = temp[3]
			self.ip+=1

	def compile(self):
		self.header()
		self.declarations()
		self.begin()

		self.match('TK_EOF')
		self.emitOpcodes(Opcodes.HALT)
		return self.byteArray
	
	def header(self):
		self.getToken()
		self.match('TK_PROGRAM')
		self.match('TK_ID')
		self.match('TK_SEMI_COLON')

	def declarations(self):
		#declares var, label, procedure
		while self.curToken[1]!='TK_BEGIN':
			#print(f'\ndeclaration {self.curToken}')
			token = self.curToken[1]
			if token == 'TK_VAR':
				self.varDeclaration()
			elif token == 'TK_LABEL':
				self.labelDeclaration()
			elif token == 'TK_PROCEDURE':
				self.procDeclaration()
			else:
				raise SyntaxError(f'Token:{self.curToken[1]} doest not mathc at row: {self.curToken[2]}, col: {self.curToken[3]}')

	def varDeclaration(self):
		#insert vars into symbol table
		#print('varDeclaration')
		self.match('TK_VAR')
		varList = []
		while self.curToken[1] == 'TK_ID':
			if self.curToken not in varList:
				varList.append(self.curToken)
				self.match('TK_ID')
				if self.curToken[1] == 'TK_COMMA':
					self.match('TK_COMMA')
			else:
				raise NameError("Variable already declared" + self.curr_t[1])

		self.match('TK_COLON')
		dataType = self.curToken[1]
		self.match(dataType)

		#if array, go to array declaration
		if dataType == 'TK_ARRAY':
			self.arrayDeclaration(varList)
		else:
			for i in varList:
				self.symbolTable.insert(i[0], Symbol(i[0], 'TK_VAR', dataType, self.dp))
				self.dp+=4

		self.match('TK_SEMI_COLON')
		#print(self.symbolTable)
		#print('varDeclaration')

	def labelDeclaration(self):
		#insert label into symbol table
		#print('labelDeclaration')
		self.match('TK_LABEL')
		labelList = []
		while self.curToken[1] != 'TK_SEMI_COLON':
			if self.curToken not in labelList:
				labelList.append(self.curToken)
			else:
				raise NameError(f'Repeate label: {self.curToken}')
			self.match('TK_ID')

			if self.curToken[1] == 'TK_COMMA':
				self.match('TK_COMMA')

			elif self.curToken[1] == 'TK_SEMI_COLON':
				break

		self.match('TK_SEMI_COLON')

		for i in labelList:
			self.symbolTable.insert(i[0], Symbol(i[0], 'TK_LABEL', 'LABEL', 0))
		#print(self.symbolTable)
		#print('labelDeclaration')

	def procDeclaration(self):
		#uncompleted
		pass

	def arrayDeclaration(self, tempToken):
		#inser array to symbol table
		self.match('TK_LB')
		if len(self.curToken[0].split('..')) != 2:
			raise SyntaxError('Range needs to be like  0..2')

		temp = self.curToken[0].split('..')
		if temp[0].isdigit() and temp[1].isdigit():
			lower = int(temp[0])
			upper = int(temp[1])
			indexType = 'TK_INTEGER'
		elif temp[0].isalpha() and temp[1].isalpha():
			lower = ord(temp[0])
			upper = ord(temp[1])
			indexType = 'TK_CHAR'
		else:
			raise TypeError('Unsupported index types: ' + self.curToken)

		self.match('TK_RANGE')
		self.match('TK_RB')
		self.match('TK_OF')

		dataType= self.curToken[1]
		self.match(dataType)

		for i in tempToken:
			sym = Symbol(i[0], 'TK_ARRAY', dataType, self.dp)
			sym.indexType = indexType
			sym.low = lower
			sym.high = upper
			sym.assigmentType = dataType
			self.symbolTable.insert(i[0], sym)
			self.dp += 4*upper - 4*lower

	def begin(self):
		#print('begin')
		self.match('TK_BEGIN')

		self.statement()
		#print('end statement')
		self.match('TK_END')
		self.match('TK_DOT')

	def statement(self):
		while self.curToken[1] != 'TK_END':
			token = self.curToken[1]
			if token == 'TK_ID':
				#check whether identifiers is exisited in symbol table
				#change token to match corresponding statement
				self.lookup()
			elif token == 'TK_WRITELN':
				self.writeStatement()
			elif token == 'TK_IF':
				self.ifStatement()
			elif token == 'TK_WHILE':
				self.whileStatement()
			elif token == 'TK_REPEAT':
				self.repeatStatement()
			elif token == 'TK_GOTO':
				self.gotoStatement()
			elif token == 'TK_CASE':
				self.caseStatement()
			elif token == 'TK_A_VAR':
				self.assigment()
			elif token == 'TK_A_LABEL':
				self.labelStatement()
			elif token == 'TK_A_ARRAY':
				self.arrayAssigment()
			elif token == 'TK_SEMI_COLON':
				self.match('TK_SEMI_COLON')
			else:
				return

	def lookup(self):
		#checking type of cur var in sysmbol table
		#print(f'lookup ID for token: {self.curToken}')
		curSym = self.symbolTable.lookup(self.curToken[0])
		#print(f'token type for curSym: {curSym.tokenType}')
		if curSym:
			if curSym.tokenType == 'TK_VAR':
				self.curToken[1] = 'TK_A_VAR'

			elif curSym.tokenType == 'TK_LABEL':
				self.curToken[1] = 'TK_A_LABEL'

			elif curSym.tokenType == 'TK_ARRAY':
				self.curToken[1] = 'TK_A_ARRAY'
			else:
				raise SyntaxError(f'{self.curToken[0]} is not a valid data type!')
		else:
			raise SyntaxError(f'{self.curToken[0]} initialized before declaration!')
		#print(f'after lookup ID for token: {self.curToken}')

	def assigment(self):
		#print('VarAssigment')
		curID = self.symbolTable.lookup(self.curToken[0])
		#print(self.curToken)
		lhs = curID.dataType
		lhsAddr = curID.addr
		self.match('TK_A_VAR')
		self.match('TK_ASSIGN')
		rhs = self.E();
		if lhs == rhs:
			self.emitOpcodes(Opcodes.POP)
			self.emitByte(lhsAddr)
		else:
			print(f'lhs:{lhs}, rhs:{rhs}')
			raise SyntaxError(f'ERORR IN ROW {self.curToken[2]}, LHS and RHS data type must be same!')
		#self.match('TK_SEMI_COLON')
		#print('VarAssigment')
		#print(self.curToken)


	def writeStatement(self):
		#print('writeStatement')
		self.match('TK_WRITELN')
		self.match('TK_LP')

		while True:
			if self.curToken[1] == 'TK_ID' :
				sym = self.symbolTable.lookup(self.curToken[0])
				if sym.tokenType == 'TK_ARRAY':
					self.match('TK_ID')
					self.arrayAcess(sym)
					self.emitOpcodes(Opcodes.GET)
					t = sym.dataType
				elif sym.tokenType == 'TK_VAR':
					t = sym.dataType
					self.emitOpcodes(Opcodes.PUSH)
					self.emitByte(sym.addr)
					self.match('TK_ID')
			else:
				t = self.curToken[1]
				if t=='TK_INTEGER':
					self.emitOpcodes(Opcodes.PUSHI)
					self.emitByte(int(self.curToken[0]))
				elif t=='TK_REAL':
					self.emitOpcodes(Opcodes.PUSHF)
					self.emitByte(float(self.curToken[0]))
				elif t =='TK_BOOL':
					self.emitOpcodes(Opcodes.PUSHI)
					if self.curToken[0] == 'true':
						self.emitByte(1)
					else:
						self.emitByte(0)
				elif t=='TK_CHAR':
					self.emitOpcodes(Opcodes.PUSHI)
					self.emitByte(ord(self.curToken[0]))
				elif t=='TK_STRING':
					for i in self.curToken[0]:
						self.emitOpcodes(Opcodes.PUSHI)
						self.emitByte(ord(i))
						self.emitOpcodes(Opcodes.PRINTCHR)
				self.match(self.curToken[1])

			if t=='TK_INTEGER':
				self.emitOpcodes(Opcodes.PRINTINT)
			elif t=='TK_REAL':
				self.emitOpcodes(Opcodes.PRINTREAL)
			elif t=='TK_CHAR':
				self.emitOpcodes(Opcodes.PRINTCHR)
			elif t=='TK_BOOL':
				self.emitOpcodes(Opcodes.PRINTBOOL)

			if self.curToken[1] == 'TK_COMMA':
				self.match('TK_COMMA')

			elif self.curToken[1] =='TK_RP':
				self.match('TK_RP')
				self.emitOpcodes(Opcodes.NEWLINE)
				return
			else:
				raise SyntaxError("Expected Clsoing Parentheses or Comma")

	def repeatStatement(self):
		self.match('TK_REPEAT')
		target = self.ip
		self.statement()
		self.match('TK_UNTIL')
		self.condition()
		# jumping address
		self.emitOpcodes(Opcodes.JFALSE)
		self.emitByte(target)

	def whileStatement(self):
		self.match('TK_WHILE')
		target = self.ip
		self.condition()

		self.emitOpcodes(Opcodes.JFALSE)
		#creating hole
		hole = self.ip
		self.emitByte(0)
		self.match('TK_DO')

		self.match('TK_BEGIN')
		self.statement()
		self.match('TK_END')
		self.match('TK_SEMI_COLON')

		self.emitOpcodes(Opcodes.JMP)
		self.emitByte(target)
		#filing hole
		saveIP = self.ip
		self.ip = hole
		#jump address
		self.emitByte(saveIP)
		self.ip = saveIP

	def ifStatement(self):
		#print('IF statement')
		self.match('TK_IF')
		self.condition()
		self.match('TK_THEN')
		#creating hole
		self.emitOpcodes(Opcodes.JFALSE)
		hole1 = self.ip
		self.emitByte(0)
		self.statement()

		if self.curToken[1] == 'TK_ELSE':
			self.emitOpcodes(Opcodes.JMP)
			hole2 = self.ip
			self.emitByte(0)
			saveIP = self.ip
			self.ip = hole1
			self.emitByte(saveIP)
			self.ip = saveIP
			hole1=hole2
			self.statement()
			self.match('TK_ELSE')
			self.statement()


		saveIP = self.ip
		self.ip = hole1
		self.emitByte(saveIP)
		self.ip = saveIP
		#print('IF statement')

	def labelStatement(self):
		#print('labelStatement')
		sym = self.symbolTable.lookup(self.curToken[0])
		self.match('TK_A_LABEL')
		self.match('TK_COLON')

		if sym:
			#print(f'cur(save) IP: {self.ip}')
			target = sym.addr

			#print(f'target: {target}')
			saveIP = self.ip

			self.ip=target

			#print(f'save IP: {saveIP}')
			self.emitByte(saveIP)

			self.ip = saveIP

			self.statement()
		else:
			raise SyntaxError(f'Label: {self.curToken} doesnot exist!')

		#print('labelStatement')


	def gotoStatement(self):
		#print('goto')
		self.match('TK_GOTO')
		sym = self.symbolTable.lookup(self.curToken[0])
		self.match('TK_ID')

		self.emitOpcodes(Opcodes.JMP)

		if sym:
			sym.addr = self.ip
			#print(f'label addr: {sym.addr}')
			#print(sym)
		else:
			raise SyntaxError(f'Label: {self.curToken} doesnot exist!')

		self.emitByte(0)

		self.match('TK_SEMI_COLON')
		#print('goto')


	def caseStatement(self):
		self.match('TK_CASE')
		self.match('TK_LP')
		token = self.curToken[0]

		t1 = self.E()

		if t1 == 'TK_REAL':
			raise TypeError('Case statement does not support float data type')

		self.match('TK_RP')
		self.match('TK_OF')

		caseLabels = []

		while self.curToken[1] in ['TK_INTEGER', 'TK_CHAR', 'TK_BOOL']:
			t2 = self.E()
			self.emit('TK_EQUAL', t1, t2)
			self.match('TK_COLON')

			self.emitOpcodes(Opcodes.JFALSE)
			hole = self.ip
			self.emitByte(0)
			self.statement()

			self.emitOpcodes(Opcodes.JMP)
			caseLabels.append(self.ip)
			self.emitByte(0)

			saveIP = self.ip
			self.ip = hole
			self.emitByte(saveIP)
			self.ip = saveIP

			if self.curToken[1] != 'TK_END':
				#for next comparison 
				sym = self.symbolTable.lookup(token)
				if sym:
					self.emitOpcodes(Opcodes.PUSH)
					self.emitByte(sym.addr)

		self.match('TK_END')
		self.match('TK_SEMI_COLON')

		saveIP = self.ip
		#print(f"caseLabels : {caseLabels}")
		#filling address of label
		for i in caseLabels:
			self.ip = i
			self.emitByte(saveIP)

		self.ip = saveIP

	def arrayAssigment(self):
		sym = self.symbolTable.lookup(self.curToken[0])
		if sym:
			lhs = sym.dataType
			self.match('TK_A_ARRAY')
			
			self.arrayAcess(sym)
	
			self.match('TK_ASSIGN')
			rhs = self.E()

			if lhs == rhs:
				self.emitOpcodes(Opcodes.PUT)
		else:
			raise NameError(f'Array doesnot exist: {self.curToken}')

	def arrayAcess(self, array):
		self.match('TK_LB')

		sym = self.symbolTable.lookup(self.curToken[0])
		#check whether array index is a variable or literal
		if sym:
			if sym.dataType != array.indexType:
				raise TypeError('Index tyep of Array: {sym} does not match')
			
			self.emitOpcodes(Opcodes.PUSH)
			self.emitByte(sym.addr)
			self.match('TK_ID')
			self.match('TK_RB')
			
			lo = array.low
			hi = array.high
			self.emitOpcodes(Opcodes.PUSHI)
			self.emitByte(lo)
			self.emitOpcodes(Opcodes.XCHG)
			self.emitOpcodes(Opcodes.SUB)

			self.emitOpcodes(Opcodes.PUSHI)
			self.emitByte(4)

			self.emitOpcodes(Opcodes.MULT)
			self.emitByte(array.addr)
			self.emitByte(Opcodes.ADD)
		else:
			#print(self.curToken)
			index = self.E()
			if index != array.indexType:
				raise TypeError('Index type {index} does not match Array {array}')
			self.match('TK_RB')

			lo = array.low
			hi = array.high
			self.emitOpcodes(Opcodes.PUSHI)
			self.emitByte(lo)
			#self.emitOpcodes(Opcodes.XCHG)
			self.emitOpcodes(Opcodes.SUB)

			self.emitOpcodes(Opcodes.PUSHI)
			self.emitByte(4)

			self.emitOpcodes(Opcodes.MULT)

			self.emitOpcodes(Opcodes.PUSHI)
			self.emitByte(array.addr)

			self.emitOpcodes(Opcodes.ADD)

	def E(self):
		t1 = self.T()
		while self.curToken[1] in ['TK_ADD','TK_MINUS']:
			op = self.curToken[1]
			self.match(op)
			t1 = self.emit(op, t1, self.T())
		return t1

	def T(self):
		t1 = self.F()
		while self.curToken[1] in ['TK_MULTIPLY','TK_DIVIDE','TK_DIV']:
			op = self.curToken[1]
			self.match(op)
			t1 = self.emit(op, t1, self.F())
		return t1

	def F(self):
		val = self.curToken[0]
		token = self.curToken[1]

		if token == 'TK_INTEGER':
			#print('int val in F(), ',val)

			self.emitOpcodes(Opcodes.PUSHI)
			self.emitByte(int(val))

		elif token == 'TK_REAL':
			#print('val in F(), ',val)
			self.emitOpcodes(Opcodes.PUSHF)
			self.emitByte(float(val))

		elif token == 'TK_CHAR':
			self.emitOpcodes(Opcodes.PUSHI)
			self.emitByte(ord(val))

		elif token == 'TK_STRING':
			for c in val:
				self.emitOpcodes(Opcodes.PUSHI)
				self.emitByte(ord(c))

		elif token == 'TK_BOOL':
			self.emitOpcodes(Opcodes.PUSHI)
			val = 1 if val == 'true' else 0
			self.emitByte(val)

		#elif token in ['TK_NOT', 'TK_AND', 'TK_OR']:
			#self.match(token)
			#return self.F()

		elif token == 'TK_LP':
			self.match(token)
			t = self.E()
			self.match('TK_RP')
			return t

		elif token == 'TK_ID':
			sym = self.symbolTable.lookup(val)
			if sym:
				if sym.tokenType == 'TK_VAR':
					self.emitOpcodes(Opcodes.PUSH)
					self.emitByte(sym.addr)
					self.match('TK_ID')
					return sym.dataType
				else:
					sym.tokenType == 'TK_ARRAY'
					self.match('TK_ID')
					self.arrayAcess(sym)
					self.emitOpcodes(Opcodes.GET)
					return sym.dataType

			else:
				raise SyntaxError(f'Symnol no found {val}')
		else:
			raise SyntaxError(f'Unsupported data type {token}: {val}')

		self.match(token)
		return token


	def condition(self):
		e1 = self.E()

		while self.curToken[1] in {'TK_EQUAL', 'TK_NOT_EQUAL','TK_GREATER_THAN', 'TK_LESS_THAN', 'TK_GREATER_THAN_EQUAL', 'TK_LESS_THAN_EQUAL'}:
			op = self.curToken[1]
			self.match(op)
			e2 = self.T();
			#print(op)
			return self.emit(op, e1, e2)
		else :
			raise SyntaxError(f'Expected contional statement instead of {self.curToken}')

	def emit(self, op, t1, t2):
		if op == 'TK_ADD':
			return self.emitArth('+', t1,t2)
		elif op == 'TK_MINUS':
			return self.emitArth('-', t1,t2)
		elif op == 'TK_MULTIPLY':
			return self.emitArth('*', t1,t2)
			
		elif op == 'TK_DIVIDE':
			return self.emitArth('/', t1,t2)
			
		elif op == 'TK_DIV':
			if t1 =='TK_INTEGER' and t2 == 'TK_INTEGER':
				self.emitOpcodes(Opcodes.DIV)
				return 'TK_INTEGER'
		elif op in {'TK_EQUAL','TK_NOT_EQUAL','TK_GREATER_THAN','TK_LESS_THAN','TK_GREATER_THAN_EQUAL','TK_LESS_THAN_EQUAL'}:
			return self.emitPred(op, t1, t2)

		else:
			raise TypeError(f'Cannot match datatype.{op}, {t1}, {t2}!')

	def emitArth(self, op, t1, t2):
		if t1 == 'TK_INTEGER' and t2 == 'TK_INTEGER':
			if op == '/':
				self.emitOpcodes(self.operations['f'+op])
				return 'TK_REAL'
			self.emitOpcodes(self.operations[op])
			return 'TK_INTEGER'

		elif t1 == 'TK_INTEGER' and t2 =='TK_Real':
			self.emitOpcodes(Opcodes.XCHG)
			self.emitOpcodes(Opcodes.CVR)
			self.emitOpcodes(Opcodes.XCHG)
			self.emitOpcodes(self.operations['f'+op])
			return 'TK_REAL'

		elif t1 == 'TK_REAL' and t2 == 'TK_INTEGER':
			self.emitOpcodes(Opcodes.CVR)
			self.emitOpcodes(self.operations['f'+op])
			return 'TK_REAL'

		elif t1 == 'TK_REAL' and t2 == 'TK_REAL':
			self.emitOpcodes(self.operations['f'+op])
			return 'TK_REAL'
		return None

	def emitPred(self, op, t1, t2):
		if t1==t2:
			pass

		elif t1 == 'TK_INTEGER' and t2 == 'TK_REAL':
			self.emitOpcodes(Opcodes.XCHG)
			self.emitOpcodes(Opcodes.CVR)

		elif t1 == 'TK_REAL' and t2 == 'TK_INTEGER':
			self.emitOpcodes(Opcodes.CVR)

		else:
			return None

		self.emitOpcodes(self.operations[op])
		return 'TK_BOOL'