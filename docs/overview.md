# Overview

The following is a high level overview of how this language works. It documents the execution pipeline. For the architecture and instruction set, view the specs.md file.

```Source code --> [Lexer] --> tokens --> [Parser] --> Instructions --> [VM] --> output ```
---

## Lexing

* Lexing is the first step of the process.
* The input code is used to create a stream of tokens with whitespace and comments removed.
* A **Token** is of the form (atom_number, line_number, column_number, atom).
* **Atom**: smallest unit of the language, Types: opcodes eg. ```PUSH```, ```POP``` and operands(numbers). 
* **Instruction**: an opcode with its valid operand. eg. ```PUSH 100``` (in user code), after parsing -> ```("PUSH", 100)```.
* Lexer returns a list -> ``` [token, token, ... ]```.

---

## Parsing

* The parser reads the tokens and understand the code.
* It  checks for syntax errors.
* For instructions that expect operand, the parser checks whether an operand is given or not, as well as its validity. 
* Any error that is found in this phase is called "Parse Error".
* The parser returns a list of tuple containing opcode and (if any) its corresponding operand: ```[(opcodes, operand), ... ]``` eg. ```[("PUSH", 10)```, ```("POP", None), ... ]```.
* Instructions that dont take any arguments have ```None``` in the operand.
* Parser also returns labels in the form ```(label, <label_name>)```. 

--- 

## Execution

* The execution part or the VM receives a list of tuple containing parsed instructions ```[..., (opcode,operand), ...]```.
* The first step of execution phase is mapping of the labels in `parsed_instrucitons` using a dictionary so that the machine knows exactly where a lable is and is able to jump to labels if necessary.
* Each label is mapped to its corresponding index in `parsed_instruction`. When a jump statement to a label is called, the program counter jumps to the location just after the lable and continues.
* After labels are mapped the VM interpreter goes through each element of the parsed instruciton list and calls the corresponding function with arguments (if any).
* These funcitons then do some error checking and finally perform the  specified operations.
* Any error that is found in this phase here is called "Exec Error".


