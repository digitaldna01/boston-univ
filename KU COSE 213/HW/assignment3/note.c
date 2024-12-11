#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define MAX_YEAR_DURATION	10	// 기간

// 이름 구조체 선언
typedef struct {
	char	name[20];				// 이름
	char	sex;					// 성별 M or F
	int		freq[MAX_YEAR_DURATION]; // 연도별 빈도
} tName;

////////////////////////////////////////////////////////////////////////////////
// LIST type definition
typedef struct node
{
	tName		*dataPtr;
	struct node	*link;
} NODE; //노드 구조체

typedef struct
{
	int		count;
	NODE	*head;
} LIST; //head 구조체

////////////////////////////////////////////////////////////////////////////////
// Prototype declarations

// Allocates dynamic memory for a list head node and returns its address to caller
// return	head node pointer
// 			NULL if overflow
// 헤드 리스트 구조체를 만들고 리스트의 주소를 리턴
LIST *createList(void); 

//  이름 리스트에 할당된 메모리를 해제 (head node, data node, name data)
//  아무것도 남지 않도록 모든 메모리를 해제 
void destroyList( LIST *pList);

// internal insert function
// inserts data into a new node
// return	1 if successful
// 			0 if memory overflow
// ordered list이기 때문에 적절한 위치를 찾아서 삽입
static int _insert( LIST *pList, NODE *pPre, tName *dataInPtr);

// internal search function
// searches list and passes back address of node containing target and its logical predecessor
// return	1 found
// 			0 not found
// 수업에서 배웠던 그 내용 그대로를 구현하면 된다
// 이걸 잘 만들어 두어야 다음 과제에서도 사용가능
static int _search( LIST *pList, NODE **pPre, NODE **pLoc, tName *pArgu);

// 이름 구조체를 위한 메모리를 할당하고, 이름(name)과 성별(sex)을 초기화
// return	할당된 이름 구조체에 대한 pointer
//			NULL if overflow
// 이름 구조체의 메모리를 할당하고 구조체를 만들고 초기화, 빈도는 년도와 나중에 추가하면서 초기화
tName *createName( char *name, char sex); 

//  이름 구조체에 할당된 메모리를 해제
// 쓸모 없어진 이름 구조체를 해제
void destroyName( tName *pNode);

////////////////////////////////////////////////////////////////////////////////
// 입력 파일을 읽어 이름 정보(연도, 이름, 성별, 빈도)를 이름 리스트에 저장
// 이미 리스트에 존재하는(저장된) 이름은 해당 연도의 빈도만 저장
// 새로 등장한 이름은 리스트에 추가
// 주의사항: 동일 이름이 남/여 각각 사용될 수 있으므로, 이름과 성별을 구별해야 함
// 주의사항: 정렬 리스트(ordered list)를 유지해야 함
// start_year : 시작 연도 (2009)
void load_names( FILE *fp, int start_year, LIST *list);

// 이름 리스트를 화면에 출력
// 리스트 전체를 쭉 순회하면서 필요한 정보를 출력
void print_names( LIST *pList, int num_year);

////////////////////////////////////////////////////////////////////////////////
// compares two names in name structures
// for _search function
// search 함수를 위한것 --> 작성을 해주셨음
static int cmpName( const tName *pName1, const tName *pName2)
{
	int ret = strcmp( pName1->name, pName2->name);
	if (ret == 0) return pName1->sex - pName2->sex;
	else return ret;
}

////////////////////////////////////////////////////////////////////////////////
int main( int argc, char **argv)
{
	LIST *list;
	FILE *fp;
	
	if (argc != 2){
		fprintf( stderr, "usage: %s FILE\n\n", argv[0]);
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

	// 입력 파일로부터 이름 정보를 리스트에 저장
	load_names( fp, 2009, list);
	
	fclose( fp);
	
	// 이름 리스트를 화면에 출력
	print_names( list, MAX_YEAR_DURATION);
	
	// 이름 리스트 메모리 해제
	destroyList( list);
	
	return 0;
}

LIST *createList(void){
	LIST *newList = (LIST *)malloc(sizeof(LIST));
	if(!newList){
		return NULL;
	}
	newList->count = 0;
	newList->head = NULL;

	return newList;
}
//  이름 리스트에 할당된 메모리를 해제 (head node, data node, name data)
//  아무것도 남지 않도록 모든 메모리를 해제 
void destroyList( LIST *pList){
    NODE *curr = pList->head;

	while(curr != NULL){
        NODE *nodePtr = curr->link;
	    tName *namePtr = curr->dataPtr;
        destroyName(namePtr);
        free(curr);
		curr = nodePtr;
	}
	pList->count = 0;
	free(pList);
	// printf("destroy List success\n");
}

// internal insert function
// inserts data into a new node
// return	1 if successful
// 			0 if memory overflow
// ordered list이기 때문에 적절한 위치를 찾아서 삽입
static int _insert( LIST *pList, NODE *pPre, tName *dataInPtr){
	
	NODE *newNode = (NODE *)malloc(sizeof(NODE));
	if(!newNode){
		return 0;
	}
	newNode->link = NULL;
	newNode->dataPtr = dataInPtr;
    
	if(pPre == NULL){
		newNode->link = pList->head;
		pList->head = newNode;
		return 1;
	}else{
		newNode->link = pPre->link;
		pPre->link = newNode;
		return 1;
	}
}

// internal search function
// searches list and passes back address of node containing target and its logical predecessor
// return	1 found
// 			0 not found
// 수업에서 배웠던 그 내용 그대로를 구현하면 된다 -> 수업시간에는 한번에 전체 리스트를 보는것 
// 이걸 잘 만들어 두어야 다음 과제에서도 사용가능
static int _search( LIST *pList, NODE **pPre, NODE **pLoc, tName *pArgu){
	while(((*pLoc) != NULL) && (cmpName((*pLoc)->dataPtr, pArgu) < 0)){
		*pPre = *pLoc;
		*pLoc = (*pLoc)->link;
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

tName *createName( char *name, char sex){
	tName *newName = (tName *)malloc(sizeof(tName));
	if(!newName){
		return NULL;
	}
	strcpy(newName->name, name);
	newName->sex = sex;
	for(int i = 0; i < MAX_YEAR_DURATION; i++){
		newName->freq[i] = 0;
	}
	return newName;
}

//  이름 구조체에 할당된 메모리를 해제
// 쓸모 없어진 이름 구조체를 해제
void destroyName( tName *pNode){
	tName *ptr = pNode;
	strcpy(ptr->name, "");
	ptr->sex = 0;
	for (int i = 0; i < MAX_YEAR_DURATION; i++){
		ptr->freq[i] = 0;
	}

	free(ptr);
}

////////////////////////////////////////////////////////////////////////////////
// 입력 파일을 읽어 이름 정보(연도, 이름, 성별, 빈도)를 이름 리스트에 저장
// 이미 리스트에 존재하는(저장된) 이름은 해당 연도의 빈도만 저장
// 새로 등장한 이름은 리스트에 추가
// 주의사항: 동일 이름이 남/여 각각 사용될 수 있으므로, 이름과 성별을 구별해야 함
// 주의사항: 정렬 리스트(ordered list)를 유지해야 함
// start_year : 시작 연도 (2009)
void load_names( FILE *fp, int start_year, LIST *list){
	tName *newName;

	const int max = 255;
	char line[max], name[20], gender;
	int year = 0, freq_value = 0;

	while(fgets(line, sizeof(line), fp) != NULL){
		sscanf(line, "%d %s %c %d", &year, name, &gender, &freq_value);
		newName = createName(name, gender);  
        
		NODE *Pre = NULL;
		NODE *Loc = (list->head);

		if(_search(list, &Pre, &Loc, newName) == 1){
			Loc->dataPtr->freq[year - start_year] = freq_value;
			free(newName);
		}else{
			if(_insert(list, Pre, newName) == 1){
				newName->freq[year - start_year] = freq_value;
				list->count++;
			}else{
				printf("memory overflow");
			}
		}
	}
}

// 이름 리스트를 화면에 출력
// 리스트 전체를 쭉 순회하면서 필요한 정보를 출력
void print_names( LIST *pList, int num_year){
	NODE *ptr = pList->head;
	while(ptr != NULL){
		printf("%s", ptr->dataPtr->name);
		printf("\t%c", ptr->dataPtr->sex);
		for(int i = 0; i < num_year; i++){
			printf("\t%d", ptr->dataPtr->freq[i]);
		}
		printf("\n");
		ptr = ptr->link;
	}
}
