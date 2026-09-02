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
    -helper functions cannot cause destructive changes like consuming tokens.
    -calling peek() after consume() is forbidden, peeking next token
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
control_flow = {"JMP", "JZ", "JNZ"}
subroutine = {"CALL", "RET"}
address_input_operation = {"STORE", "LOAD" }
all_operations = set.union(noinput_operations, input_operations,
                           address_input_operation, control_flow,
                           subroutine)

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
 
    if not filename.endswith('.txt'):
        sys.exit("Enter filename.txt as file")
        
    with open(filename, 'r') as file:
        line_no = 1
        token_pos = 0
        for line in file:
            line = line.strip()
            

            if not line == '':
                new_tokens = list(line.split())
                #print("line read: ", new_tokens)
                for i in range(len(new_tokens)):
                    tokens += [(token_pos,line_no, i + 1, new_tokens[i].upper())]
                    token_pos += 1
            line_no += 1

        #print(tokens)
        return tokens

class Parser:

    def __init__(self, tokens):
        #single token format: (token_no, line_no, col_no, atom)
        self.tokens = tokens
        self.no_of_tokens = len(tokens)
        self.pos = 0
        #to prevent changing stack size after initilaizaion
        self.stack_size_given = False
        self.stack_size = 0

    #returns an atom and advance the position
    def consume(self):
        if self.pos > self.no_of_tokens:
            self.error("Out of Bounds, token pointer greater than the no of tokens")
        parsing_atom = self.current_token[3]
        self.pos += 1
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
                disp = 'Add "HALT" to exit the program'

            case "var_not_int":
                disp = "use @a[integer_address]"

            case "non_numeric_address":
                disp = "addresses must be integer values"

            case "missing_address_specifier":
                disp = "use prefix * for memory address or @a for variable address"

        print("Compt Error:", error_msg,f":{disp}:","on", "line",
               self.current_token[1], "col",
               self.current_token[2])

        sys.exit()

    #returns the next atom
    def peek(self):
        if self.pos + 1< self.no_of_tokens:
            return self.tokens[self.pos + 1][3]
        return None
    @property
    def previous_atom(self):
        if self.pos > 0 and self.pos <= self.no_of_tokens:
            return self.tokens[self.pos - 1][3]
        return None
    
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

    def is_label(self, atom):
        matches = re.search(r"^<([\w]+)>$", atom)
        if matches:
            return (True, matches.group(1))
        matches = re.search(r"^(<.+>|<.+|.+>|<>)",atom)
        if matches:
            self.error(f"Invalid label name {matches.group(1)}")
        return (False, None)

    def is_valid_address(self, token):
        if not token:
             return ("invalid", None)
        
        matches_var = re.search(r"^@a|A(\d+)$", token)
        matches_mem = re.search(r"^\*(\d+)$", token)

        if matches_var:
            return ("var", int(matches_var.group(1)))
        elif matches_mem:
            return ("mem", int(matches_mem.group(1)))
        else:
            return ("invalid", None)



    def parse(self):
        if not "HALT" in [x[3] for x in self.tokens]:
            self.error("HALT not found", "no_halt")
        parsed_instructions = []

        #main loop
        while self.pos < self.no_of_tokens:
            atom = self.current_token[3].upper()
            line_no = self.current_token[1]
            #print("curent atom: ", atom) 
            # stack_size is the first instrucion
            if self.pos == 0 and  atom != "STACK_SIZE":
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

            is_a_label, label = self.is_label(atom)
            if is_a_label:
                #comsume label, consume is called only once 
                self.consume()
                parsed_instructions.append((line_no, "label", label))
                continue
            self.opcode_recognized()

            if atom in subroutine:
                if atom == "CALL":

                    is_a_label, label = self.is_label(self.peek())
                    if is_a_label:
                        opcode = self.consume()
                        self.consume()
                        parsed_instructions.append((line_no, opcode, label))
                    else:
                        self.error("Expected a label <label>")
                elif atom == "RET":
                    opcode = self.consume()
                    parsed_instructions.append((line_no, opcode, None))

            if atom in control_flow:
                is_a_label, label = self.is_label(self.peek())
                if is_a_label:
                    opcode = self.consume()
                    _ = self.consume()
                    parsed_instructions.append((line_no, opcode, label))
                else:
                    self.error("Expected a label <label>")
                continue
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
                next_atom = self.peek()
                addr_type, address = self.is_valid_address(next_atom)
                if addr_type == "var":
                    opcode = self.consume()
                    var_address = self.consume()
                    parsed_instructions.append((line_no, opcode, var_address))
                    continue
                
                if not next_atom.isnumeric():
                    self.error("Operand invaid or missing", "for_current" )

                opcode = self.consume()
                operand = self.consume()
                #print("current token: ", self.current_token, atom)
                if not operand.isdigit():
                    self.error("Digit expected")
                '''Direct values are stored as floats'''
                parsed_instructions.append((line_no,opcode, float(operand)))
                continue

            #------------------------------------------------------------------------------
            #handle noinput_operations
            #-------------------------------------------------------------------------------

            if atom in noinput_operations:
                #current atom is already valid so we consume it
                opcode = self.consume()
                if opcode == "HALT":
                    parsed_instructions.append((line_no,atom, None))
                    continue
                #after consumng, we are already at the next atom 
                if self.current_atom is None:
                    break
                next_atom = self.current_atom
                if next_atom  not in all_operations and not self.is_label(next_atom)[0]:
                    self.error(f"'{next_atom}' is invalid")
                parsed_instructions.append((line_no,opcode, None))
                continue
            """
                for distinguishing them during execution:
                    memory addresses are stored as integers type
                    var_addresses are stored as str types 
            """
            if atom in address_input_operation:
                #memory addresses must start with *. eg: STORE *100
                next_atom = self.peek()
                #print("peeked")
                address_type, address = self.is_valid_address(next_atom)
                if address_type in ("var", "mem"):
                    opcode = self.consume()
                    address = self.consume()
                    parsed_instructions.append((line_no, opcode, address))
                    continue
                else:
                    if not next_atom.isnumeric():
                        self.error("Invalid memory address or variable format" )
                    if float(next_atom).is_integer():
                        self.error(f"Missing variable(@a) or address(*) specifier", "missing_address_specifier")
                    self.error("Invalid operand error") 

        return parsed_instructions

if __name__ == "__main__":
    file = get_filename(debugging = 0)
    tokens= lexer(file)
    parser_obj = Parser(tokens)
    final_instructions = parser_obj.parse()
    #print("\nParsed instrucions: ", final_instructions)

