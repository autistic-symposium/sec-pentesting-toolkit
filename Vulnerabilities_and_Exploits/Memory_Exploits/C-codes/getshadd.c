// usage: ./getshadd ENVVAR BINARY
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,char *argv[]){
        char *ptr;
        ptr=getenv(argv[1]);
        ptr+=(strlen(argv[0])-strlen(argv[2]))*2;
        printf("%s will be at %p\n",argv[1],ptr);
        return 0;
}
