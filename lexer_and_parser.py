# todo 
# --write tests 
# --test edge cases 
# 

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


    def __init__(self, tokens, token_locations):

        #location of token in the text file, used for displaying error
        self.token_locations = token_locations
        self.tokens = tokens
        self.no_of_tokens = len(tokens)

        #current position in the list of tokens
        self.pos = 0

        #When used for anything other than temporary storage, this always has an opcode,
        self.current_token = self.tokens[self.pos]

        #to prevent changing stack size after initilaizaion
        self.stack_size_given = False

    def parse(self):
        print("Inside .parse() method")

        #stores parsed result
        parsed_instructions = []

        #main loop

        while self.pos < self.no_of_tokens:
            #print("inside .parse() loop")
            token = self.current_token_method().upper()

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

                if  not float(self.tokens[1]).is_integer():
                    self.error("Invalid Stack Size")

                if  self.stack_size_given == False:
                    parsed_instructions.append((self.tokens[0], self.tokens[1]))
                    self.pos += 2
                    token = self.tokens[self.pos]
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

    def current_token_method(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        parsing_token = self.tokens[self.pos]
        if self.pos > self.no_of_tokens:
            sys.exit("Out of Bounds")

        self.pos += 1
        return parsing_token


    def error(self, error_msg):
        print("Error:", error_msg, "\nline", self.token_locations[self.pos][0], "column",
              self.token_locations[self.pos][1])
        sys.exit()


def lexer():
    tokens = []
    print("list of args: " , sys.argv)

    try:
        if (len(sys.argv) != 2):
            print("len of argv != 2")
            raise ValueError
        filename = sys.argv[1]

    except (ValueError):

        sys.exit("File read error")

    with open(filename, 'r') as file:
        token_locations = []
        line_no = 1
        token_pos = 0
        for line in file:
            line = line.strip()

            for i in line:
                if i.isnumeric():
                    i = float(i)

            if not line == '':
                new_tokens = list(line.split(' '))
                for i in range(len(new_tokens)):
                    token_locations += [(line_no, i, token_pos, new_tokens[i])]
                    token_pos += 1
                tokens += new_tokens
            line_no += 1


        print(tokens)
        return tokens, token_locations


if __name__ == "__main__":
    tokens,token_locations = lexer()
    #print("Lexed successfully")
    print("tokens: " , tokens)
    parser_obj = Parser(tokens,token_locations)
    #print("Parser object created")
    #print(all_operations)
    final_instructions = parser_obj.parse()
    print("\n Parsed instrucions: ", final_instructions)
