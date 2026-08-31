#   -Variables
#   -runtime error handling
#   -Branching
# To add:
#   -sub-routines
#   --print function
import operator
import sys
from lexer_and_parser import lexer, Parser, get_filename

class STACK_MACHINE:
    def __init__(self, size):
        self.SP = 0
        print("SIZE:" ,size)
        self.stack_size = size
        self.address = ["NaN" for x in range(self.stack_size)]
        self.call_stack = [0]*10
        self.call_SP = 0
        self.no_of_var = 10
        self.variables = ["NaN"] * self.no_of_var 
        self.input_buffer = []
        self.output_buffer = []
        self.labels = {}
        self.flags = {"zero": 0, "minus" : 0, "even": 0}
        self.PC = 0 
    
    
    def inrSP(self):
        if self.SP < self.stack_size:
            self.SP += 1
        else:
            self.error("Stack overflow, Stack pointer exceeds stack size", "stack_overflow")

    def dcrSP(self):    
        if self.SP > 0:
            self.SP -= 1
        else:
            self.error("Stack underflow, Negative SP")
    
    def JMP(self, arg_label):
        if not arg_label in self.labels:
            self.error(f"<{arg_label}> Label doesnt exist" )

        self.PC = self.labels[arg_label] + 1

    def JNZ(self, arg_label):
        if not arg_label in self.labels:
            self.error(f"<{arg_label}> Label doesnt exist" )
        a = self.POP()
        if a != 0:
            self.PC = self.labels[arg_label] + 1
            self.PC = self.labels[arg_label] + 1
    def JZ(self, arg_label):
        if not arg_label in self.labels:
            self.error(f"<{arg_label}> Label doesnt exist" )

        a = self.POP()
        if a == 0:
            self.PC = self.labels[arg_label] + 1

    def PUSH(self, value):
        if self.SP >= self.stack_size:
            self.error("Stack overflow, pushing outside stack", "larger_than_stack")
        self.address[self.SP] = value
        self.input_buffer.append(value)
        self.inrSP()

    def POP(self):
        if self.SP <= 0:
            self.error("Stack underflow", "stack_overflow")
        val = self.address[self.SP - 1]
        self.address[self.SP - 1] = 0
        self.dcrSP()
        self.output_buffer.append(val)
        return val 

    def DUP(self):
        self.PUSH(self.address[self.SP - 1])

    def SWAP(self):
        if self.SP < 1:
            self.error("Nothing to swap, Stack underflow")
        a = self.address[self.SP - 2]
        self.address[self.SP - 2] = self.address[self.SP - 1]
        self.address[self.SP - 1] = a

    def OVER(self):
        if self.SP < 2:
            self.error("Stack underflow", "stack_overflow")
        self.PUSH(self.address[self.SP - 2])
    #sub-routines
    def CALL(self, arg_label):
        print("Inside CALL")
        if arg_label not in self.labels:
            self.error(f"<{arg_label}> Label doesnt exist" )
        if self.call_SP >= len(self.call_stack):
            self.error("Call Stack Overflow", "call_stack_overflow")

        self.call_stack[self.call_SP] = self.PC 
        self.call_SP += 1
        self.PC = self.labels[arg_label] + 1

    def RET(self):
        print("call_stack", self.call_stack)
        print("call_SP", self.call_SP)
        if self.call_SP == 0:
            self.error("Call stack underflow", "call_stack_underflow")
        self.call_SP -= 1
        self.PC = self.call_stack[self.call_SP]
        
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

    def SHR(self, val):
        
        b = self.POP()
        if val.isnumeric():
            if float(val).is_integer():
                self.PUSH(operator.rshift(b, int(val)))
                return
        address_type , address = self.is_valid_address(val)
        if self.variables[address] == "NaN":
            self.error("variable uninitialized")
        if not address_type  == 'variable':
            self.error("Integer or variable expected")
        self.PUSH(operator.rshift(b, self.variables[address]))
        return 
       
    def SHL(self, val):
        b = self.POP()
        if val.isnumeric():
            if float(val).is_integer():
                self.PUSH(operator.lshift(b, int(val)))
                return
        address_type , address = self.is_valid_address(val)
        if self.variables[address] == "NaN":
            self.error("variable uninitialized")
        if not address_type  == 'variable':
            self.error("Integer or variable expected")
        self.PUSH(operator.lshift(b, self.variables[address]))
        return 
       
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

    def check_label(self, val):
        if val not in self.labels:
            self.error("Label Error")

    # Memory Access
    def LOAD(self, address):
        address_type, address = self.is_valid_address(address)
        if address_type == "variable":
            self.PUSH(self.variables[address])
            return
        elif address_type == "memory":
            self.PUSH(self.address[address])

    def STORE(self, address):
        a = self.POP()
        address_type, address = self.is_valid_address(address)
        if address_type == "variable":
            self.variables[address] = a 
            return
        if address_type == "memory":
            self.address[address] = a

    def is_valid_address(self, val):

        if val.startswith('@a'):
            raw_index = val.removeprefix('@a')  
            try:
                var_address = int(raw_index)
            except ValueError:
                self.error(f"Invalid variable address format: '{val}'")
            if var_address >= self.no_of_var:
                self.error("Stack overflow", "stack_overflow")    
            if var_address < 0:
                self.error("Stacl underflow")
            return ("variable", var_address)

    # Memory Address: *<index>
        if val.startswith('*'):
            raw_index = val.removeprefix('*') 
            try:
                mem_address = int(raw_index)
            except ValueError:
                self.error(f"Invalid memory address format: '{val}'")

            if mem_address >= self.stack_size:
                self.error("Stack overflow", "stack_overflow") 
            if mem_address < 0:
                self.error("Stack underflow")
        return ("memory", mem_address)

        self.error("Invalid memory or variable address")  


    def HALT(self):
        self.quit()

    def quit(self):
        print("Executed without error")
        print("Evaluated value: ", self.address[self.SP - 1], "at address", self.SP - 1)
        print("Stack")
        for i in range(len(self.address)):
            if i == self.SP - 1:
                print(f"[{i}]: --> {self.address[i]}")
            else:
                print(f"[{i}]: {self.address[i]}")

            
          
        print("output buffer: ", self.output_buffer)
        print("variables " , self.variables)
        sys.exit()
    
    def error(self, error_msg, code = None):
        disp = ''
        match code:
            case "stack_overflow": disp = f"Stack upto address {self.stack_size - 1} but accessing address{self.SP}"
            case "call_stack_overflow": ...
            case "call_stack_underflow": disp = f"RET executed on an empty call stack"


        print("Runt Error:" , error_msg,f":{disp}:","line", self.parsed_instructions[self.PC - 1][0] )
        sys.exit()
    #lexing and executing

class Execution(STACK_MACHINE):
    def __init__(self, parsed_instructions, size):
        super().__init__(size)
        self.parsed_instructions = parsed_instructions  
        self.no_of_instructions = len(self.parsed_instructions) 
        self.map_labels()
        self.execute()

    @property 
    def line_no(self):
        return self.parsed_instructions[self.PC][0]

    def map_labels(self):
        pos = 0
        while pos < self.no_of_instructions:
            instruction = self.parsed_instructions[pos]
            opcode = instruction[1]
            operand = instruction[2]
            if opcode == "label":
                if operand in self.labels:
                    self.error("Label already used")
                self.labels[operand] = pos
            pos += 1

    def execute(self):
        print("parsed_instructions: " ,self.parsed_instructions)
        while self.PC < self.no_of_instructions:
            instruction = self.parsed_instructions[self.PC]


            opcode = instruction[1]
            operand = instruction[2]
            self.PC += 1
            match opcode:
                #stack size is already initialized
                case "label":
                    pass
                    #self.check_label(operand)
                case "DUP":
                    self.DUP()
                case "JMP":
                    self.JMP(operand)
                case "JNZ":
                    self.JNZ(operand)
                case "JZ":
                    self.JZ(operand)
                case "CALL":
                    self.CALL(operand)
                case "RET":
                    self.RET()

                case "OVER":
                    self.OVER()

                case "STACK_SIZE":
                    pass 

                case "SWAP":
                    self.SWAP()

                case "POP":
                    self.POP()
                
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

                case "MOD":
                    self.MOD()

                case "AND":
                    self.AND()

                case "OR":
                    self.OR()

                case "XOR":
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
                    self.STORE(operand)

                case "HALT":
                    print("inside halt")
                    self.HALT()
                
                case _:
                    sys.exit(f"Invalid opcode: '{opcode}' found during execution")
     
if __name__ == "__main__":
    filename = get_filename(debugging = False)
    tokens = lexer(filename)
    parser_obj = Parser(tokens)
    instructions_list = parser_obj.parse()
    size = instructions_list[0][2]
    m = Execution(instructions_list, size)              

