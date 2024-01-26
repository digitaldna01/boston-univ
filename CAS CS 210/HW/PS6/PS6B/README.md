[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/SJXfFfYz)
# The C Calculator

**You may - and are encouraged to - complete this assignment in teams of two**

Now that we have written a version of the Calculator in assembly, we will
use a version in C to learn and explore C.  In particular, we have given
you the source code for a C version but throughout the code are
statements that cause it to crash.  At each crash, in the source code, are
some hints on what you need to study and explore to fix the crash.

The more fixes you make, the more points you will score.

## What you are given

You have been provided with:
  - c files : each c file gets translated into an assembly file which then is converted into
    an object file and finally all the object files get linked into executables.  There is
    one executable for each data file (same as the assembly version)
  - Makefile : that builds all the binaries from the source.  This make file illustrates some
    more advanced makefile techniques.  While you won't need to modify it, it contains
    lots of comments so that you can see how we use make in more powerful ways.
  - data : the directory containing all the data files from the assembly version with 2 new data files
    to test the three additional calculator commands -- see section below 'New Calculator Commands'
  - testcalc.sh : as before, it is a test script.  However, I recommend that you first follow the steps
    in 'Getting started' rather than just running the test script.
  - setup.gdb : a gdb setup file that you can use to make your life in gdb easier.
    See the section below on gdb and C

## Getting started

1) The first thing to do is study ccalc.c.  There are a lot of comments in it to guide
your learning.  
2) Once you have an idea of how the main function works. You can use the provided Makefile to build all binaries: eg. "make"
3) Now start with one binary at a time and fix it:
   - start the binary in gdb: eg. "gdb ccalc_simpleone"
   - set a break point in main: eg. "b main"
   - get the process running and wait for the break point to get hit: eg. "run"
   - now single step the C source while you poke around the variables and memory so you can see
     what is happening.  Continue single stepping until you hit something that looks suspicious
     eg. a segmentation fault
   - go read the source code and hints in the comments around where the error occurred and fix the problem.
   - once you think things are fixed try running the test script: "./testcalc.sh ccalc_simpleone 1"
   - if fixed, then great, move on to the next one
   - if not, then go back and start exploring the code more and lookup information about the
     aspects of C that the code seems to relate to.  Don't forget to use all that you know with respect to drawing things out that correspond to how things are laid out in memory and using gdb to confirm things. C's power and difficulty come from its ability to work with memory in the same way that we can directly work with memory in assembly.
4) the order we suggest are:
   1) ccalc_simpleone : will have you fix some bugs in the "or" command some new things in the driver - including how we do I/O in C 
   2) ccalc_basic : gets you to fix up more of the C version simple calculator commands
   3) ccalc_upperonly : will have you fix up the uppercase logic written in C
   4) ccalc_easy, basicwithupper and simplerandom: should all work at this point 
   5) ccalc_arraysum: see how array logic works
   6) ccalc_listsum: walk a linked list in C
   7) ccalc_atoq: do something that was hard in assembly in a single library call
   8) ccalc_listsumread: use malloc and free to build a dynamic linked list based on user input
   9) ccalc_array and list: see how function pointers work in C
   10) ccalc_popcnt : explore how to use bitwise operators in C to implement something that in INTEL assembly would have only required a single instruction

See the getting started video for an example working session.

## New Calculator Commands

There are three new calculator commands:

- 'P' :  print to standard error the current values of the running result, SUM_POSITIVE and SUM_NEGATIVE as
ascii values: look at printResults in main.c. You should run into this as soon as you work on simpleone as it calls
printResults
- 'r' : read a list from standard in and process the list with sumlist and then free the list.
   - ccalc_sumlistread tests this functionality and the print functionality.
   - you will need to learn about how to create and destroy a linked list in C using malloc and free
- 'p' : takes the current result value and a second argument as inputs and returns
        the sum of the current result plus population count (the number of one bits in the second argument).
   - ccalc_popcnt 
   
## gdb and C

One of the powerful aspects of the tool chain (compiler, assembler, linker) is that they all know how to leave information for a debugger like gdb.  In particular, they leave enough information that
gdb knows what assembly code corresponds to what C source code lines.  This allows us to use gdb to work both at the "source" level while also working directly with the memory of the process created from the binary.

The provided "setup.gdb" file configures the tui mode so that we can see both the source code and assembly.  To use it, simply start gdb with the extra option "gdb -x setup.gdb <binary>".

Everything that we were doing before, inspecting registers and memory and single stepping instructions, are all still possible.  However, we can also now ask gdb to show us things that correspond the the C code.  Eg we can:
  - list the source code corresponding to a function: eg. "list csum"
  - disassemble a function. eg. "disassemble csum"
  - set break points on "c" function names and even on c source code lines.  Gdb will figure out
    the address of the underlying opcodes and set the break point on the appropriate address.
    eg.
      - "b csum" will set a break point to stop execution when the csum function starts executing
      - "b 263" will set a break point on the instructions that implement line 263 for the current c source file you are viewing.
  - print C variables, structures eg. p <variable name> or p /x <variable name> to see it in hex
  - work with C pointers.  eg. assume we have a pointer variable like "cmd" in the main function of ccalc.c we can do things like:
    1) print what address it is pointing to: "p cmd"
    2) dereference the pointer to see the values at the location in memory it points to:  "p *cmd"
    3) if it is a pointer to a structure or union we can use the C pointer syntax to see fields:
    "p cmd->first.cmd[0]
  - we can have gdb single step a source line eg. we can ask gdb to run all the assembly instructions that implement a single source line of C.  eg. "step". Notice we no longer have the i at the end
  - "step" will single step into functions but you can also use "next" which will not step into functions but rather execute until you get to the next line of the function you are in.
  - there are lots more features to explore and you will be well rewarded

## Uncommented

The source files are heavily commented so that you can better understand what the code is 
trying to do or illustrate.  However, sometimes it can be hard to see the structure, or
core meaning, with all the comments present.  For this reason, we also provide a copy of 
the code in the `uncommented` directory that has the comments stripped. 

## References

K.N. King, “C Programming: A Modern Approach”, Second Edition, W. W. Norton & Company, 2008. 
1) Skim chapters 2-9 
2) Focus on 
  - 11 Pointers
  - 12 Pointers and Arrays
  - 16 Structures and Unions
  - 17 Advanced uses of pointers in particular :
      - 17.5 Linked Lists
      - 17.7 Pointers to Functions


Start early and HAVE FUN!
