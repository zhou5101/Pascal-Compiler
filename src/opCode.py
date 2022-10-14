class Opcodes:
	PUSH = 1
	POP = 2
	PUSHI = 3
	PUSHF = 4

	JMP = 5
	JFALSE = 6 
	JTRUE = 7

	CVR = 8
	CVI = 9
	XCHG = 10

	ADD = 11
	SUB = 12
	MULT = 13
	DIV = 14

	FADD = 15
	FSUB = 16
	FMULT = 17
	FDIV = 18

	EQL = 19
	NEQL = 20
	GEQ = 21
	LEQ = 22
	GTR = 23
	LSS = 24

	HALT = 25
	PRINTINT = 26
	PRINTCHR = 27
	NEWLINE = 28
	PRINTBOOL = 29
	PRINTREAL = 30
	GET = 31
	PUT = 32

ops = {
	'+': Opcodes.ADD,
	'f+': Opcodes.FADD,
	'-': Opcodes.SUB,
	'f-': Opcodes.FSUB,
	'*': Opcodes.MULT,
	'f*': Opcodes.FMULT,
	'/': Opcodes.DIV,
	'f/': Opcodes.FDIV,
	'TK_EQUAL': Opcodes.EQL,
	'TK_NOT_EQUAL': Opcodes.NEQL,
	'TK_LESS_THAN': Opcodes.LSS,
	'TK_GREATER_THAN': Opcodes.GTR,
	'TK_GREATER_THAN_EQUAL': Opcodes.GEQ,
	'TK_LESS_THAN_EQUAL': Opcodes.LEQ
}