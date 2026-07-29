#Files

import sys
#opcodes---------------------------------------------------------]
#set of opcodes

#these operation dont require user input
noinput_operations = {"ADD", "SUB", "MUL", "DIV", "GT", "GE",
                      "LT", "LE", "EQ", "MOD", "AND", "OR",
                      "XOR", "NOT", "INR", "DCR", "SWAP", "OVER",
                      "DUP", "POP", "STACK_SIZE", "HALT"}

#these operations require user inputs
input_operations = {"SHR", "SHL", "LOAD", "STORE", "PUSH", "LOAD", "STORE"}
all_operations = set.union(noinput_operations, input_operations)

'''
    the parser will read a list of [ tokens ] are return a list of tuples [ (opcode, operand) ], 
    most operations dont have an operand
'''


class Parser:


    def __init__(self, tokens, token_locations):

        #location of token in the text file, used for displaying error 
        self.token_locations = token_locations              
        self.tokens = tokens
        self.no_of_tokens = len(tokens)
        
        #position in the list of tokens
        self.pos = 0
        
        #When used for anything other than temporary storage, this always has an opcode,
        self.current_token = tokens[self.pos]
        
        #to prevent changing stack size after initilaizaion
        self.stack_size_given = False

    def parse(self):

        
        #stores the result of parsing
        parsed_instructions = []

        #main loop
        while self.pos <= self.no_of_tokens:
            token = self.current_token.upper()

            # stack_size is the first instrucion and the second token must be int
        
            if not tokens[0] == "stack_size":
                self.error('First instruction must be stack size, use "stack_size size"')           

            if not token in all_operations:
                self.error("Opcode expected")
                
            if token == "stack_size" :
                if self.consume().is_integer() and self.stack_size_given == 0:
                    parsed_instructions.append((token, tokens[1]))
                    self.pos += 2
                    self.stack_size_given = True
                elif self.stack_size_given == True:
                    self.error("Stack size cannot be changed")
                else:
                    self.error("Invalid")

            #----------------------------------------------------------------------------- 
            #handle  input_operations 
            #----------------------------------------------------------------------------- 
            # if current instruction takes immediate input, consume two tokens and
            #  check if the second token is an integer  
        #
            if token in input_operations:
                opcode = token.consume()
                user_input = token.consume()
                if not user_input.is_integer():
                    self.error("Integer expected") 
                parsed_instructions.append((opcode, user_input))
            
            #------------------------------------------------------------------------------ 
            #handle noinput_operations 
            #-------------------------------------------------------------------------------
            
            if token in input_operations:
                opcode = token.consume()
                user_input = token.consume()
                if not user_input.is_integer():
                    self.error("Integer expected")
        print("Token no: ", self.pos, "/", self.no_of_tokens)
    
        return parsed_instructions


    def consume(self):
        parsing_token = self.current_token
        if not self.pos <= self.no_of_tokens:
            sys.exit("Out of Bounds")
        
        self.pos += 1
        return parsing_token
        

    def error(self, error_msg):
        print("Error:", error_msg, "\nline", self.token_locations[self.pos][0], "column",
              self.token_locations[self.pos][1])
        sys.exit()
        

def lexer():
    tokens = []
    try:
        if (len(sys.argv) != 2):
            raise ValueError
        filename = sys.argv[1]

    except (ValueError):
        print("File read error")

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
        
 
tokens,token_locations = lexer()
#print(token_locations)
parser_obj = Parser(tokens,token_locations)
print(all_operations)
final_instructions = parser_obj.parse()
print("\n final instrucions: ", parsed_instructions)

