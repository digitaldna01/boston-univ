#include "ccalc.h"
#include <stdio.h>

/* carray: An example of how to use function pointers.  This function
   takes in 1) the current running result value cres, 2) the length of
   an array of 8 byte signed values, 3) a pointer to the beginning of
   the array of 8 byte signed values and 4) a pointer to a function to
   be called on the running result and each of the array elements.
   Each function is expected to return an updated running result
   value.  The function returns the final updated version of the
   running result after the array iteration.
   
   See the ccalc.h file for details on the calc_simple_func_ptr 
   type. */

long long
carray(long long cres, long long len, long long *array,
       calc_simple_func_ptr func) {
  long long i;

  // iterate over the array 
  for (i=0; i<len; i++) {
    VPRINT("  func:%p len:%lld cres:%lld SUM_POSITIVE=%lld SUM_NEGATIVE=%lld"
	   " : array[%lld]=%lld\n",
	   func, len, cres, SUM_POSITIVE, SUM_NEGATIVE, i, array[i]);    
    // Wonder why this is crashing ?
    // maybe you need to figure out what the address of func holds and why it looks
    // bogus ;-).  HINT:  Look at the code that is call this and work your way
    // backwards.
    // Invoke the function pointer: note looks just like a normal function call
    // but the name of the function really is function pointer variable.
    cres = func(cres, array[i]);
  }
  VPRINT("  FINAL: func:%p len:%lld cres:%lld SUM_POSITIVE=%lld SUM_NEGATIVE=%lld"
	 " : array[%lld]=%lld\n",
	 func, len, cres, SUM_POSITIVE, SUM_NEGATIVE, i, array[i]);
  return cres;
}
