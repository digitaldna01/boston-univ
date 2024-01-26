/* cupper: takes in 1) running result and 2) a pointer to an ascii string.
   The function should upper case any lower case characters in the string
   and return the addition of the string length to the running result.

   Well as you guessed, this is the C version of assembly upper.  Learn how to 
   work with a array of bytes as ascii values in C.
 */
long long
cupper(long long cres, char *cptr)
{
  char c;
  int i=0;

  // Pointers and arrays are closely related in C syntax.
  //
  // This for loop iterates through the values pointed to by cptr as
  // an array.  When we use 'cptr[i]' after a pointer the compiler
  // will generate the assembly code that calculates an address by
  // taking the address of cptr as the base and add to it i * the
  // sizeof the type of the pointer.
  //
  // In our case cptr is a char pointer which is one byte so the loop
  // will iterate over the values pointed to by cptr one "char" at a
  // time.  Note the loop terminates when it finds a zero value.
  // Since by convention we terminate ascii strings with 0 we will
  // stop when we find it and thus when we are at the end of the string
for (i=0; cptr[i] != 0; i++) {
    c = cptr[i];
    if ((c >= 'a') && (c <= 'z')) {
      // we found a value that within the range of lower case ascii
      // we need to overwrite the value at cptr[i] with the upper case version
      // HINT: what does "c - ('a' - 'A')" do?
      cptr[i] = c - ('a' - 'A');                           // for each character of ascii string, subtract 32 to make it upper character
    }
  }
  return cres + i;
}
