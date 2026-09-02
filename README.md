# Stack Machine

A lightweight, stack-based programming language and virtual machine written in Python. It features a simple instruction set, zero-register architecture, label-based control flow, subroutine calls, and precise error reporting with line and column tracking.

---

## Key Features

* **Stack-Based Virtual Machine:** Pure zero-register stack architecture utilizing a dedicated Data Stack for evaluation and a Call Stack for function.
* **Rich Instruction Set:** Built-in operations for stack manipulation (`DUP`, `SWAP`, `PUSH`, `POP`), arithmetic (`ADD`, `SUB`, `MUL`, `DIV`, `MOD`), and bitwise/logical evaluation.
* **Control Flow & Labels:** Unconditional (`JMP`) and conditional branching (`JZ`, `JNZ`) using human-readable label pointers (`<LABEL>`).
* **Variables & Memory Addressing:** Support for local stack variables (`@a0`, `@a1`) and direct memory pointer manipulation (`*addr`).
* **Function Subroutines:** Function calls (`CALL <LABEL>`, `RET`) supporting recursive execution.
* **Precise Error Reporting:** Comprehensive compile-time and runtime error diagnostics complete with line number and column index.

---

## Quick Start

### Installation

Clone the repository and ensure you have Python 3.10+ installed:

```bash
git clone [https://github.com/Aryan-Baral38/stack-machine.git]
cd stack-machine
```

### First Program 
In add.txt file type this:
```
stack_size 10
PUSH 10 
PUSH 5 
ADD 
HALT
```


```
```
```
