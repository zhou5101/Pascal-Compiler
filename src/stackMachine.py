from opCode import Opcodes
from struct import unpack, pack

class StackMachine:
	"""docstring for StackMachine"""
	def __init__(self, byteCode):
		self.instruction = byteCode
		self.data = bytearray(100)
		self.stack = []
		self.ip = 0
		self.dp = 0

	def getAddr(self):
		packed = bytearray(4)
		for i in range(4):
			packed[i] = self.instruction[self.ip]
			self.ip+=1
		return self.unpackBytes(packed)
	
	def getData(self, dp):
		packed = bytearray(4)
		for i in range(4):
			packed[i] = self.data[dp]
			dp+=1
		return self.unpackBytes(packed)

	def unpackBytes(self, packed):
		byte1 = packed[0] << 24
		byte2 = packed[1] << 16
		byte3 = packed[2] << 8
		byte4 = packed[3] << 0

		return byte1|byte2|byte3|byte4

	def getFloat(self):
		packed = bytearray(4)
		for i in range(4):
			packed[i] = self.instruction[self.ip]
			self.ip+=1
		#a=round(unpack('>f', packed)[0],6)
		return round(unpack('>f', packed)[0],6)

	def add(self):
		val1 = int(self.stack.pop())
		val2 = int(self.stack.pop())
		#print(f'val1: {val1}, val2: {val2}, sum: {val1+val2}')
		self.stack.append(val1+val2)

	def fadd(self):
		val1 = float(self.stack.pop())
		val2 = float(self.stack.pop())
		#print(f'val1: {val1}, val2: {val2}, sum: {val1+val2}')
		self.stack.append(val1+val2)

	def sub(self):
		val1 = int(self.stack.pop())
		val2 = int(self.stack.pop())
		self.stack.append(val2-val1)
		#print(f'val1: {val1}, val2: {val2}, diff: {val2-val1}')

	def fsub(self):
		val1 = float(self.stack.pop())
		val2 = float(self.stack.pop())
		#print(f'val1: {val1}, val2: {val2}, diff: {val2-val1}')
		self.stack.append(val2-val1)

	def mult(self):

		val1 = int(self.stack.pop())
		val2 = int(self.stack.pop())
		#print(f'val1: {val1}, val2: {val2}, mult: {val1*val2}')
		self.stack.append(val1*val2)

	def fmult(self):
		val1 = float(self.stack.pop())
		val2 = float(self.stack.pop())
		#print(f'val1: {val1}, val2: {val2}, mult: {val1*val2}')
		self.stack.append(val1*val2)

	def div(self):
		val1 = int(self.stack.pop())
		val2 = int(self.stack.pop())
		#print(f'val1: {val1}, val2: {val2}, q: {val2//val1}')
		self.stack.append(val2//val1)

	def fdiv(self):
		val1 = float(self.stack.pop())
		val2 = float(self.stack.pop())
		#print(f'val1: {val1}, val2: {val2}, q: {val2/val1}')
		self.stack.append(round(val2/val1,6))

	def printInt(self):
		print(self.stack.pop(), end='')

	def printCh(self):
		print(chr(self.stack.pop()), end='')

	def printReal(self):
		val = self.stack.pop()
		if isinstance(val, int):
			temp = bytearray(4)
			temp[0] = (val>> 24)& 0xFF
			temp[1] = (val>> 16)& 0xFF
			temp[2] = (val>> 8)& 0xFF
			temp[3] = (val>> 0)& 0xFF
			print(round(unpack('>f', temp)[0],6), end='')
		else:
			print(float(val), end='')

	def printBool(self):
		if self.stack.pop() == 1:
			print('True', end='')
		else:
			print('False', end='')

	def newline(self):
		print()

	def cvr(self):
		val = float(self.stack.pop())
		#print(val)
		self.stack.append(val)

	def cvi(self):
		val = int(self.stack.pop())
		#print(val)
		self.stack.append(val)

	def xchg(self):
		val1 = self.stack.pop() 
		val2 = self.stack.pop() 

		self.stack.append(val1)
		self.stack.append(val2)

	def eql(self):
		val1 = self.stack.pop()
		val2 = self.stack.pop()
		#print(f'val1: {val1}, val2: {val2}, {val1 == val2}')
		self.stack.append(val1 == val2)

	def neql(self):
		val1 = self.stack.pop()
		val2 = self.stack.pop()
		self.stack.append(val2 != val1)

	def gtr(self):
		val1 = self.stack.pop()
		val2 = self.stack.pop()
		self.stack.append(val2 > val1)

	def leq(self):
		val1 = self.stack.pop()
		val2 = self.stack.pop()
		self.stack.append(val2 <= val1)

	def lss(self):
		val1 = self.stack.pop()
		val2 = self.stack.pop()
		self.stack.append(val2 < val1)

	def geq(self):
		val1 = self.stack.pop()
		val2 = self.stack.pop()
		#print(f'val1: {val1}, val2: {val2}')
		self.stack.append(val2 >= val1)

	def jmp(self):
		self.ip =self.getAddr()

	def jtrue(self):
		if self.stack.pop() == True:
			self.ip = self.getAddr()
		else:
			self.getAddr()

	def jfalse(self):
		val = self.stack.pop()
		#print(val)
		if val == False:
			#print(f'before jfalse ip: {self.ip}')
			self.ip = self.getAddr()
			#print(f'After jfalse ip: {self.ip}')
		else:
			self.getAddr()

	def push(self):
		self.dp = self.getAddr()
		val = self.getData(self.dp)
		#print(f'dp :{self.dp}, value: {val} ')
		self.stack.append(val)

	def pushi(self):
		val= self.getAddr()
		#print(f'val: {val}')
		self.stack.append(val)

	def pushf(self):
		val = self.getFloat()
		#print(f'val: {val}')
		self.stack.append(val)

	def pop(self):
		val = self.stack.pop()
		self.dp = self.getAddr()
		#print(f'dp :{self.dp}, value: {val} ')
		#print('val in pop: ', val)

		self.packBytes(val)



	def put(self):
		val = self.stack.pop()
		self.dp = self.stack.pop()
		#print(f'val: {val}, dp: {self.dp}')
		self.packBytes(val)


	def get(self):
		self.dp = self.stack.pop()
		self.stack.append(self.getData(self.dp))


	def packBytes(self, var):
		#print('dp: ', self.dp)
		if isinstance(var, int):
			self.data[self.dp] = (int(var) >> 24) & 0xFF
			self.dp+=1
			self.data[self.dp] = (int(var) >> 16) & 0xFF
			self.dp+=1
			self.data[self.dp] = (int(var) >> 8) & 0xFF
			self.dp+=1
			self.data[self.dp] = (int(var) >> 0) & 0xFF
			self.dp+=1
		elif isinstance(var, float):
			temp = pack(">f", var)
			self.data[self.dp] = temp[0]
			self.dp+=1
			self.data[self.dp] = temp[1]
			self.dp+=1
			self.data[self.dp] = temp[2]
			self.dp+=1
			self.data[self.dp] = temp[3]
			self.dp+=1
		else:
			print(f'Error caused by operation code:{self.ip}')

	def simulate(self):
		
		while True:
			opCode =self.instruction[self.ip]
			self.ip+=1
			if opCode == Opcodes.PUSH:
				#print('push')
				self.push()
				#print()

			elif opCode == Opcodes.PUSHI:
				#print('pushint')
				self.pushi()
				#print()

			elif opCode == Opcodes.PUSHF:
				#print('pushfloat')
				self.pushf()
				#print()

			elif opCode == Opcodes.POP:
				#print('pop')
				self.pop()
				#print()

			elif opCode == Opcodes.JMP:
				#print('jmp')
				self.jmp()
				#print()

			elif opCode == Opcodes.JFALSE:
				#print('jfalse')
				self.jfalse()
				#print()

			elif opCode == Opcodes.JTRUE:
				#print('jtrue')
				self.jtrue()
				#print()

			elif opCode == Opcodes.XCHG:
				#print('xchg')
				self.xchg()
				#print()

			elif opCode == Opcodes.CVR:
				#print('cvr')
				self.cvr()
				#print()

			elif opCode == Opcodes.CVI:
				#print('cvi')
				self.cvi()
				#print()

			elif opCode == Opcodes.ADD:
				#print('add')
				self.add()
				#print()

			elif opCode == Opcodes.SUB:
				#print('sub')
				self.sub()
				#print()

			elif opCode == Opcodes.MULT:
				#print('mult')
				self.mult()
				#print()

			elif opCode == Opcodes.DIV:
				#print('div')
				self.div()
				#print()

			elif opCode == Opcodes.FADD:
				#print('fadd')
				self.fadd()
				#print()

			elif opCode == Opcodes.FSUB:
				#print('fsub')
				self.fsub()
				#print()

			elif opCode == Opcodes.FMULT:
				#print('fmult')
				self.fmult()
				#print()

			elif opCode == Opcodes.FDIV:
				#print('fdiv')
				self.fdiv()
				#print()

			elif opCode == Opcodes.EQL:
				#print('eql')
				self.eql()
				#print()

			elif opCode == Opcodes.NEQL:
				#print('neql')
				self.neql()
				#print()

			elif opCode == Opcodes.GTR:
				#print('gtr')
				self.gtr()
				#print()

			elif opCode == Opcodes.LEQ:
				#print('leq')
				self.leq()
				#print()

			elif opCode == Opcodes.LSS:
				#print('lss')
				self.lss()
				#print()

			elif opCode == Opcodes.GEQ:
				#print('geq')
				self.geq()
				#print()

			elif opCode == Opcodes.HALT:
				return
				
			elif opCode == Opcodes.PRINTINT:
				#print('printInt')
				self.printInt()
				#print()

			elif opCode == Opcodes.PRINTCHR:
				#print('printChar')
				self.printCh()
				#print()

			elif opCode == Opcodes.NEWLINE:
				#print('printNewline')
				self.newline()
				#print()

			elif opCode == Opcodes.PRINTBOOL:
				#print('printBool')
				self.printBool()
				#print()

			elif opCode == Opcodes.PRINTREAL:
				#print('printReal')
				self.printReal()
				#print()

			elif opCode == Opcodes.GET:
				#print('get')
				self.get()
				#print()

			elif opCode == Opcodes.PUT:
				#print('put')
				self.put()
				#print()

			else:
				print(f'{opCode} is not supported by this machine!')
				break
	