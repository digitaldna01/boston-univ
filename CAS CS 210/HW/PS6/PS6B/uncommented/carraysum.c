#include "ccalc.h"
#include <stdio.h>
long long
carraysum(long long cres, long long len, long long *array) {
  long long i;
  for (i=0; i<len; i++) {
    VPRINT("  len:%lld cres:%lld SUM_POSITIVE=%lld SUM_NEGATIVE=%lld"
	   " : array[%lld]=%lld\n",
	   len, cres, SUM_POSITIVE, SUM_NEGATIVE, i, array[i]);
    *((int *)0) = 1;
  }
  VPRINT("  FINAL: len:%lld cres:%lld SUM_POSITIVE=%lld SUM_NEGATIVE=%lld"
	 " : array[%lld]=%lld\n",
	 len, cres, SUM_POSITIVE, SUM_NEGATIVE, i, array[i]);
  return cres;
}
