#include <stdlib.h>
int main()
{
  char *array[2];
  array[0] = "/bin/sh";
  array[1] = NULL;
  execve(array[0], array, NULL);
  exit(0);
}
