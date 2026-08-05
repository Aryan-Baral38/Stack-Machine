import operator
import sys

class STACK_MACHINE:
    def __init__(self, filename):
        tokens = lex(filename)
        print("token[0] = ", tokens[0])
        if not (tokens[0].lower() == "stack_size"):
            return sys.exit('Invalid Stack Size, first line should be "stack_size size"')
        print("token 1 is stack_size") 
        self.SP = 0
        self.size = size
        self.address = [0 for x in range(size)]
        

    def inrSP(self):
        self.SP += 1

    def dcrSP(self):                    
        self.SP -= 1

    def PUSH(self, value):
        self.address[self.SP] = value
        self.inrSP()

    def POP(self):
        self.dcrSP()
        return self.address[self.SP]

    def DUP(self):
        self.PUSH(self.address[self.SP - 1])

    def SWAP(self):
        a = self.address[self.SP - 2]
        self.address[self.SP - 2] = self.address[self.SP - 1]
        self.address[self.SP - 1] = a

    def OVER(self):
        self.PUSH(self.address[self.SP - 2])

    # Arithmetic and Logical operations
    def binary_op(self, op_func):
        b = self.POP()
        a = self.POP()
        self.PUSH(op_func(a, b))

    def ADD(self):
        self.binary_op(operator.add)

    def SUB(self):
        self.binary_op(operator.sub)

    def MUL(self):
        self.binary_op(operator.mul)

    def DIV(self):
        self.binary_op(operator.floordiv)   

    def MOD(self):
        self.binary_op(operator.mod)

    def AND(self):
        self.binary_op(operator.and_)       

    def OR(self):
        self.binary_op(operator.or_)

    def XOR(self):
        self.binary_op(operator.xor)

    def SHL(self, val):
        b = self.POP()
        self.PUSH(operator.lshift(b, val))

    def SHR(self, val):
        b = self.POP()
        self.PUSH(operator.rshift(b, val))
        
    def EQ(self):
        self.binary_op(operator.eq)

    def LT(self):
        self.binary_op(operator.lt)

    def GT(self):
        self.binary_op(operator.gt)

    def GE(self):
        self.binary_op(operator.ge)

    def LE(self):
        self.binary_op(operator.le)

    def NOT(self):
        a = self.POP()
        self.PUSH(operator.invert(a))

    def INR(self):
        a = self.POP()
        self.PUSH(a + 1)

    def DCR(self):
        a = self.POP()
        self.PUSH(a - 1)

    # Memory Access
    def LOAD(self, val):
        self.PUSH(self.address[val])

    def STORE(self, val):
        a = self.POP()
        self.address[val] = a

    def HALT(self):
        sys.exit("Halted")

    #lexing and executing
    def lex(file):
        tokens = []
        with open(file, 'r') as file:
            for line in file:
                line = line.strip();
                if not line == '':
                    tokens += line.split(' ')
        if tokens[0] != size and not token[1].isnunm():
            sys.exit("Stack Size not specified")
        return tokens
    def parse_and_execute(self):
        self.pos = 0
        self.push_count = 0
        self.pop_count = 0
        while (pos <= len(self.tokens)):
            if not tokens[0] = size


    

     
if __name__ == "__main__":
    m = STACK_MACHINE()               
    m.PUSH(21)
    m.PUSH(20)
    a = m.POP()
    b = m.POP()
    print(a, b)
