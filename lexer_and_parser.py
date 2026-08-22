#aa
# todo
# --write tests
# --test edge cases
#

'''
DEFINITIONS:

    token: result of lexing, a tuple (atom_number, line_number, column_number, atom)
            -line and column numbers are from the code file

    atom: smallest unit of the language, Types: opcodes eg. PUSH, POP and operands(numbers) 

    instruction: an opcode with its valid operand.
      eg. PUSH 100 (in user code), after parsing -> ("PUSH", 100)

STEPS:
    lexing: -reads raw file, trims it(remove whitespaces)
            - returns a list -> [token, token, ... ]
    parsing: read the tokens and understand the code:
                - check for syntax errors
                - throw compiletime errors
                - return [(opcodes, operand), ... ] eg. [("PUSH", 10), ("POP", None), ... ]

IMPORTANT PATTERNS:
    -calling peek() after consume() is forbidden, peek()-ing next token
      and its validation must be done BEFORE calling consume() on current token

'''
import re
import sys
#opcodes---------------------------------------------------------]
#set of opcodes

#these operations do not require operands
noinput_operations = {"ADD", "SUB", "MUL", "DIV", "GT", "GE",
                      "LT", "LE", "EQ", "MOD", "AND", "OR",
                      "XOR", "NOT", "INR", "DCR", "SWAP", "OVER",
                      "DUP", "POP",  "HALT"}

#these operations require operand
input_operations = {"SHR", "SHL", "PUSH", "STACK_SIZE"}
address_input_operation = {"STORE", "LOAD" }
all_operations = set.union(noinput_operations, input_operations, address_input_operation)


'''
    the parser will read a list of [ tokens ] are return a list of tuples [ (opcode, operand(s) ],
    most operations dont have an operand
'''

def get_filename(debugging = False):
   #print("list of args: " , sys.argv)
    filename = 'None'
    
    if not debugging:
        try:
            if (len(sys.argv) != 2):
                print("len of argv != 2")
                raise ValueError
            filename = sys.argv[1]

        except (ValueError):
            sys.exit("File read error")
    else:
        ## __________!! TEST ONLY !!______________
        # for debugging
        filename = "/workspaces/175494904/conj/testcode1.txt"
        #filename = "testcode2.txt"
        ##________________________________________
    if not filename == "None":
        return filename

def lexer(filename):
    tokens = []
 
    with open(filename, 'r') as file:
        line_no = 1
        token_pos = 0
        for line in file:
            line = line.strip()

            if not line == '':
                new_tokens = list(line.split(' '))
                #print("line read: ", new_tokens)
                for i in range(len(new_tokens)):
                    tokens += [(token_pos,line_no, i + 1, new_tokens[i])]
                    token_pos += 1
            line_no += 1

        #print(tokens)
        return tokens


class Parser:

    def __init__(self, tokens):
        # "atom" is the actual words form the code

        #single token format: (token_no, line_no, col_no, atom)
        self.tokens = tokens
        self.no_of_tokens = len(tokens)

        #current position in the list of tokens
        self.pos = 0

        #to prevent changing stack size after initilaizaion
        self.stack_size_given = False
        self.stack_size = 0

    #returns an atom and advance the position
    def consume(self):
        #print("Position before consuming:", self.pos)
        parsing_atom = self.current_token[3]
        if self.pos > self.no_of_tokens:
            self.error("Out of Bounds, token pointer greater than the no of tokens")

        self.pos += 1
        #print("Position after consuming:", self.pos)
        return parsing_atom

    #returns the current token(not atom)
    @property
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    @property
    def current_atom(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][3]

    def error(self, error_msg, code = "None"):
        disp = ''
        match code:

            case "None":
                disp = ''

            case "throw_atom":
                disp = f" '{self.current_atom}' "

            case "throw_previous":
                disp = f" '{self.previous_atom}' "

            case "too_many_operands":
                disp = f" ({self.previous_atom} {self.current_atom}) "

            case "for_previous":
                disp = f" for '{self.previous_atom}' "

            case "for_current":
                disp = f" for '{self.current_atom}' "

            case "no_halt":
                disp = ''

            case "var_not_int":
                disp = "use @a[integer_address]"

            case "non_numeric_address":
                disp = "addresses must be integer values"

            case "missing_address_specifier":
                disp = "use prefix * for memory address or @a for variable address"


        print("Error:", error_msg,f":{disp}:","on", "line",
               self.current_token[1], "col",
               self.current_token[2])

        sys.exit()

    #returns the next atom
    def peek(self):
        if self.pos < self.no_of_tokens:
            return self.tokens[self.pos + 1][3]
        return None
    @property
    def previous_atom(self):
        if self.pos > 0:
            return self.tokens[self.pos - 1][3]
    
    def opcode_recognized(self):
        atom = self.current_token[3]
        if not atom in all_operations:
            if self.previous_atom.upper() in input_operations:
                self.error("Expected an operand after",  "throw_previous" )
            if atom.isdigit():
                if self.previous_atom.isdigit():
                    self.error("Too many operands", "too_many_operands")
                if self.previous_atom in noinput_operations:
                    self.error("Unwanted Operand")
            self.error("Invalid Opcode")


    def parse(self):
        if not "HALT" in [x[3] for x in self.tokens]:
            sys.exit("Error: Halt not found : No 'HALT': specify end of program with 'HALT' ")
        #stores parsed result'''
        parsed_instructions = []

        #main loop
        while self.pos < self.no_of_tokens:
            #print("inside .parse() loop")
            atom = self.current_token[3].upper()
            line_no = self.current_token[1]
            print("curent atom: ", atom) 
            # stack_size is the first instrucion
            if self.pos == 0 and  atom != "STACK_SIZE":
                #print("first token: ", token, self.tokens[self.pos], self.tokens[0])
                #print("first inst is stack_size")
                self.error('First instruction must be stack size, use "stack_size"',)


            #-----------------------------------------------------------------------------------
            # stack_size must have an integer operand
            # -----------------------------------------------------------------------------------
            if atom == "STACK_SIZE" :

                if self.stack_size_given == True or self.pos != 0:
                    self.error("Stack Size cannot be changed", "throw_atom")

                if not float(self.peek()).is_integer():
                    self.error("Invalid Stack Size", "throw_atom")

                if  self.stack_size_given == False:
                    size_opcode = self.consume().upper() # should be "STACK_SIZE"
                    stack_size = self.consume()          #some int value
                    parsed_instructions.append((line_no,size_opcode, int(stack_size)))
                    self.stack_size_given = True
                    self.stack_size = int(stack_size)
                    continue;
                else:
                    self.error("Stack invalid", "throw_atom")

            self.opcode_recognized()
            #-----------------------------------------------------------------------------
            '''
            # handle opcodes that take operand
            # if current instruction takes operand, consume two tokens and
            #  check if the second token is digit
            #-----------------------------------------------------------------------------
            '''
            if atom in input_operations:
                #print("current token: ", self.current_token, atom)
                ''' Handle variable operand
                        variable addresses are returned as str
                '''
                matches = re.search(r"^@a(\d+)$",self.peek()) 
                if matches:
                    opcode = self.consume()
                    if not float(matches.gorup(1)).is_integer():
                        self.error("Invalid variable name", "var_not_int")
                    var_address = self.consume()
                    parsed_instructions.append((line_no,opcode, var_address))
                    continue

                if not self.peek().isdigit():
                    self.error("Operand invaid or missing", "for_current" )

                opcode = self.consume()
                #print("current token: ", self.current_token, atom)


                operand = self.consume()
                #print("current token: ", self.current_token, atom)
                if not operand.isdigit():
                    self.error("Digit expected")
                '''Direct values are stored as floats'''
                parsed_instructions.append((line_no,opcode, float(operand)))

            #------------------------------------------------------------------------------
            #handle noinput_operations
            #-------------------------------------------------------------------------------

            if atom in noinput_operations:
                #current atom is already valid so we consume it
                opcode = self.consume()
                if opcode == "HALT":
                    parsed_instructions.append((line_no,atom, 'None'))
                    break
                #after consumng, we are already at the next atom 
                next_atom = self.current_atom
                if next_atom  not in all_operations:
                    self.error(f"'{next_atom} is invalid'")
                parsed_instructions.append((line_no,opcode, None))
                continue
            """
                for distinguishing them during execution:
                    memory addresses are stored as integers type
                    var_addresses are stored as str types 
            """
            if atom in address_input_operation:
                #memory addresses must start with *. eg: STORE *100
                next_token = self.peek()
                print("peeked")
                matches = re.search(r"^@a(\d+)$", next_token)
                if matches:
                    print("matched1")
                    opcode = self.consume()
                    var_address = matches.group(1)
                    if not float(var_address).is_integer():
                        self.error("Invalid variable name", "var_not_int")
                    var_address = self.consume()
                    parsed_instructions.append((line_no,opcode, var_address))
                    continue
                matches = re.search(r"^(\*)(\d+)$",next_token)
                if matches:
                    address = matches.group(2)
                    #print("address:", address)
                    #print("stack size", self.stack_size, type(self.stack_size))

                    if not float(address).is_integer():
                        self.error("Integer value expected")
                    address = int(address)
                    if (address) > self.stack_size:
                        self.error("address larger than stack")

                    opcode = self.consume()
                    mem_address = self.consume() #
                    parsed_instructions.append((line_no,opcode,mem_address))
                    continue

                if not next_token.isnumeric():
                    self.error("Invalid memory address or variable", "non_numeric_address")
                if float(next_token).is_integer():
                    self.error(f"Missing variable or address specifier", "missing_address_specifier")
                self.error("Invalid operand error")                

        
        def is_valid_var(self, next_token):
            matches_var_address = re.search(r"^@a(\d+)$", next_token)
            matches_mem_address = re.search(r"^\*(\d+)$", next_token)
            if matches_var_address:
                opcode  = self.consume()
                if not float(matches.gorup(1)).is_integer():
                    self.error("Invalid variable name", "var_not_int")
                var_address = self.consume()
                return (True, int(matches.group(1)))
                
        
           
        return parsed_instructions



if __name__ == "__main__":
    file = get_filename(debugging = 0)

    tokens= lexer(file)

    #print(tokens)

    #print("Lexed successfully")
    #print("tokens: " , tokens)

    parser_obj = Parser(tokens)
    #print("Parser object created")
    #print(all_operations)
    final_instructions = parser_obj.parse()
    print("\nParsed instrucions: ", final_instructions)

