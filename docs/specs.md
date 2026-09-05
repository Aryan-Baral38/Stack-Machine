# Stack Machine Specifification and Instructions 
--- 

## Architecture

The core execution engine `STACK_MACHINE` in `stack_machine.py` emulates a machine with a stack on which various operations can be executed.
* `parsed_instruction`: This list is the output of the parsing phase. Each element of this list is a tuple `(opcode, operand)`.
* **Stack Pointer** `SP`: Points to the top of the stack, specifically the next available memory location of the stack.
* **Program Counter** `PC`: Tracks the index of the instruction currently executing form the list `parsed_instruction` (returned by the parser). The `PC` is updated to the next instruction immediately after the current instruciton is read form `parsed_instruction` , before the current instruction is even executed.
* **Evaluation Stack** `address`: Fixed sized array used for intermediate computation.
* **Call Stack** `call_stack`: Tracks the return addresses for subroutine(function) execution (`CALL`, `RET`).When `CALL`ed,  After `RET`, the top value of `call_stack` is stored in  `PC`. The return address is the next immediate index in `parsed_instruction`. 
* **Variables** `variables`: For persistent storage that, can be accessed using `'@a'` addressing. eg: `PUSH @a1`. 

---

## Addressing modes

* **Immediate addressing**: Values are passed directly in the code. eg: `PUSH 12`.
* **Variable addressing**: Operates on the variables using `@a` to address variables. eg: `PUSH @a1`, `STORE @a2`.
* **Direct memory addressing**: Access the exact address on the evaluation stack using `*<mem_address>` addressing. eg: `PUSH *12`, `STORE *10`.

--- 

# Instruction Set 
 
## Stack Manipulation

### `PUSH val`
* `val` can be a literal, a variable(`@a<address>`) or memory address (`*<address>`)
* Pushes val onto the evaluation stack.

### `POP`
* Removes the value on the top of the stack.

### `DUP`
* Duplicates the top value of the evaluation stack.

### `SWAP`
* Exchanges the position of the top two elements on the stack.

### `OVER`
* Copies the second item from the top and pushed it onto the stack.
* Eg:
```
instruction     stack
---
PUSH 10        ->[10]
PUSH 20        ->[10, 20]
SWAP           ->[20, 10]
DUP            ->[20, 10, 10]
POP            ->[20, 10]
OVER           ->[20, 10, 20]
```

## ARITHEMATIC AND LOGICAL OPERATIONS

### BINARY OPERATIONS
* Includes `ADD`, `SUB`, `MUL`, `DIV`, `MOD`.
* Pop the top two vlues and perfrom binary opertion on them, If  stack is [..., b, a]` then it pops `a` and `b` then, perfoms `a (bin) b` and push the value.
* Eg:
```
Instruction    stack
PUSH 12       ->[12]
PUSH 10       ->[12, 10]
ADD           ->[22]
PUSH 20       ->[22, 20]
SUB           ->[-2]
```

### BITWISE AND BOOLEAN
* Performs operations bitwise and takes no arguments.
* Includes `AND`, `OR`, `XOR`, `NOT`, `SHL`,`SHR`.
* `AND`, `OR`, `XOR` pops the top two values and perform bitwise boolean operations and pushes the result.
* `NOT` performs bitwise NOT operation on the top element of stack.
* `SHL` and `SHR` performs bitwise left shift and right shift respectively.
* Eg:
```
instruction    stack 
PUSH 10       ->[10]
PUSH 12       ->[10, 12]
GE            ->[1]
```

### COMPARISIONS
* Includes `EQ` (equal), `LT` (less than), `GT` (greater than) (Pops top 2 values and pushes a 1 or 0 boolean)

## MEMORY ACCESS
* Includes instructions to load form or store to persistent memory as well as random access to the evaluation stack.



