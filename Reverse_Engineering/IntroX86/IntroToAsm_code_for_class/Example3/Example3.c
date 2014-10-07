//Example3.c - conditionals
//New instructions: je, jge, jle,
int main(){
	int a=1, b=2;
	if(a == b){
		return 1;
	}
	if(a > b){
		return 2;
	}
	if(a < b){
		return 3;
	}
	return 0xdefea7;
}