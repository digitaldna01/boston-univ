#include "ccalc.h"
#include <stdio.h>

// Declare a structure type (struct Node) to describe how a list node
// should look like in memory:
struct Node { 
  long long v;          // 8 byte signed value
  struct Node *next;    // followed by a pointer to another node
};

/* clist: takes in 1) the running result, 2) an address of where the
   beginning of a list (head) and 3) a pointer to a function to call
   on the running result and each element of the list.  clist returns
   the final running result.

   Another illustration of a linked list walk and use of a function
   pointer.  See ccalc.h for details on calc_simple_func_ptr
*/
long long
clist(long long cres, void *head, calc_simple_func_ptr func)
{
  struct Node *node = head;

  // loop that interates over the nodes
  for (; node != 0; node=node->next) {    
    VPRINT("  func:%p cres:%lld SUM_POSITIVE=%lld SUM_NEGATIVE=%lld "
	   ": node:%p: v:%lld next:%p\n",
	   func, cres, SUM_POSITIVE, SUM_NEGATIVE, node, node->v,
	   node->next);
    // You need to invoke the function pointed to by func and set cres
    // to the value it returns:  HINT: See how carry.c does this
    cres = func(cres, node->v);            // run input function with node value
  }
  
  VPRINT("  FINAL func:%p cres:%lld SUM_POSITIVE=%lld "
	 "SUM_NEGATIVE=%lld : node:%p\n",
	 func, cres, SUM_POSITIVE, SUM_NEGATIVE, node);
  return cres;
}

