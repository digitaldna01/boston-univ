# Problem Set 2 Bonus

This is a bonus assignment with questions pertaining to the material from PS2B. As stated in the syllabus, should you choose to complete a given bonus assignment, it can be submitted anytime before the last day of classes (December 12). 

For this bonus, you must answer the questions in the space provided on the PDF, and submit **only the assignment PDF** to the ps2bonus Gradescope site.

**Note**: To prevent any errors in the grading process, please submit a copy of the assignment PDF, with your answers filled in the blanks provided (i.e., do not submit a document with your solutions only, remove pages from the PDF, etc.) 

Have fun!

## Instructions

First, clone this repository.

Then, you may either:
- copy and paste the content of your `empty.s` and `Makefile` into two new files, respectively, from your PS2B assignment or,
- follow `Step 1: empty.s / make and Makefiles` and `Question 3: q3.gdb - Modify Your empty.s` from the PS2B instructions to recreate these two files
  - note: make the appropriate modifications to your `empty.s` and `Makefile` as asked in `Question 3: q3.gdb - Modify Your empty.s`

Please make any necessary adjustments to these two files.

At this point, you should have the following in your cloned PS2Bonus repository:
- README.md
- `q4test.sh`
- `empty.s`
- `Makefile`

**Do not forget to add each new file that you make to the repo.**

Next, you will need to create two new `gdb` commands. Please read and follow the instructions below before answering the questions in the PDF.

## Creating `q4.gdb`

Similar to `Question 2: q2.gdb` from the PS2B assignment, you will need to execute an operation. In particular, you will have your computer count the number of bits that are set to 1 in the value of the `rax` register and place the result in `rbx`.

In this task, you will no longer use `gdb` functionality to set the values of registers. Instead, you will "program" the computer to perform this operation. You will do that by writing an assembly instruction to the memory of your computer and then have your computer execute that instruction.

 To do this, you will need to write the bytes that correspond to the IA64 opcode for the `popcnt` instruction:
 ``` gas
   popcnt rbx, rax     
 ```

 The opcode for this instruction is:
 ```
         0xf3, 0x48, 0x0f, 0xb8, 0xd8
 ```

You will need to have the CPU execute this instruction and then examine the register values to see if things look right. You are encouraged to play around with this by hand. When you are convinced you know how things work, write your `q4.gdb` file to automate things with a `q4` command.

There is a testing script, `q4test.sh`, that you should use to test your solution.

We highly suggest you read through and apply the instructions from `Question 2: q2.gdb` in PS2B for `popcnt`.

## Creating `q5.gdb`

Similar to `Question 3: q3.gdb` from the PS2B assignment, you will write a `q5` gdb command that will output the following in `gdb`:
```
 (gdb) x /12xb _start
 0x400078 <_start>:      0xf3    0x48    0x0f    0xb8    0xd8    0x48    0x89    0x1d
 0x400080 <_start+8>:    0x00    0x00    0x00    0x00
 (gdb)
 ```

You may refer to the instructions from PS2B to guide you.


## PDF Assignment

At this point, you should have the following in your cloned PS2Bonus repository:
- README.md
- `q4test.sh`
- `empty.s`
- `Makefile`
- `q4.gdb`
- `q5.gdb`

Now, you are ready to answer the questions in the PDF.
