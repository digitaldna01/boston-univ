#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>
#include <string.h>

void get_array(int arr[], int n){
    int i;
    srand(time(NULL));

    for(i = 0; i < n; i++){
        arr[i] = rand() % 100 +1;
    }
}

void print_array(int *arr, int n){
    int i;
    int *p;
    p = arr;

    for(i = 0; i < n; i++, p++){
        printf( "%d ", *p);
    }
    printf("\n");
}

void generic_print_array(void *base, size_t nmemb, size_t size, void (*print_elem)(const void *)){
    
    void *p = base;

    for(p = base; p < base+ nmemb*size; p+=size){
        print_elem(p);
    }
    printf("\n");
}

void print_elem(const void *elem){
    printf("%d ", *((int *)elem));
}

void float_print_elem(const void *elem){
    printf("%.2f", *(float *)elem);
}

void bubble(int arr[], int n){
    int i, j;
    int temp;

    for(i = 0; i < n-1; i++){
        for(j = 0; j < n-i-1; j++){
            if(arr[j] > arr[j+1]){
                temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
        print_array(arr, n);
    }
}

void bsort2(void *base, size_t nmemb, size_t size, int (*compare)(const void *, const void *)){
    int i, j;
    void *temp = malloc(size);
    void *ptr;

    for(i = 0; i < nmemb-1; i++){
        
        for(j = 0; j < nmemb-i-1; j++){
            ptr = base + j*size;
            if( compare(base + j * size , base + (j+1)*size) > 0){
                memcpy(temp, base + j*size, size);
                memcpy(base + j*size, base + j*size +size, size);
                memcpy(base + j*size + size, temp, size);
            }
        }
    }
    free(temp);
}

void bsort(void *base, size_t nmemb, size_t size, int (*compare)(const void *, const void *)){
    void *i_ptr, *j_ptr;
    void *temp = malloc(size);
    void *end_p = base + size * (nmemb - 2);

    for(i_ptr = base; i_ptr <= end_p; i_ptr+=size){
        for(j_ptr = base; j_ptr < end_p-(i_ptr-base); j_ptr+=size){
            if(compare(j_ptr, j_ptr+size) > 0){
                memcpy(temp, j_ptr, size);
                memcpy(j_ptr, j_ptr+size, size);
                memcpy(j_ptr+size, temp, size);
                
            }
        }

    }
    free(temp);
}

int compare(const void *elem1, const void *elem2){
    int *e1 = (int *)elem1;
    int *e2 = (int *)elem2;

    return *e1 - *e2;
}

int main(void){
    int arr[10];

    get_array(arr, 10);

    generic_print_array(arr, 10, sizeof(int), print_elem);

    bubble(arr, 10);

    generic_print_array(arr, 10, sizeof(int), print_elem);

    return 1;
}