//Journey to the center of memcpy
#include <stdio.h>

typedef struct mystruct{
	int var1;
	char var2[4];
} mystruct_t;

int main(){
	mystruct_t a, b;
	a.var1 = 0xFF;
	memcpy(&b, &a, sizeof(mystruct_t)); 
	return 0xAce0Ba5e;
}