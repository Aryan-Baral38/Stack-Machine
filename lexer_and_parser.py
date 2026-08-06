
# todo
# --write tests
# --test edge cases
#


'''
STEPS:
    lexing: -read raw file trims it(remove whitespaces) and turn it into a list of tokens
            - returns a list -> [token, token, ...]
    parsing: read the tokens and understand the code:
                - check for syntax errors
                - group the opcodes and operands
DEFINITIONS:

    token: a token is in the form (position, line_number, column_number, atom)
            -line and column numbers are from the code file

    atom: an atom is the smallest unit of the code, Types: opcodes and operands(numbers) eg: PUSH, POP,

    instruction: a single opcode with its valid operand. eg. PUSH 100

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

    #consume returns the atom
    def consume(self):
        parsing_token = self.current_token[3]
        if self.pos > self.no_of_tokens:
            self.error("Out of Bounds, token pointer greater than the no of tokens")

        self.pos += 1
        return parsing_token

    #returns the current token
    @property
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def error(self, error_msg):

        print("Error:", error_msg, "\nline",
               self.current_token[1], "col",
               self.current_token[2])

        sys.exit()

    def parse(self):

        #stores parsed result
        parsed_instructions = []

        #main loop
        while self.pos < self.no_of_tokens:
            #print("inside .parse() loop")
            token = self.current_token[3].upper()

            # stack_size is the first instrucion
            if self.pos == 0 and  token != "STACK_SIZE":
                #print("first token: ", token, self.tokens[self.pos], self.tokens[0])
                #print("first inst is stack_size")
                self.error('First instruction must be stack size, use "stack_size"')


            #-----------------------------------------------------------------------------------
            # stack_size must have an integer operand
            # -----------------------------------------------------------------------------------
            if token == "STACK_SIZE" :

                if self.stack_size_given == True or self.pos != 0:
                    self.error("Stack Size cannot be changed")

                if  not float(self.tokens[1][3]).is_integer():
                    self.error("Invalid Stack Size")

                if  self.stack_size_given == False:
                    parsed_instructions.append((self.tokens[0][3], self.tokens[1][3]))
                    self.pos += 2
                    self.stack_size_given = True
                    continue;
                else:
                    self.error("Stack invalid")

            # make sure all tokens here token must be an opcode
            if not token in all_operations:
                self.error("Opcode expected")

            #-----------------------------------------------------------------------------
            #handle opcodes that take operand
            # if current instruction takes operand, consume two tokens and
            #  check if the second token is digit
            #-----------------------------------------------------------------------------
            if token in input_operations:
                opcode = self.consume()
                operand = self.consume()
                if not operand.isdigit():
                    self.error("Digit expected")
                parsed_instructions.append((opcode, operand))

            #------------------------------------------------------------------------------
            #handle noinput_operations
            #-------------------------------------------------------------------------------

            elif token in noinput_operations:
                opcode = self.consume()
                parsed_instructions.append((opcode, None))
                if opcode == "HALT":
                    break
        #print("Token no: ", self.pos, "/", self.no_of_tokens)

        return parsed_instructions





def lexer():
    tokens = []
    #print("list of args: " , sys.argv)

    try:
        if (len(sys.argv) != 2):
            print("len of argv != 2")
            raise ValueError
        filename = sys.argv[1]

    except (ValueError):

        sys.exit("File read error")

    with open(filename, 'r') as file:
        line_no = 1
        token_pos = 1
        for line in file:
            line = line.strip()


            if not line == '':
                new_tokens = list(line.split(' '))
                print("line read: ", new_tokens)
                for i in range(len(new_tokens)):
                    tokens += [(token_pos,line_no, i + 1, new_tokens[i])]
                    token_pos += 1
            line_no += 1

        #print(tokens)
        return tokens


if __name__ == "__main__":
    tokens= lexer()

    print(tokens)

    #print("Lexed successfully")
    #print("tokens: " , tokens)

    parser_obj = Parser(tokens)
    #print("Parser object created")
    #print(all_operations)
    final_instructions = parser_obj.parse()
    print("\n Parsed instrucions: ", final_instructions)

