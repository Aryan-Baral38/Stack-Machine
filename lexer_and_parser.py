
# todo
# --write tests
# --test edge cases
#

'''
DEFINITIONS:

    token: result of lexing, a tuple (atom_number, line_number, column_number, atom)
            -line and column numbers are from the code file

    atom: smallest unit of the language, Types: opcodes and operands(numbers) eg: PUSH, POP

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

import sys
#opcodes---------------------------------------------------------]
#set of opcodes

#these operations do not require operands
noinput_operations = {"ADD", "SUB", "MUL", "DIV", "GT", "GE",
                      "LT", "LE", "EQ", "MOD", "AND", "OR",
                      "XOR", "NOT", "INR", "DCR", "SWAP", "OVER",
                      "DUP", "POP",  "HALT"}

#these operations require operand
input_operations = {"SHR", "SHL", "LOAD", "STORE", "PUSH", "STACK_SIZE"}
all_operations = set.union(noinput_operations, input_operations)

'''
    the parser will read a list of [ tokens ] are return a list of tuples [ (opcode, operand(s) ],
    most operations dont have an operand
'''
def lexer():
    tokens = []
    #print("list of args: " , sys.argv)
    debugging = 1
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
        match code:

            case "None":
                disp = ''
            case "throw_atom":
                disp = f" '{self.current_token[3]}' "
            case "throw_previous":
                disp = f" '{self.previous()}' "
            case "too_many_operands":
                disp = f" ({self.previous_atom} {self.current_atom}) "
            case "for_previous":
                disp = f" for '{self.previous_atom}' "
            case "for_current":
                disp = f" for '{self.current_token[3]}' "

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

    def parse(self):

        #stores parsed result
        parsed_instructions = []

        #main loop
        while self.pos < self.no_of_tokens:
            #print("inside .parse() loop")
            atom = self.current_token[3].upper()

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
                    parsed_instructions.append((size_opcode, stack_size))
                    self.stack_size_given = True
                    continue;
                else:
                    self.error("Stack invalid", "throw_atom")

            # make sure all tokens here token must be an opcode
            if not atom in all_operations:
                if self.previous_atom.upper() in input_operations:
                    self.error("Expected an operand after",  "throw_previous" )
                if atom.isdigit():
                    if self.previous_atom.isdigit():
                        self.error("Too many operands", "too_many_operands")
                    if self.previous_atom in noinput_operations:
                        self.error("Unwanted Operand")
                self.error("Invalid Opcode")

            #-----------------------------------------------------------------------------
            #handle opcodes that take operand
            # if current instruction takes operand, consume two tokens and
            #  check if the second token is digit
            #-----------------------------------------------------------------------------
            if atom in input_operations:
                #print("current token: ", self.current_token, atom)

                if not self.peek().isdigit():
                    self.error("Operand invaid or missing", "for_current" )

                opcode = self.consume()
                #print("current token: ", self.current_token, atom)


                operand = self.consume()
                #print("current token: ", self.current_token, atom)
                if not operand.isdigit():
                    self.error("Digit expected")
                parsed_instructions.append((opcode, operand))

            #------------------------------------------------------------------------------
            #handle noinput_operations
            #-------------------------------------------------------------------------------

            elif atom in noinput_operations:
                if atom == "HALT":
                    self.consume()
                    break
                next_atom = self.peek()
                if next_atom.isnumeric():
                    sys.error("Unwanted operand: ", "throw_atom")

                opcode = self.consume()
                parsed_instructions.append((opcode, None))
                if opcode == "HALT":
                    break
        #print("Token no: ", self.pos, "/", self.no_of_tokens)

        return parsed_instructions



if __name__ == "__main__":
    tokens= lexer()

    #print(tokens)

    #print("Lexed successfully")
    #print("tokens: " , tokens)

    parser_obj = Parser(tokens)
    #print("Parser object created")
    #print(all_operations)
    final_instructions = parser_obj.parse()
    print("\nParsed instrucions: ", final_instructions)

