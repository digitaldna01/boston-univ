#include <stdlib.h> // malloc
#include <stdio.h>
#include <string.h> // strdup, strcmp
#include <ctype.h> // toupper

#define QUIT			1
#define FORWARD_PRINT	2
#define BACKWARD_PRINT	3
#define SEARCH			4
#define DELETE			5
#define COUNT			6

// User structure type definition
typedef struct 
{
	char	*name;	// 이름
	int		freq;	// 빈도
} tName;

////////////////////////////////////////////////////////////////////////////////
// LIST type definition
typedef struct node
{
	tName		*dataPtr;
	struct node	*llink;
	struct node	*rlink;
} NODE;

typedef struct
{
	int		count;
	NODE	*head;
	NODE	*rear;
} LIST;

////////////////////////////////////////////////////////////////////////////////
// Prototype declarations

// Allocates dynamic memory for a list head node and returns its address to caller
// return	head node pointer
// 			NULL if overflow
LIST *createList(void);

//  이름 리스트에 할당된 메모리를 해제 (head node, data node, name data)
void destroyList( LIST *pList);

// Inserts data into list
//	return	0 if overflow
//			1 if successful
//			2 if duplicated key
int addNode( LIST *pList, tName *dataInPtr);

// Removes data from list
//	return	0 not found
//			1 deleted
int removeNode( LIST *pList, tName *keyPtr, tName **dataOutPtr);

// interface to search function
//	pArgu	key being sought
//	dataOutPtr	contains found data
//	return	1 successful
//			0 not found
int searchList( LIST *pList, tName *pArgu, tName **dataOutPtr);

// returns number of nodes in list
int countList( LIST *pList);

// returns	1 empty
//			0 list has data
int emptyList( LIST *pList);

// traverses data from list (forward)
void traverseList( LIST *pList, void (*callback)(const tName *));

// traverses data from list (backward)
void traverseListR( LIST *pList, void (*callback)(const tName *));

// internal insert function
// inserts data into list
// return	1 if successful
// 			0 if memory overflow
static int _insert( LIST *pList, NODE *pPre, tName *dataInPtr);

// internal delete function
// deletes data from list and saves the (deleted) data to dataOutPtr
static void _delete( LIST *pList, NODE *pPre, NODE *pLoc, tName **dataOutPtr);

// internal search function
// searches list and passes back address of node containing target and its logical predecessor
// return	1 found
// 			0 not found
// searchlist에서 사용
static int _search( LIST *pList, NODE **pPre, NODE **pLoc, tName *pArgu);

// 응용 프로그램 개발자
////////////////////////////////////////////////////////////////////////////////
// Allocates dynamic memory for a name structure, initialize fields(name, freq) and returns its address to caller
//	return	name structure pointer
//			NULL if overflow
tName *createName( char *name, int freq); 

// Deletes all data in name structure and recycles memory
void destroyName( tName *pNode);

////////////////////////////////////////////////////////////////////////////////
// gets user's input
int get_action()
{
	char ch;
	scanf( "%c", &ch);
	ch = toupper( ch);
	switch( ch)
	{
		case 'Q':
			return QUIT;
		case 'P':
			return FORWARD_PRINT;
		case 'B':
			return BACKWARD_PRINT;
		case 'S':
			return SEARCH;
		case 'D':
			return DELETE;
		case 'C':
			return COUNT;
	}
	return 0; // undefined action
}

// compares two names in name structures
// for createList function
int cmpName( const tName *pName1, const tName *pName2)
{
	return strcmp( pName1->name, pName2->name);
}

// prints contents of name structure
// for traverseList and traverseListR functions
void print_name(const tName *dataPtr)
{
	printf( "%s\t%d\n", dataPtr->name, dataPtr->freq);
}

// increases freq in name structure
// for addNode function
void increase_freq(tName *dataOutPtr, const tName *dataInPtr)
{
	dataOutPtr->freq += dataInPtr->freq;
}

////////////////////////////////////////////////////////////////////////////////
int main( int argc, char **argv)
{
	LIST *list;
	
	char name[100];
	int freq;
	
	tName *pName;
	int ret;
	FILE *fp;
	
	if (argc != 2){
		fprintf( stderr, "usage: %s FILE\n", argv[0]);
		return 1;
	}
	
	fp = fopen( argv[1], "rt");
	if (!fp)
	{
		fprintf( stderr, "Error: cannot open file [%s]\n", argv[1]);
		return 2;
	}
	
	// creates an empty list
	list = createList();
	if (!list)
	{
		printf( "Cannot create list\n");
		return 100;
	}
	
	while(fscanf( fp, "%*d\t%s\t%*c\t%d", name, &freq) != EOF)
	{
		pName = createName( name, freq);
		
		//ret = addNode( list, pName);
		
		if (ret == 2) // duplicated
		{
			destroyName( pName);
		}
	}
	
	fclose( fp);
	
	fprintf( stderr, "Select Q)uit, P)rint, B)ackward print, S)earch, D)elete, C)ount: ");
	
	while (1)
	{
		tName *ptr;
		int action = get_action();
		
		switch( action)
		{
			case QUIT:
				destroyList( list);
				return 0;
			
			case FORWARD_PRINT:
				//traverseList( list, print_name);
				break;
			
			case BACKWARD_PRINT:
				//traverseListR( list, print_name);
				break;
			
			case SEARCH:
				fprintf( stderr, "Input a name to find: ");
				fscanf( stdin, "%s", name);
				
				pName = createName( name, 0);

				//if (searchList( list, pName, &ptr)) print_name( ptr);
				//else fprintf( stdout, "%s not found\n", name);
				
				destroyName( pName);
				break;
				
			case DELETE:
				fprintf( stderr, "Input a name to delete: ");
				fscanf( stdin, "%s", name);
				
				pName = createName( name, 0);

				//if (removeNode( list, pName, &ptr))
				//{
				//	fprintf( stdout, "(%s, %d) deleted\n", ptr->name, ptr->freq);
				//	destroyName( ptr);
				//}
				//else fprintf( stdout, "%s not found\n", name);
				
				destroyName( pName);
				break;
			
			case COUNT:
				fprintf( stdout, "%d\n", countList( list));
				break;
		}
		
		if (action) fprintf( stderr, "Select Q)uit, P)rint, B)ackward print, S)earch, D)elete, C)ount: ");
	}
	return 0;
}

////////////////////////////////////////////////////////////////////////////////
LIST *createList(void){
	LIST *newList = (LIST *)malloc(sizeof(LIST));
	if(!newList){
		return NULL;
	}
	newList->count = 0;
	newList->head = NULL;
	newList->rear = NULL;

	return newList;
}

//  이름 리스트에 할당된 메모리를 해제 (head node, data node, name data)
void destroyList( LIST *pList){
	NODE *curr = pList->head;

	while(curr != NULL){
		NODE *nodePtr = curr->llink;
		tName *nameptr = curr->dataPtr;
		destroyName(nameptr);
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
int addNode( LIST *pList, tName *dataInPtr){
	tName *foundPtr = NULL;
	
	if(searchList(pList, dataInPtr, &foundPtr) == 1){
		increase_freq(foundPtr, dataInPtr);
		return 2;
	}else{	
		//to insert a node into a null list
		//
		//
		//to insert a node between two nodes
		//
		NODE *pPre = NULL;

		if(_insert(pList, , dataInPtr) == 1){
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
int removeNode( LIST *pList, tName *keyPtr, tName **dataOutPtr);

// interface to search function
//	pArgu	key being sought
//	dataOutPtr	contains found data
//	return	1 successful
//			0 not found
int searchList( LIST *pList, tName *pArgu, tName **dataOutPtr){
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
void traverseList( LIST *pList, void (*callback)(const tName *));

// traverses data from list (backward)
void traverseListR( LIST *pList, void (*callback)(const tName *));

// internal insert function
// inserts data into list
// return	1 if successful
// 			0 if memory overflow
static int _insert( LIST *pList, NODE *pPre, tName *dataInPtr){
	//NODE 메모리 할당 후 연결
	NODE *newNode = (NODE *)malloc(sizeof(NODE));
	if(!newNode){
		return 0;
	}
	newNode->dataPtr = dataInPtr;
	
	//to insert a node into a null list
	if(pPre == NULL){
		//set new node back pointer to null
		//set new node forward pointer to list head
		// set list head to new node
	}else{
		//to insert a node between two nodes
		//
		//to insert a node at the end of the list
	}
	
	

	newNode->rlink = pPre;
	newNode->llink = pPre->llink;
	pPre->llink->rlink = newNode;
	pPre->llink = newNode;
	return 1;
}

// internal delete function
// deletes data from list and saves the (deleted) data to dataOutPtr
static void _delete( LIST *pList, NODE *pPre, NODE *pLoc, tName **dataOutPtr);

// internal search function
// searches list and passes back address of node containing target and its logical predecessor
// return	1 found
// 			0 not found
// searchlist에서 사용
static int _search( LIST *pList, NODE **pPre, NODE **pLoc, tName *pArgu){
	while(((*pLoc) != NULL) && (cmpName((*pLoc)->dataPtr, pArgu) < 0)){
		*pPre = *pLoc;
		*pLoc = (*pLoc)->llink;
	}
	if((*pLoc) == NULL){
		return 0;
	}else{
		if(cmpName((*pLoc)->dataPtr, pArgu) == 0){
			return 1;
		}else{
			return 0;
		}
	}
	return 0;
	
}

// 응용 프로그램 개발자
////////////////////////////////////////////////////////////////////////////////
// Allocates dynamic memory for a name structure, initialize fields(name, freq) and returns its address to caller
//	return	name structure pointer
//			NULL if overflow
tName *createName( char *name, int freq){
	tName *newName = (tName *)malloc(sizeof(tName));
	if(!newName){
		return NULL;
	}
	//TODO check char ptr works
	newName->name = name;
	newName->freq = freq;

	return newName;
}


// Deletes all data in name structure and recycles memory
void destroyName( tName *pNode){
	tName *ptr = pNode;
	ptr->name = NULL;
	ptr->freq = 0;

	free(ptr);
}