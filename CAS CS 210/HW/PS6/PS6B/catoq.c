#include "ccalc.h"
#include <stdlib.h>

/* catoq: C version of atoq.  Takes in 1) the current running result
   and 2) add a pointer to an ascii string.  It should attempt to
   decode and ascii integer from the beginning of the string
   into an 8 byte signed value and then call the csum function
   on the running result and the decoded value updating 
   the running result.

   Example of why all the libc functions for strings can be so handy
*/

long long
catoq(long long cres, char *cptr)
{
  long long y=0;

  // libc has a very handy set of functions that can convert ascii
  // strings that encode numbers into a binary value. Lookup atoll and
  // use it here to do what is a pain to write ourselves in assembly.
  // eg.  a single call to atoll will do all the work

  y = atoll(cptr);            // use atoll function from libc to convert string to integer

  // now that we have the value as a binary, use csum to do the
  // remaining work
  cres = csum(cres, y);
  return cres;
}
