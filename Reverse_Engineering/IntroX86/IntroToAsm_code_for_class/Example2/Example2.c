#include <stdlib.h>
int sub(int x, int y){
	return 2*x+y;
}

int main(int argc, char ** argv){
	int a;
	a = atoi(argv[1]);
	return sub(argc,a);
}