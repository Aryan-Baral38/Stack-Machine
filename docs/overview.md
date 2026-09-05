#Overview

The following is a high level overview of how this language works. It documents the execution pipeline. For the architecture and instruction set, view the specs.md file  

---

##Lexing

* Lexing is the first step of the process.
* The input code is used to create a stream of tokens with whitespace and comments removed.
* A **Token** is of the form (atom_number, line_number, column_number, atom).
* **Atom**: smallest unit of the language, Types: opcodes eg. ```PUSH```, ```POP``` and operands(numbers). 
* **Instruction**: an opcode with its valid operand. eg. ```PUSH 100``` (in user code), after parsing -> ```("PUSH", 100)```.
* Lexer returns a list -> ``` [token, token, ... ]```.

---

##Parsing

* The parser reads the tokens and understand the code:
* Check for syntax errors.
* Checks if the operands are valid.
* Throw "Parse Error" errors
* The parser returns a list of tuple containing opcodes and corresponfing operands: ```[(opcodes, operand), ... ]``` eg. ```[("PUSH", 10), ("POP", None), ... ]```.

--- 

##Execution

* The execution part or the VM receives a list of tuple containing parsed instructions ```[..., (opcode,operand), ...]```.
* It goes through each element of the parsed instruciton list and calls the corresponding function with arguments (if any).
* These funcitons then do some error checking and finally perform the  specified operations.
* Any errors that occur during this phase here are called "Exec Error".
    


