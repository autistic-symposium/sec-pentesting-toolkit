#include <stdio.h>

void ExecuteSuperFunGame(){
	printf("We both find toying with humans fun, right?\n");
}

int main(int argc, char ** argv){

	int a = 123, b = 5, c = 0x31337, d = 0;
	int i = atoi(argv[0]);

	i = i * a ^ 4/b  >> d + 19;

	if(i == i / c * d ^ 0xb0b){
		ExecuteSuperFunGame();		
	}
	else{
		printf("You must enter a valid serial number as the first command line parameter.\n");
		printf("The entered serial number is not valid\n");
	}
}