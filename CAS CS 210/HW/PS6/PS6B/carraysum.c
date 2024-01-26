#include "ccalc.h"
#include <stdio.h>

/* carraysum: takes in 1) the current running result 2) the length of
   an array of 8 byte signed integers, and 3) a pointer to the
   beginning of the array of 8 byte signed integers.  This function
   calls the csum function to each element and updates the running
   result as it goes.  The function returns the final updated
   running result value.

   Illustrates a standard C array iteration.
  */

long long
carraysum(long long cres, long long len, long long *array) {
  long long i;
  for (i=0; i<len; i++) {
    VPRINT("  len:%lld cres:%lld SUM_POSITIVE=%lld SUM_NEGATIVE=%lld"
	   " : array[%lld]=%lld\n",
	   len, cres, SUM_POSITIVE, SUM_NEGATIVE, i, array[i]);
    // call csum on the ith element of the array and update cres
    cres = csum(cres, array[i]);               // call csum to add array value to cres
  }
  VPRINT("  FINAL: len:%lld cres:%lld SUM_POSITIVE=%lld SUM_NEGATIVE=%lld"
	 " : array[%lld]=%lld\n",
	 len, cres, SUM_POSITIVE, SUM_NEGATIVE, i, array[i]);
  return cres;
}
