import tokens

class Scanner:
	def __init__(self, file):
		self.keywords = tokens.keywordToken
		self.opToken = tokens.opToken
		self.operators = set(tokens.opToken.keys())

		self.tokenList = []
		self.rowIndex = 1
		self.colIndex = 1
		self.pos = 0

		self.src = open(file, 'r').read().lower()

	def buildToken(self, value, token_type):
		if token_type:
			return [value, token_type, self.rowIndex, self.colIndex]
		else:
			return [value, 'TK_UNKNOWN', self.rowIndex, self.colIndex] 
	
	def getChar(self, cur=None):
		#returns current charater
		if cur and cur < len(self.src):
			return self.src[cur]
		elif self.pos <  len(self.src):
			return self.src[self.pos]
		else:
			return 'eof'

	def scan(self):
		#print(f'length of program {len(self.src)}')
		#print(self.getChar(self.pos+1))
		while self.pos < len(self.src):
			ch = self.getChar()
			if ch == '\'':
				string = ''
				cur = self.pos+1
				# looking for next single quote
				for c in self.src[cur:]:
					if c!='\'':
						string += c
					else:
						break
				#len without single quote
				if len(string) == 1:
					self.colIndex+=3
					self.pos+=3
					self.tokenList.append([string, 'TK_CHAR',self.rowIndex, self.colIndex])
				else: 
					self.colIndex+=len(string)+2
					self.pos+= len(string)+2
					self.tokenList.append([string, 'TK_STRING',self.rowIndex, self.colIndex])

				#print(f'{self.pos} string: {string} and Token:  {self.tokenList[-1]}')
			elif ch.isalpha():
				# current char is a charater 
				key = ch
				cur = self.pos+1

				for c in self.src[cur:]:
					if c.isalpha() or c.isdigit():
						# mix of character and digit
						key+=c
					else:
						break

				self.colIndex+=len(key)
				self.pos+=len(key)
				#check tokens
				if self.keywords.get(key, None):
					self.tokenList.append(self.buildToken(key, self.keywords.get(key, None)))
				else:
					#use as identifier
					self.tokenList.append([key, 'TK_ID', self.rowIndex, self.colIndex])
				#print(f'{self.pos} keywords: {key} and Token: {self.tokenList[-1]}')
			elif ch.isdigit():
				# current char is a digit
				digit = ch
				cur = self.pos+1

				for c in self.src[cur:]:
					if c.isdigit() or c == '.':
						digit += c
					else:
						break
				#check range/float/integer
				if len(digit.split('..')) ==2 :
					tok = 'TK_RANGE'
				elif len(digit.split('.')) ==2:
					tok = 'TK_REAL'
				elif digit.isdigit():
					tok = 'TK_INTEGER'
				else:
					tok = 'TK_UNKNOWN'

				self.colIndex+=len(digit)
				self.pos += len(digit)
				self.tokenList.append([digit, tok, self.rowIndex, self.colIndex])
				#print(f'{self.pos} digits/range: {digit} and Token: {self.tokenList[-1]}')

			elif ch in self.operators:
				#chekc operators
				op = ch
				if op == ':':
					nextCh = self.getChar(self.pos+1)
					if nextCh == '=':
						op += nextCh
				elif op == '<':
					nextCh = self.getChar(self.pos+1)
					if nextCh == '>':
						op+=nextCh
					elif nextCh == '=':
						op+= nextCh
				elif op == '>':
					nextCh = self.getChar(self.pos+1)
					if nextCh == '=':
						op += nextCh
				
				self.colIndex+=len(op)
				self.pos += len(op)
				self.tokenList.append(self.buildToken(op, self.opToken.get(op, None)))	
				#print(f'{self.pos} operators: {op} and Token: {self.tokenList[-1]}')
			elif ch == ' ':
				#skip space
				self.colIndex+=1
				self.pos+=1
				#print(f'{self.pos} space: \'{ch}\'')

			elif ch == '\n' or '\r':
				#skip newline
				self.pos+=1
				self.rowIndex+=1
				self.colIndex=0
				#print(f'{self.pos} newline')

			elif ch =='\t':
				self.colIndex+=4
				#print(f'{self.pos} tap: \'{ch}\'')

			else:
				self.pos+=1
				raise TypeError(f'Unidentified character find in row: {self.rowIndex}, column: {self.colIndex}!!!')

		self.tokenList.append(['eof', 'TK_EOF', self.rowIndex, self.colIndex])

		return self.tokenList