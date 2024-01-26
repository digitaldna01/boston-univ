/******************************************************************************
* Copyright (C) 2022 by Jonathan Appavoo, Boston University
*****************************************************************************/
/* A C version of the Assembly Calculator */
/*
  This code illustrates how the C programming language allows us to
  work with memory in a more human friendly fashion than assembly
  code.  However, while we gain certain advantages it is also worth
  noting that some things that we were able to do in assembly are not
  possible.
*/

/* The C Preprocessor:

   Before our file is translated it is first processed by the C
   'pre-processor'.  The pre-processor implements what is called a
   macro language.  See
   https://gcc.gnu.org/onlinedocs/cpp/Overview.html#Overview
   Specifically certain text in the file get substituted based on
   "macros".  You can identify c-preprocessor macro definitions by the
   fact that they begin with the '#" symbol The most common macro you
   will first run into is #include file. The #include macro expands to
   the contents of the file that is specified. For example the
   following line will get substituted with the contents of the file
   ccalc.h */
#include "ccalc.h"

/* We must enclose the file name in either double quotes "" or angle
   brackets <>.  Double quotes indicate that the file's location is
   relative to the directory of the source code.  So in the above line
   we are asking the preprocessor to look for a file in the same
   directory as this file, ccalc.c, by the name of ccalc.h and
   substitute its contents here.

   On the other hand if we use angle brackets as below, the
   preprocessor will look for files in a set of default system paths
   where standard files are kept.
*/

// Declaration of the UNIX standard C functions that typically provide
// access to UNIX system calls such as write
#include <unistd.h>

// Declarations of the standard input/output libc functions and types
// (eg. printf and friends) see man stdio
#include <stdio.h>

// Declaration of various standard C functions such as libc's exit
// routine
#include <stdlib.h>

/* Header files

 It is standard practice at the start of a C file to use the #include
 directive to include the contents of what are called header files.
 By convention we use the suffix ".h" in their name.  In these files
 we provide declarations that we want to use in our code.  NOTE
 declarations are not definitions!  We will talk more about this
 later.  Go look at the file ccalc.h to see what its content looks
 like.  What you will find is that it declares the name of functions
 and specifies their return type and argument lists.

 By including these declarations in our code the compiler will know
 enough to be able to generate the assembly code to call the
 functions.  Again note the definitions (bodies) of the functions are
 not in the header file.  Rather there are separate source files that
 contain the actual definitions of the functions.

 One of the most powerful aspects of the C toolchain model is the
 standardization of how we can compose programs from existing content
 including binary content for which we do not have the source code but
 rather just have access to object files that have been given to us.
 By providing us with a header file, a programmer can give us
 everything we need to have the C compiler generate calls to their
 code while only giving use object files for the actual functions.
  
 In this way we can write C code that has calls to other functions we
 do not define.  The compiler will generate the right assembly code to
 call the symbol that is in the object file that is provided.  Because
 the header file contains the declaration of a function, the compiler
 can generate the assembly code to load the arguments into the right
 registers and then generate the appropriate call a symbol that is the
 name of the function.  For example when our code below specifies a
 call to 'csum(result, cmd->second)' the compiler will generate the
 assembly to put result and the cmd->second field into the right
 registers and also generate `call csum` after using the assembler the
 resulting opcodes will be in the ccalc.o.

 Given that we have a separate csum.c that when compiled and assemble
 will produce the opcodes for the csum function into the csum.o.  We
 will then be able to link the two together and the binary will then
 contain both and the call and return will behave as we expect.

*/


/* Have the compiler introduce two 8 byte values into the the data
   section whose labels are SUM_POSITIVE and SUM_NEGATIVE */  
long long SUM_POSITIVE=0;
long long SUM_NEGATIVE=0;

/* Unions -- multiple views of a chunk of memory

A union lets us tell the compiler that we will want to work with a
chunk of memory in more than one way.  Each member declaration in the
union provides a different view/interpretation of memory (the size is
determined by the size of the largest declaration)

For example the first 8 bytes of the calculator command structure is a
good candidate for a union.  We would like to use it as:

     1) A single raw 8 byte quantity when we want to test to see if
        they are all 0 in which case we have reached the end of the
        commands.

     2) An array of 8 single bytes that encode our ascii calculator
        command characters.
*/
union calc_cmd_word {
  long long raw;             
  char c[sizeof(long long)];
};

/* The following tells the compiler that some other object file will
   be providing symbols that we will use like C variables that are of
   type struct calc_cmd */
extern struct calc_cmd CALC_DATA_BEGIN;
extern struct calc_cmd  CALC_DATA_END;

/* Now that we have introduced calc_cmd_word union we can now use
   "union calc_cmd_word" when want to treat an 8 byte chunk of memory
   in these two ways.  Below we will see examples.  */

/* Structures:  heterogeneous complicated views of memory
  
   One of the most powerful aspects of C is our ability to tell the
   compiler about which complicated view of memory that we want to use
   as a unit.  In assembly we had to keep track of this all on our
   own.  It was our job to hold things in our head and write assembly
   code that use memory according to the way we wanted.
 
   C solves this problem by letting us describe memory in terms of
   structures.  Each structure definition describes to the compiler an
   aggregation of member fields that together describe a view of
   memory.  By giving each structure definition a type name we can
   then declare memory to be of a particular structure type.  Then the
   compiler will generate code to access that memory by the individual
   fields of the structure automatically.

   The rules of the C language ensures that the size and location of
   the individual fields can be exactly determined, and meet all the
   constraints that our particular computer might have.  The 'sizeof()'
   operator evaluates to the number of bytes that a type is.  It can
   be used on all the standard built in types such as: char, short,
   int, long, long long.  But importantly it can also be used with
   programmer defined unions and structure types.  This will become
   very important as we will see later.
*/

/* The Calculator command structures that describe the unique ways
   that the calculator commands get laid out in memory */

// The basic calculator command
struct calc_cmd {  
  union calc_cmd_word first;
  long long second;
};

// The Upper and ATOQ commands uniquely treat the second argument as a
// string pointer to more clearly document this we introduce another
// struct type
struct calc_string_cmd {
  union calc_cmd_word first;
  char *str;               
};

// The array sum and array commands uniquely uses an extra field
//   First 8 is our standard command word
//   Second is the length of the array
//   Third is a pointer to the start of the array of numbers
struct calc_array_cmd {
  union calc_cmd_word first;
  long long len;
  long long *array;
};

// The list sum and list commands use the second value as a pointer to
// the head of a list.  To better document this view we introduce a
// structure.  All pointers on a 64 bit system are also 64 bits. Here
// we use a void * to indicate that the second field is a pointer but
// that we don't know what type it points to.  void is the "notype"
// type.
struct calc_list_cmd {
  union calc_cmd_word first;
  void  *head;
};


/* Declarations for functions that are not defined before we use them
   must be provided so that the compiler knows how to generate calls
   to them.  If the definition comes first, it also serves as a
   declaration.  Here we have chosen to organize the file with main
   function first.  So functions it uses, that appear later in the
   file, need to be declared.  Such declarations are often called
   forward declarations. */

// Discussion of these are provided with their definitions after the
// main function
calc_simple_func_ptr cmd2func(char c);   
void writeResults(long long result);
void printResults(long long result);

/* main: the first application programmer function to be called
   
  The C library includes what is called the C runtime.  The C runtime
  code provides the _start assembly code for our binary.  It contains
  lots of startup code that initializes various C library facilities
  for us.  This way once the code we have written is started the C
  library will already be initialized for our use.  When the
  initialization is done the C runtime code has a call to a symbol
  called "main"

  As such by providing a main function we can take over execution from
  the C startup code.  The C runtime passes two standard parameters to
  the main routine (on Unix there is a third):

    1) An integer count of the number of command line arguments 
    2) An array of pointers to the strings associated with the command line arguments
    3) On Unix a third pointer to a copy of the environment variables that the parent process
       had when they created the child to run the binary is also passed in

  See man execve for the details on Linux.  While these arguments are
  passed in we don't have to use them.  That is up to us.
 */

// Our main functions is the equivalent of the driver we wrote for the
// assembly version of the calculator.  It will be called from the
// libc provided _start routine
int
main(int argc, char **argv, char *envp)
{
  // variables declared in a function are local variables if the
  // compiler needs memory for them it will create space on the stack.
  // On the other hand if the compiler can keep them in registers it
  // will and thus avoid using the stack if it can.
  long long i=0;
  long long result=0;
  
  // A variable that we will use to point to the current calculator
  // command we are working on.  In our assembly version we explicitly
  // used rbx to hold the address of the current command.  In C we are
  // letting the compiler decide what registers or memory to use for
  // this
  struct calc_cmd *cmd;   
  
  // We use a for loop to iterate though the command array
  for (cmd = &CALC_DATA_BEGIN;  // initialize the cmd variable with the address
                                // of the first command
       cmd->first.raw != 0;     // loop until the first 8 bytes of the current
                                // command is not zero
       i++) {                   // increment the i variable to keep track of how
                                // many commands we have processed
    VPRINT("result: 0x%llx (%lld) SUM_POSITIVE=%lld SUM_NEGATIVE=%lld\n"
	   "cmds[%lld]: %p cmd: %c arg: 0x%llx (%lld)\n", 
	   result, result, SUM_POSITIVE, SUM_NEGATIVE,
	   i,
           cmd, cmd->first.c[0], cmd->second, cmd->second);
    // Use a case statement to decode the first byte of the command word
    switch(cmd->first.c[0]) {
    case '&':
      
      // Unlike our assembly version, C does not let us explicitly
      // control what registers are used for and we can only return a
      // single value.  So our functions have been rewritten to taken
      // in the current running value (that we kept in RAX in our
      // assembly version) as their first argument.  We have also
      // rewritten them to explicitly take the value at the memory of
      // the second 8 bytes of the current command rather than a
      // pointer.  In our assembly version we used RBX to pass in a
      // pointer to the value being operated on and the functions
      // implicitly updated RAX and RBX.  Now the functions return the
      // new running value which we assign to the result variable.
      result = cand(result, cmd->second);
      
      // similarly since the functions no longer directly update where
      // the next command is we now use "pointer" arithmetic here
      // after the function has executed to advance to the next
      // command.  Since the compiler knows that the type of the thing
      // we are pointing to, it assumes that when we add to the
      // pointer it should add or subtract in sizes of the type rather
      // than just single bytes!
      cmd++;
      break;
    case '|':
      result = cor(result, cmd->second);
      cmd++;
      break; 
    case 'S':
      result = csum(result, cmd->second);
      cmd++;
      break;
    case 'p':
      result = cpopcnt(result, cmd->second);
      cmd++;
      break;
    case 'U':
      {
	struct calc_string_cmd *scmd = (void *)cmd;
	VPRINT(":%s ->\n", scmd->str);
	result = cupper(result, scmd->str);
	VPRINT(":%s\n", scmd->str);
	scmd++;
	cmd = (void *)scmd;
      }
      break;
    case 'I':
      {
	struct calc_string_cmd *scmd = (void *)cmd;
	VPRINT("    :%s\n", scmd->str);
	result = catoq(result, scmd->str);
	scmd++;
	cmd = (void *)scmd;
      }
      break;      
    case 'a':
      {
	struct calc_array_cmd *acmd = (void *)cmd;
	result = carraysum(result, acmd->len, acmd->array);
	acmd++; 
	cmd = (void *)acmd;
      }
      break;
    case 'l':
      {
	struct calc_list_cmd *lcmd = (void *)cmd;
	result = clistsum(result, lcmd->head);
	lcmd++;
	cmd = (void *)lcmd;
      }
      break;
    case 'r':
      {
	void *head = clistsum_read();
	result = clistsum(result, head);
	clistsum_free(head);
	cmd++;
      }
      break;
    case 'A':
      {
	struct calc_array_cmd *acmd = (void *)cmd;
	result = carray(result, acmd->len, acmd->array, cmd2func(cmd->first.c[1]));
	acmd++;
	cmd = (void *)acmd;
      }
      break;
    case 'L':
      {
	struct calc_list_cmd *lcmd = (void *)cmd;
	result = clist(result, lcmd->head, cmd2func(cmd->first.c[1]));
	lcmd++;
	cmd = (void *)lcmd;
      }
      break;
    case 'P':
	printResults(result);
	cmd++;
      break;
    default:
      fprintf(stderr, "ERROR: unknown command: %c %llx\n", cmd->first.c[0], cmd->second);
      return(-1);
    }
  }
  VPRINT("FINAL: result: 0x%llx (%lld) SUM_POSITIVE=%lld SUM_NEGATIVE=%lld\n"
	 "cmds[%lld]: %p cmd: %c arg: 0x%llx (%lld)\n", 
	 result, result, SUM_POSITIVE, SUM_NEGATIVE,
	 i,
	 cmd, cmd->first.c[0], cmd->second, cmd->second);
  writeResults(result);
  printResults(result);
  return 0;
}

// Another powerful aspect of C is the ability to work with text
// addresses aka pointers to code/functions.  Here we use this ability
// to write a function that returns a pointer to the correct simple
// calculator command function that corresponds to the appropriate
// calculator command character.  See ccalc.h for how we define the
// type calc_simple_func_ptr
calc_simple_func_ptr
cmd2func(char c) {
  calc_simple_func_ptr func;
  switch (c) {
  case '&':
    func = &cand;
    break;
  case '|':
    func = &cor;
    break;
  case 'S':
    func = &csum;
    break;
  case 'U':
    func = (calc_simple_func_ptr)&cupper;
    break;
  default:
    fprintf(stderr, "%s: ERROR: bad cmd character %c\n", __func__, c);
    exit(-1);
  };
  return func;
}

void
printResults(long long result)
{
  // print to standard error the current values as ascii values
  // eg. "result SUM_POSITIVE SUM_NEGATIVE\n" where result is printed
  // as a 0x prefixed hex value and SUM_POSITIVE and SUM_NEGATIVE are
  // decimal numbers
  fprintf(stderr, "0x%llx ", result);
  // use fprintf to print SUM_POSITIVE and SUM_NEGATIVE
  // note - space separate the values and put a new line at the end.
  // HINT: the format string for a long long decimal is "%lld" and a newline is "\n"
  // force crash -- replace with your code here
  fprintf(stderr, "%lld ", SUM_POSITIVE);                                    // add print function of SUM_POSITIVE

  fprintf(stderr, "%lld\n", SUM_NEGATIVE);                                   // add print function of SUM_NEGATIVE and newline
}

void
writeResults(long long result) {
  if (write(1, &result, sizeof(result)) != sizeof(result)) {                   // write result memory value to standard output
    fprintf(stderr, "ERROR: write results failed\n");
  }
  if (write(1, &SUM_POSITIVE, sizeof(SUM_POSITIVE)) != sizeof(SUM_POSITIVE)) {  // write SUM_POSITIVE memory value to standard output
    fprintf(stderr, "ERROR: write SUM_POSITIVE failed\n");
  }
  if(write(1, &SUM_NEGATIVE, sizeof(SUM_NEGATIVE)) != sizeof(SUM_NEGATIVE)) {   // write SUM_NEGATIVE memory value to standard output
    fprintf(stderr, "ERROR: write SUM_NEGATIVE failed\n");
  }
  if(write(1, &CALC_DATA_BEGIN, ((void*)&CALC_DATA_END) - ((void*)&CALC_DATA_BEGIN)) != ((void*)&CALC_DATA_END) - ((void*)&CALC_DATA_BEGIN)) {      // write CALC_DATA memory value to standard output
    fprintf(stderr, "ERROR: write CALC_DATA failed\n");
  }
  // add the rest of the writes of the data to standard out
  // force crash -- replace with your code here
  
}

