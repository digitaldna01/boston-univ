[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/ylgmMxXC)
# Writing Some Assembly Fragments

Before we start writing functions in assembly language, we will start writing some simple assembly "fragments".  

## Important General Information

There are two main components to each fragment to be written: 1) the fragment itself and 2) the fragment's test code. For each fragment, both of these components have their own assembly source code files. For this assignment, the test code for each fragment is provided in the sections below along with the filenames that should be used for all of the source code files. 

Each fragment should contain a symbolic label identifying the beginning of its instructions, and the last instruction for each fragment should trap back to the debugger. See the lecture notes here for more info on trapping:

https://CS-210-Fall-2023.github.io/UndertheCovers/lecturenotes/assembly/L08.html#interrupt-3-int3-trap-to-debugger

In addition, you will need to construct a single `Makefile` so that all of the assembly source code files can first be assembled into object files and then linked together to produce functioning binary executables.

The provided test code will check if your fragments are correct, but they will assume your `Makefile` has certain targets that you will need to write. Study the test script to determine what these targets are. HINT: Examine each line in the test script that invokes make.

Given we don't know how to write complete functions yet, our fragments finish by trapping back to the debugger. With this in mind, our code is "run" and tested using the `gdb` debugger. For example, each provided test script starts `gdb` with your executable file and then runs `gdb` commands to exercise your fragment. You should use `gdb` by hand to explore the test code and your fragments.

**Lastly, don't blindly use the test scripts! They are there for you to explore and learn from.**

## Notes

What you need to complete this assignment can be found in the examples in the lecture slides, discussion handouts, and the textbook. The additionally provided reference sheet summarizes all the assembly and gdb syntax that you need.


### Examples

The examples in the lecture notes, discussions, and textbook include examples of the commands required to assemble your code into object files as well as how to link the object files to produce an executable.  In particular, the `sumit.s and usesum.s` example, from the lecture notes, illustrates the complete process of creating a binary from two source files; 1) a file containing a assembly fragment (`sumit.s` and 2) a file containing test code that uses the fragment `usesum.s`.  This example can be found here:

https://CS-210-Fall-2023.github.io/UndertheCovers/lecturenotes/assembly/L10.html#sumit-s-and-usesumit-s


### Reference Information

The reference sheet:

https://CS-210-Fall-2023.github.io/UndertheCovers/textbook/images/INTELAssemblyAndGDBReferenceSheet.pdf

Has a summary of all the INTEL instructions, addressing mode syntax, and gdb commands you need.

If needed, more information can be found by looking up INTEL instructions and how they work in the INTEL manuals that are available online here:

https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html

Chapters 3, 4, and 5 of Volume 2A is the INTEL instruction set reference documentation that provides a detailed description of all the INTEL instructions. 
The table of contents lets you jump directly to the pages for a particular instruction. 

With respect to the address mode syntax for the operands, beyond what is on the reference sheet, you can find a summary and guidance in the lecture notes here: 

https://CS-210-Fall-2023.github.io/UndertheCovers/lecturenotes/assembly/L09.html#addressing-modes-for-sources-and-destinations


## The Fragments To Write

There are three fragments `AND_FRAG`, `OR_FRAG` and `SUB_FRAG`.  Each are described below. Variables x and y in the descriptions are only used to aid in understanding the problem. Use the corresponding registers instead.

**Do not use the following descriptions as a comment in your final submission.**

### File: `and.s` Fragment symbol: `AND_FRAG`

#### Description
```
	# AND_FRAG Fragement
	# INPUTS: rax -> x
	#         rbx -> &y address of where in memory y is
	# OUTPUTS: x = x bitwise and y : update rax with bit wise and of the 
	#                                8 byte quantity at the location of &y
	#          rbx should be updated to equal &y + 8
```


#### Test code: `andtest.s`
```
        .intel_syntax noprefix
        .section .text
        .global _start
_start:
test1:
        mov rbx, OFFSET data_start
        mov rax, 0xfadefacebeaddeed
        jmp AND_FRAG
test2:
        jmp AND_FRAG
test3:
        jmp AND_FRAG

        .section .data
data_start:
        .quad -1                  # mask all bits
        .quad 0x5555555555555555  # every other bit
        .quad 0xBADF00C3D4BADF00
data_end:
        .quad 0x0
```

Study the test code to figure out exactly what is expected of your AND_FRAG
routine.  You are encouraged to write your own more complex test program to ensure that you understand what is going on.  

The included `andtest.sh` will be used to test your solution. It
assumes that you have created a Makefile that does what is needed. You
will need to study the `andtest.sh` script to figure out what your Makefile
will need to do and how your code will be tested with `gdb`.  Do not
blindly try and make your solution work with the test script.  Rather,
read the scripts and figure out how to write things and test them
yourselves by hand.


### File: `or.s` Fragment Symbol: `OR_FRAG`

Similar to above, but with the 'or' operation.  

#### Description

```
        # INPUTS: rax -> x
        #         rbx -> &y address of where in memory y is
        # OUTPUTS: x = x bitwise or y : update rax with bitwise or of the 
        #                               8 byte quantity at the location of &y
        #          rbx should be updated to equal &y + 8
```

#### Test code: `ortest.s`
```
        .intel_syntax noprefix
        .section .text
        .global _start
_start:
test1:
        mov rbx, OFFSET data_start
        xor rax, rax
        jmp OR_FRAG
test2:
        jmp OR_FRAG
test3:
        jmp OR_FRAG

        .section .data
data_start:
        .quad 0x8000000000000001 # outside bits
        .quad 0x000000FFFF000000 # middle 16 bits
        .quad 0x6F3A823BE019DD45
data_end:
        .quad 0x0
```

### File: `sub.s`  Fragement Symbol: `SUB_FRAG`

Now that we have gotten the hang of the mechanics, let's write a fragment that is a little more involved and operates on memory as well as registers.

#### Description
```
        # INPUTS: rax -> x
        #         rbx -> &y address of where in memory y is
        # OUTPUTS: x = x - y : update rax by subtracting y
        #                      from rax at the location of &y
        #          if y is positive then add y into an 8 byte value
        #          stored at a location marked by a symbol
        #          named SUB_POSTIVE
        #          else subtract y from an 8 byte value stored at a 
        #          location marked by a symbol named SUB_NEGATIVE
        #          final rbx should be updated to equal &y + 8
        #
        # This file must provide the symbols SUB_POSTIVE 
        # and SUB_NEGATIVE and associated memory
```        


#### Test code: `subtest.s`

```
        .intel_syntax noprefix
        .section .text
        .global _start
_start:
test1:
        xor rax, rax
        mov QWORD PTR [SUB_POSITIVE], rax
        mov QWORD PTR [SUB_NEGATIVE], rax

        mov rbx, OFFSET data_start

        jmp SUB_FRAG
test2:
        jmp SUB_FRAG
test3:
        jmp SUB_FRAG
test4:
        jmp SUB_FRAG

        .section .data
data_start:
        .quad 1
        .quad -4560
        .quad 52553324
        .quad -2
data_end:
        .quad 0x0
```
