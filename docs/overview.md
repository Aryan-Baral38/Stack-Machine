-Once the code is written, a few steps happen before a result is outputted.  
#lexing
First is lexing. The input code is used to create a stream of tokens with whitespace and comments removed,
    of the form (atom_number, line_number, column_number, atom).
  atom: smallest unit of the language, Types: opcodes eg. PUSH, POP and operands(numbers) 
  instruction: an opcode with its valid operand.
      eg. PUSH 100 (in user code), after parsing -> ("PUSH", 100)
  lexer returns a list -> [token, token, ... ]

#parsing
read the tokens and understand the code:
                - check for syntax errors
                - throw "Parse Error" errors
                - return [(opcodes, operand), ... ] eg. [("PUSH", 10), ("POP", None), ... ]
#Execution
The execution part of the program receives a list of tuple containing parsed instructions [..., (opcode,operand), ...]
    which goes through each element of the parsed instruciton list and calls the corresponding function with arguments (if any
    these funcitons then do some error checking and finally perform the operations specified.
    Any errors here are called "Exec Error".
    


