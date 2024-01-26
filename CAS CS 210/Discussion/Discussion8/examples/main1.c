#include <unistd.h>

long long XARRAY[10] = { 1, 2, 3, 4, 5, -15, 1, 1, 1, 1 };

long long sumit();

int main(int argc, char *argv[])
{
  long long sum;

  sum = sumit();
  write(1, &sum, 8);

  return 0;
}
