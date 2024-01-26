/******************************************************************************
* Copyright (C) 2022 by Jonathan Appavoo, Boston University
*****************************************************************************/

/* HEADER Files: This is an example of a header file.  We use it to
  declare all the things that a c file might need to work with in the
  rest of the calculator code.  In general we avoid putting any definitions in
  header files.  Rather we just provide the declaration of types and
  functions that other c files provide the definitions for.  See
  comment in ccalc.c
 */

// The next two lines along with the #endif at the bottom of the file
// are c preprocessor macros. To avoid multiple inclusions of this
// file from causing a problem we add this "guard logic".  If the
// macro __CCALC_H__ is not define then the contents up till the
// #endif will be present.  Other wise it will be like this file is
// empty when it is included.  In general you will want to add a guard
// to any header file you ever create.
#ifndef __CCALC_H__       
#define __CCALC_H__

// declare the externals for SUM_POSITIVE and SUM_NEGATIVE the use of
// extern ensure that the compiler does not treat these like
// definitions aka it will not try and create data symbols for them. It
// just lets the compiler know that some other file will provide the
// symbols and that they should be long long in type
extern long long SUM_POSITIVE;
extern long long SUM_NEGATIVE;

/* Function pointers

   This is fancy!  One of the powers of C is the ability to declare
   types for pointers to functions -- addresses to the start of the
   opcodes of a function that has specific arguments and return types.
   Here we combine a function pointer type with a typedef.  Typedefs
   allow us to introduce our own custom name for a type.  Eg
 
    typedef int * myint_ptr
    myint_ptr i_ptr = NULL;   // same as : int * i_ptr = NULL;

    A function pointer is of the form 

     <return type> (ptr_variable_name*)(<arg1 type>,<arg2 type>,...)

    Eg to define a pointer variable 'func_ptr' that should be treated
    like a variable that holds an address to a function that returns
    an int and takes three ints as arguments we would write:

    int (*func_ptr)(int, int, int) = NULL;

    However it is often cleaner to first declare a typedef for a
    function pointer type you want and then use it to declare and
    define pointers of that type Eg.

    // first introduce a typedef
    typedef int (*my_function_ptr)(int, int, int); 
    // now you can use it to declare and define variables.   
    my_function_ptr func_ptr;                      
                                                  
*/

// introduce a type for pointers to the simple calculator functions
// that return a long long and take two long longs as arguments
typedef long long (*calc_simple_func_ptr)(long long, long long);

// Declare the functions that the various files that make up the
// calculator define.  This allows any file that includes this header
// to then be able to correctly generate assembly calls to the
// functions.
long long cand(long long x, long long y);
long long cor(long long x, long long y);
long long csum(long long x, long long y);
long long cpopcnt(long long x, long long y);
long long cupper(long long x, char *cptr);				     
long long catoq(long long x, char *cptr);
long long carraysum(long long x, long long len, long long *array);
long long clistsum(long long x, void *head);

// The next two functions take a pointer to one of the simple
// calculator functions. This way they can invoke the right function on
// each element of an array or list
long long carray(long long x, long long len, long long *array, calc_simple_func_ptr func);
long long clist(long long x, void *head, calc_simple_func_ptr func);

void *clistsum_read(void);
void clistsum_free(void *head);

/*
  A nice use of preprocessor macros is what is called conditional
  compilation here if the preprocessor macro VERBOSE is defined then
  place where VPRINT appears in the source will be substituted with a
  call to fprintf, however if it is not defined then the calls will
  automatically be deleted ;-) Once you have this you can turn on or
  off verbose printing by defining the macro VERBOSE.  This means you
  can now liberally added VPRINTS to your code such as at the
  beginning of your csum function
  
    VPRINT("csum called\n");

  When compiled correctly this will introduce a printf to standard
  error however you can also set the compilation to delete
  all such prints by again correctly compiling the code

  This can be done in one of two ways
   1) In the file you want to see verbose printing you would add
      #define VERBOSE

   2) or by using the -D option to gcc.  

      Eg. gcc -g -DVERBOSE csum.c -c -o csum.o

      In this case the compiler will ensure that the VERBOSE macro is
      defined prior to the preprocessor running.  You can have as many
      -D as you like.

      See the Makefile for an example
*/
#ifdef VERBOSE
#define VPRINT(fmt, ...) fprintf(stderr, "%s: " fmt, __func__,__VA_ARGS__)
#else
#define VPRINT(...)
#endif

#endif  // __CCALC_H__
