#include <stdlib.h> // malloc

#include "adt_dlist.h"

//adt 개발자 doubly linked list

// internal insert function
// inserts data into list
// return	1 if successful
// 			0 if memory overflow
static int _insert( LIST *pList, NODE *pPre, void *dataInPtr){
	//NODE 메모리 할당 후 연결
	NODE *newNode = (NODE *)malloc(sizeof(NODE));
	if(!newNode){
		return 0;
	}
	newNode->dataPtr = dataInPtr;
	
	//to insert a node into a null list
	if(pPre == NULL){
		newNode->rlink = NULL;
		newNode->llink = pList->head;
		pList->head = newNode;
	}else{
		//set new node forward pointer to predecessor forward pointer
		newNode->llink = pPre->llink;
		newNode->rlink = pPre;
		pPre->llink = newNode;
	}
	if(newNode->llink == NULL){
		//Inserting at end of list--set rear pointer
		pList->rear = newNode;
	}else{
		//Inserting in middle of list--point success to new ///////
		newNode->llink->rlink = newNode;
	}

	return 1;
}

// internal delete function
// deletes data from list and saves the (deleted) data to dataOutPtr
static void _delete( LIST *pList, NODE *pPre, NODE *pLoc, void **dataOutPtr){
	if(pPre != NULL){
		pPre->llink = pLoc->llink;
	}else{
		pList->head = pLoc->llink;
	}
	if(pLoc->llink != NULL){
		pLoc->llink->rlink = pPre;
	}else{
		pList->rear = pPre;
	}
	(*dataOutPtr) = pLoc->dataPtr;
 	free(pLoc); 
}

// internal search function
// searches list and passes back address of node containing target and its logical predecessor
// return	1 found
// 			0 not found
static int _search( LIST *pList, NODE **pPre, NODE **pLoc, void *pArgu){
	while(((*pLoc) != NULL) && (pList->compare((*pLoc)->dataPtr, pArgu) < 0)){
		*pPre = *pLoc;
		*pLoc = (*pLoc)->llink;
	}
	if((*pLoc) == NULL){
		return 0;
	}else{
		if(pList->compare((*pLoc)->dataPtr, pArgu) == 0){
			return 1;
		}else{
			return 0;
		}
	}
	return 0;
}

////////////////////////////////////////////////////////////////////////////////
// function declarations

// Allocates dynamic memory for a list head node and returns its address to caller
// return	head node pointer
// 			NULL if overflow
LIST *createList( int (*compare)(const void *, const void *)){
	LIST *newList = (LIST *)malloc(sizeof(LIST));
	if(!newList){
		return NULL;
	}
	newList->count = 0;
	newList->head = NULL;
	newList->rear = NULL;
	newList->compare = compare;

	return newList;
}

//  이름 리스트에 할당된 메모리를 해제 (head node, data node, name data)
void destroyList( LIST *pList, void (*callback)(void *)){
	NODE *curr = pList->head;

	while(curr != NULL){
		NODE *nodePtr = curr->llink;
		void *nameptr = curr->dataPtr;
		callback(nameptr);
		free(curr);
		curr = nodePtr;
	}
	pList->count = 0;
	free(pList);
}

// Inserts data into list
//	return	0 if overflow
//			1 if successful
//			2 if duplicated key
int addNode( LIST *pList, void *dataInPtr, void (*callback)(const void *, const void *)){
	if(!pList){
		return 0;
	}

	NODE *pPre = NULL;
	NODE *pLoc = (pList->head);
	
	if(_search(pList, &pPre, &pLoc, dataInPtr) == 1){
		callback(pLoc->dataPtr, dataInPtr);
		//duplicated key
		return 2;
	}else{
		if(_insert(pList, pPre, dataInPtr) == 1){
			pList->count++;
			//successful
			return 1;
		}else{
			//data overflow
			return 0;
		}
	}
}

// Removes data from list
//	return	0 not found
//			1 deleted
int removeNode( LIST *pList, void *keyPtr, void **dataOutPtr){
	if(keyPtr == NULL){
		return 0;
	}
	NODE *pPre = NULL;
	NODE *pLoc = (pList->head);

	if(_search(pList, &pPre, &pLoc, keyPtr) == 1){
		_delete(pList, pPre, pLoc, dataOutPtr);
		pList->count--;
		return 1;
	}else{
		return 0;
	}
}

// interface to search function
//	pArgu	key being sought
//	dataOutPtr	contains found data
//	return	1 successful
//			0 not found
int searchList( LIST *pList, void *pArgu, void **dataOutPtr){
	NODE *Pre = NULL;
	NODE *Loc = (pList->head);

	if(_search(pList, &Pre, &Loc, pArgu) == 1){
		(*dataOutPtr) = Loc->dataPtr;
		return 1;
	}else{
		return 0;
	}
}

// returns number of nodes in list
int countList( LIST *pList){
	return pList->count;
}

// returns	1 empty
//			0 list has data
int emptyList( LIST *pList){
	if(pList->count == 0){
		return 1;
	}else{
		return 0;
	}
}

// traverses data from list (forward)
void traverseList( LIST *pList, void (*callback)(const void *)){
	NODE *current = pList->head;

	while(current != NULL){
		callback(current->dataPtr);
		current = current->llink;
	}
}

// traverses data from list (backward)
void traverseListR( LIST *pList, void (*callback)(const void *)){
	NODE *current = pList->rear;

	while(current != NULL){
		callback(current->dataPtr);
		current = current->rlink;
	}
}

////////////////////////////////////////////////////////////////////////////////
