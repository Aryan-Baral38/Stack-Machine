# To add:
#   -Variables
#   -Branching
#   -sub-routines


import operator
import sys
from lexer_and_parser import lexer, Parser, get_filename

class STACK_MACHINE:
    def __init__(self, size):
        self.SP = 0
        self.size = size
        self.address = [0 for x in range(size)]
        self.input_buffer = []
        self.output_buffer = []
        

    def inrSP(self):
        self.SP += 1

    def dcrSP(self):                    
        self.SP -= 1

    def PUSH(self, value):
        self.address[self.SP] = value
        self.input_buffer.append(value)
        self.inrSP()

    def POP(self):
        val = self.address[self.SP - 1]
        self.address[self.SP] = 0
        self.dcrSP()
        self.output_buffer.append(val)
        return val 

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
        self.quit()

    def quit(self):
        print("Executed without error")
        print("Stack")
        for i in range(len(self.address)):
            if i == self.SP - 1:
                print(f"[{i}]: --> {self.address[i]}")
            else:
                print(f"[{i}]: {self.address[i]}")

            
          
        print("output buffer: ", self.output_buffer)
        print("Top Value: ", self.address[self.SP - 1])


    #lexing and executing


class Execution(STACK_MACHINE):
    def __init__(self, parsed_instructions, size):
        super().__init__(size)
        self.parsed_instructions = parsed_instructions  
        self.execute()

    def execute(self):
        i = 0 
        print(self.parsed_instructions)
        for instruction in self.parsed_instructions:
            opcode = instruction[0]
            operand = instruction[1]
            match opcode:
                #stack size is already initialized
                case "DCR":
                    self.dcrSP()

                case "DUP":
                    self.DUP()

                case "INR":
                    self.inrSP()

                case "OVER":
                    self.OVER()

                case "STACK_SIZE":
                    pass 

                case "SWAP":
                    self.SWAP()

                case "POP":
                    self.output_buffer.append(self.POP())
                
                case "PUSH":
                    self.PUSH(operand)
                # Arithmetic and logcal operations
                case "ADD":
                    self.ADD()
                case "SUB":
                    self.SUB()
                
                case "MUL":
                    self.MUL()

                case "DIV":
                    self.DIV()

                case "MOV":
                    self.MOD()

                case "AND":
                    self.AND()

                case "OR":
                    self.OR()

                case "OXR":
                    self.XOR()
                
                case "SHL":
                    self.SHL(operand)
                case "SHR":
                    self.SHR(operand)
                case "EQ":
                    self.EQ()

                case "LT":
                    self.LT()

                case "GT":
                    self.GT()

                case "GE":
                    self.GE()
                case "LE":
                    self.LE()

                case "NOT":
                    self.NOT()

                case "INR":
                    self.INR()

                case "DCR":
                    self.DCR()

                #mem Access
                case "LOAD":
                    self.LOAD(operand)

                case "STORE":
                    print("store reached", opcode, operand, type(operand))
                    self.STORE(operand)

                case "HALT":
                    self.HALT()
                
                case _:
                    sys.exit("Invalid opcode:", f"'{opcode}'" , " found during execution")
        

     
if __name__ == "__main__":
    filename = get_filename(debugging = False)
    tokens = lexer(filename)
    parser_obj = Parser(tokens)
    instructions_list = parser_obj.parse()
    size = instructions_list[0][1]
    m = Execution(instructions_list, size)              
