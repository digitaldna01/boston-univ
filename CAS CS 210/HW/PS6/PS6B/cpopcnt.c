#include "ccalc.h"
#include "stdio.h"

/* cpopcnt: A new function for the c version of the calculator.  Takes
   in 1) the running result and 2) a signed integer value y.  The
   function should calculate the number of 1 bits in y and return the
   addition of this count and the running result
 */
long long
cpopcnt(long long result, long long y)
{
  unsigned long long v=(unsigned long long)(y);
  long long cnt=0;
  // Turns out that something that was one INTEL instruction in 
  // assembly has no C counter part :-(
  // We are going to have to write some code
  // HINT:
  //       Right shifting (">>")an unsigned variable by 1 will produce
  //       a new binary value where all the bits have shifted down to
  //       the right by one and the new upper left bit will be set to
  //       0.
  //       eg if we have: unsigned long long y=0xffffffffffffffff; 
  //          then "v=v>>1;" will set y to 0x7fffffffffffffff;
  //          if you repeatedly right shift v (63 times) you will end up
  //          with all the original bits having gone through the zeroth
  //          bit position
  //      Additionally: "masking" by bitwise anding a binary value by
  //      0x1 will yield the value only of the bit in the zeroth
  //      position.
  //         eg. "cnt = cnt + (v & 0x1);" will add one to the count if
  //             the bit in the zeroth position of v is 1 and it will
  //             and zero if the bit is zero
  //
  // Using the above, can you write a very small loop to count the
  // number of ones in v?

  // force program to crash here by trying to read address zero
  for(int i = 0; i < 64; i++){            // execute the for loop for 63 times
    cnt = cnt + (v & 0x1);                // count the 1 at the right most digit
    v = v>>1;                             // shift more digit to the right
  }

  return result + cnt;
}
