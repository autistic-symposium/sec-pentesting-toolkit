//Goto example
#include <stdio.h>
int main(){
	goto mylabel;
	printf("skipped\n");
mylabel:
	printf("goto ftw!\n");
	return 0xf00d;
}
