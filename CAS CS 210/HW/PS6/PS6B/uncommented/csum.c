#include "ccalc.h"
long long csum(long long x, long long y) {
  if ( y >= 0) SUM_POSITIVE += y;   
  else {
    *((int *)0) = 1;
  }
  return x + y;
}
