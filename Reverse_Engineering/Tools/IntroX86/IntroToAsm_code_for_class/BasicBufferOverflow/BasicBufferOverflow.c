#include <stdio.h>

int lame(unsigned int size, unsigned int value){

	unsigned int array1[4];
	unsigned int array2[6];
	array2[5] = value;
	memcpy(&array1, &array2, size * sizeof(unsigned int));

	return 1;
}

void awesome(){
	printf("awwwwwww yeaaahhhhh! All awesome, all the time!\n");
}

void main(unsigned int argc, char ** argv){
	unsigned int size, value;
	size = strtoul(argv[1], "", 10);
	value = strtoul(argv[2], "", 16);

	if(!lame(size, value)){
		awesome();
	}
	else{
		printf("I am soooo lame :(\n");
	}

	return 0xdeadbeef;
}