#include "ccalc.h"
#include <stdio.h>

struct Node { 
  long long v;          // 8 byte signed value
  struct Node *next;    // followed by a pointer to another node
};

long long
clist(long long cres, void *head, calc_simple_func_ptr func)
{
  struct Node *node = head;

  for (; node != 0; node=node->next) {    
    VPRINT("  func:%p cres:%lld SUM_POSITIVE=%lld SUM_NEGATIVE=%lld "
	   ": node:%p: v:%lld next:%p\n",
	   func, cres, SUM_POSITIVE, SUM_NEGATIVE, node, node->v,
	   node->next);
        *((int *)0) = 1;
  }
  
  VPRINT("  FINAL func:%p cres:%lld SUM_POSITIVE=%lld "
	 "SUM_NEGATIVE=%lld : node:%p\n",
	 func, cres, SUM_POSITIVE, SUM_NEGATIVE, node);
  return cres;
}

