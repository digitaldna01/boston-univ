#include <stdio.h>
#include <stdlib.h> // malloc, realloc

#include "adt_heap.h"

/* Reestablishes heap by moving data in child up to correct location heap array
*/
static void _reheapUp( HEAP *heap, int index){
    if(index != 0){
        int parent = (index - 1) / 2;
        if(heap->compare(heap->heapArr[index], heap->heapArr[parent]) > 0){
            void *temp = heap->heapArr[index];
            heap->heapArr[index] = heap->heapArr[parent];
            heap->heapArr[parent] = temp;
            _reheapUp(heap, parent);
        }
    }
}


/* Reestablishes heap by moving data in root down to its correct location in the heap
*/
static void _reheapDown( HEAP *heap, int index){
    int leftindex = (index * 2) + 1;
    int rightindex = (index * 2) + 2;
    if(leftindex <= heap->last){
        int largest = leftindex;
        if(rightindex <= heap->last && (heap->compare(heap->heapArr[rightindex], heap->heapArr[largest]) > 0)){
            largest = rightindex;
        }//end if
        if(heap->compare(heap->heapArr[largest], heap->heapArr[index]) > 0 ){
            void *temp = heap->heapArr[largest];
            heap->heapArr[largest] = heap->heapArr[index];
            heap->heapArr[index] = temp;
            _reheapDown(heap, largest);
        }//end if
    }//end if
}

/* Allocates memory for heap and returns address of heap head structure
if memory overflow, NULL returned
*/
HEAP *heap_Create( int capacity, int (*compare) (void *arg1, void *arg2)){
    HEAP *newHeap = (HEAP *)malloc(sizeof(HEAP));
    if(!newHeap){
        return NULL;
    }

    newHeap->last = -1;
    newHeap->capacity = capacity;
    newHeap->heapArr = malloc(sizeof(void*) * capacity);
    newHeap->compare = compare;

    return newHeap;
}

/* Free memory for heap
*/
void heap_Destroy( HEAP *heap){
    for(int i = heap->last; i > -1; i--){
        free(heap->heapArr[i]);
    }
    free(heap->heapArr);
    heap->capacity = 0;
    heap->last = 0;
    heap->compare = NULL;
    free(heap);
}

/* Inserts data into heap
return 1 if successful; 0 if heap full
*/
//삽입 용량이 다 찼을 시 배열을 capacity를 늘려준다
int heap_Insert( HEAP *heap, void *dataPtr){
    if(heap->last == heap->capacity -1){
        heap->capacity = heap->capacity * 2;
        void **temp = realloc(heap->heapArr, sizeof(void*) * (heap->capacity));
        if(!temp){
            return 0;
        }
        heap->heapArr = temp;
    }
    heap->last = heap->last + 1;
    heap->heapArr[heap->last] = dataPtr;
    _reheapUp(heap, heap->last);
    return 1;
}

/* Deletes root of heap and passes data back to caller
return 1 if successful; 0 if heap empty
*/
int heap_Delete( HEAP *heap, void **dataOutPtr){
    if(heap->last == -1){
        return 0;
    }//end if
    *dataOutPtr = heap->heapArr[0];
    heap->heapArr[0] = heap->heapArr[heap->last];
    heap->last = heap->last - 1;
    _reheapDown(heap, 0);
    return  1;
}

/*
return 1 if the heap is empty; 0 if not
*/
int heap_Empty(  HEAP *heap){
    if(heap->last == -1){
        return 1;
    }else{
        return 0;
    }
}

/* Print heap array */
void heap_Print( HEAP *heap, void (*print_func) (void *data)){
    for(int i = 0; i <= heap->last; i++){
        print_func(heap->heapArr[i]);
    }
    printf("\n");
}