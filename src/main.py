from scanner import Scanner
from MyParser import Parser
from stackMachine import StackMachine
import sys

if __name__ == '__main__':
    filename = sys.argv[1]

    tokens = Scanner(filename).scan()
    byteCode = Parser(tokens).compile()

    simulator = StackMachine(byteCode)
    title = filename.split('/')[-1].upper()
    print(f'===========START OF {title}===========\n')
    simulator.simulate()
    print(f'\n============END OF {title}============')