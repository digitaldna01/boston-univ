#include "ccalc.h"

/* csum: takes in two 8 byte signed integers x and y. Updates
   the global variable SUM_POSITIVE and SUM_NEGATIVE depending on the
   sign of y.  Returns x + y
   Ah the assembly version seems oh so long ago ;-)
*/
long long csum(long long x, long long y) {
  if ( y >= 0) SUM_POSITIVE += y;  // ccalc.h has externals declarations that make this work 
  else {
    SUM_NEGATIVE += y;            // if y is a negative number add y to SUM_NEGATIVE
  }
  return x + y;
}
