# Feature Completed

- Expressions, integers and reals
- Assignment
- Writeln
- Repeat statement
- While statement
- If statement
- Goto
- Case
- Array

# Feature Uncompleted

- Procedures

# Files

- tokens.py : tokens and keywords used in scanner
- scanners.py : scans the input pascal file and returns a list of tokens
- MyParser.py : process the output of scanner, and produces a series of operations in byte code array
- opCode.py : defines operation code class
- symbol.py : defines symbols used in symbolTable.py
- symbolTable.py : defines symbol table in MyParser.py, responsible for keep tracking of info of variables, labels and arrays declaration
- stackMachine.py : handles byte code array returned from MyParser.py, and execute the operations based on it

# Executing Program

Note: I am using python version 3.9.6, but should be compatible for any version of python3.

1. cd src

2. python main.py ./ex/{pascal file name}
   
   - Ex: python main.py ./ex/write.pas

3. The output of pascal file will be surrounding by the START and END.