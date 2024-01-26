/* preprocessor directive to include the contents of the unistd.h "header file" */
#include <unistd.h>
#include <stdio.h>

/* forward declaration of function called in main */
long long sumit();
/* this line introduces an array wirh 10 elements, which are or the type long long, meaning 8 byte signed integers. In the same line, we assign the array elements to be the values inbetween the curly braces */
long long XARRAY[10] = {1, 2, 3, 4, 5, -15, 1, 1, 1, 1};

/* argc is an integer that holds the number of arguments passed to the program, and argv is an array of pointers to those arguments */
int main(int argc, char *argv[]){
  /* Declares the variable sum, which is type long long */
  long long sum;

  /* assign the value returned by the sumit function to the sum variable*/
  sum = sumit();

  /* call the write system call, passing 1 as the file descriptor to write to (standard out), the address of the data we want to wrtie (&sum), and the length to write in bytes (8) */
  /*write(1, &sum, 8);*/
  printf("%lld", sum);

  return 0;
}
