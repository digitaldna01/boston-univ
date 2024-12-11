#include <stdio.h>
#include <stdlib.h>

char global1 = 'g';
char global2;
char global3;
char global4 = 'G';

void func(void);


void swap(int *a, int *b){
    int temp;
    temp = *a;
    *a = *b;
    *b = temp;
}

int main(void){
    func();

    return 0;

}

void func(void){
    
    char *ptr = (char *)malloc(10*sizeof(char)); 

    //free(ptr);
}