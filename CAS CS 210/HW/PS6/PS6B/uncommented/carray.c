#include "ccalc.h"
#include <stdio.h>
long long
carray(long long cres, long long len, long long *array,
       calc_simple_func_ptr func) {
  long long i;
  for (i=0; i<len; i++) {
    VPRINT("  func:%p len:%lld cres:%lld SUM_POSITIVE=%lld SUM_NEGATIVE=%lld"
	   " : array[%lld]=%lld\n",
	   func, len, cres, SUM_POSITIVE, SUM_NEGATIVE, i, array[i]);    
    
    cres = func(cres, array[i]);
  }
  VPRINT("  FINAL: func:%p len:%lld cres:%lld SUM_POSITIVE=%lld SUM_NEGATIVE=%lld"
	 " : array[%lld]=%lld\n",
	 func, len, cres, SUM_POSITIVE, SUM_NEGATIVE, i, array[i]);
  return cres;
}
