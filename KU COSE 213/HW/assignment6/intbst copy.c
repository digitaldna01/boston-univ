#include <stdlib.h> // malloc, atoi, rand
#include <stdio.h>
#include <assert.h>
#include <time.h> // time

#define RANDOM_INPUT	1
#define FILE_INPUT		2

////////////////////////////////////////////////////////////////////////////////
// TREE type definition
typedef struct node
{
	int			data;
	struct node	*left;
	struct node	*right;
} NODE;

typedef struct
{
	NODE	*root;
} TREE;

////////////////////////////////////////////////////////////////////////////////
// Prototype declarations

/* Allocates dynamic memory for a tree head node and returns its address to caller
	return	head node pointer
			NULL if overflow
*/
TREE *BST_Create( void);

/* Deletes all data in tree and recycles memory
*/
// 데이터 노드들도 따라다니며 다 해제 해야함 그리고 자기자신(head node) 해제
void BST_Destroy( TREE *pTree);

/* internal function (not mandatory)
*/
//root부터 받아서 내부를 recursively 데이터 노드들을 정리
// 참고용 이렇게 하지 않아도 된다
static void _destroy( NODE *root);

/* Inserts new data into the tree
	return	1 success
			0 overflow
*/
// _insert를 호출하여 사용
int BST_Insert( TREE *pTree, int data);

/* internal function (not mandatory)
*/
static NODE *_insert( NODE *root, int data);

// 숫자를 하나 받아서 데이터 노들 만들기
NODE *_makeNode( int data);

/* Deletes a node with dltKey from the tree
	return	1 success
			0 not found
*/
//삭제할 키를 받아서 내부에서 삭제
int BST_Delete( TREE *pTree, int dltKey);

/* internal function
	success is 1 if deleted; 0 if not
	return	pointer to root
*/
// 주로 작업
// root 노드부터 시작해서 삭제해야할 키를 받아서 해당되는 노드를 찾아서 삭제
//여러가지 경우 그림을 그려가면서 코드 작성
//삭제가 성공하면 success에 1을 삽입, 실패하면 0을 삽입
static NODE *_delete( NODE *root, int dltKey, int *success);

/* Retrieve tree for the node containing the requested key
	return	address of data of the node containing the key
			NULL not found
*/
int *BST_Retrieve( TREE *pTree, int key);

/* internal function
	Retrieve node containing the requested key
	return	address of the node containing the key
			NULL not found
*/
static NODE *_retrieve( NODE *root, int key);

/* prints tree using inorder traversal
*/
void BST_Traverse( TREE *pTree);
/* internal function (not mandatory)
*/
static void _traverse( NODE *root);

/* Print tree using inorder right-to-left traversal
*/
// 오른쪽에서 왼쪽방향으로의 inorder traversal 각 노드의 depth에 따라서 tap문자를 앞에 입력하고 찍으면 된다 
void printTree( TREE *pTree);

/* internal traversal function
*/
//level에 따라 tab문자를 몇개를 출력할것인지
static void _inorder_print( NODE *root, int level);

/* 
	return 1 if the tree is empty; 0 if not
*/
int BST_Empty( TREE *pTree);

////////////////////////////////////////////////////////////////////////////////
int main( int argc, char **argv)
{
	int mode; // input mode
	TREE *tree;
	int data;
	
	if (argc != 2)
	{
		fprintf( stderr, "usage: %s FILE or %s number\n", argv[0], argv[0]);
		return 1;
	}
	
	FILE *fp;
	
	if ((fp = fopen(argv[1], "rt")) == NULL)
	{
		mode = RANDOM_INPUT;
	}
	else mode = FILE_INPUT;
	
	// creates a null tree
	tree = BST_Create();
	
	if (!tree)
	{
		printf( "Cannot create a tree!\n");
		return 100;
	}

	//atoi 문자열을 숫자로 바꾸어 주는 함수
	if (mode == RANDOM_INPUT)
	{
		int numbers;
		numbers = atoi(argv[1]);
		assert( numbers > 0);

		fprintf( stdout, "Inserting: ");
		
		srand( time(NULL));
		for (int i = 0; i < numbers; i++)
		{
			data = rand() % (numbers*3) + 1; // random number (1 ~ numbers * 3)
			
			fprintf( stdout, "%d ", data);
			
			// insert function call
			int ret = BST_Insert( tree, data);
			if (!ret) break;
		}
	}
	else if (mode == FILE_INPUT)
	{
		fprintf( stdout, "Inserting: ");
		
		while (fscanf( fp, "%d", &data) != EOF)
		{
			fprintf( stdout, "%d ", data);
			
			// insert function call
			int ret = BST_Insert( tree, data);
			if (!ret) break;
		}
		fclose( fp);
	}
	
	fprintf( stdout, "\n");

	if (BST_Empty( tree))
	{
		fprintf( stdout, "Empty tree!\n");
		BST_Destroy( tree);
		return 0;
	}	

	// inorder traversal
	fprintf( stdout, "Inorder traversal: ");
	BST_Traverse( tree);
	fprintf( stdout, "\n");
	
	// print tree with right-to-left inorder traversal
	fprintf( stdout, "Tree representation:\n");
	printTree(tree);
	
	// while (1)
	// {
	// 	fprintf( stdout, "Input a number to delete: "); 
	// 	int num;
	// 	if (scanf( "%d", &num) == EOF) break;
		
	// 	//int ret = BST_Delete( tree, num);
	// 	// if (!ret)
	// 	// {
	// 	// 	fprintf( stdout, "%d not found\n", num);
	// 	// 	continue;
	// 	// }
		
	// 	// print tree with right-to-left inorder traversal
	// 	fprintf( stdout, "Tree representation:\n");
	// 	printTree(tree);
		
	// 	if (BST_Empty( tree))
	// 	{
	// 		fprintf( stdout, "Empty tree!\n");
	// 		break;
	// 	}
	// }
	
	BST_Destroy( tree);

	return 0;
}

/* Allocates dynamic memory for a tree head node and returns its address to caller
	return	head node pointer
			NULL if overflow
*/
TREE *BST_Create( void){
	TREE *newTree = (TREE *)malloc(sizeof(TREE));
	if(!newTree){
		return NULL;
	}
	newTree->root = NULL;

	return newTree;
}

/* Deletes all data in tree and recycles memory
*/
// 데이터 노드들도 따라다니며 다 해제 해야함 그리고 자기자신(head node) 해제
void BST_Destroy( TREE *pTree){
	_destroy(pTree->root);
	free(pTree);
}

/* internal function (not mandatory)
*/
//root부터 받아서 내부를 recursively 데이터 노드들을 정리
// 참고용 이렇게 하지 않아도 된다
static void _destroy( NODE *root){
	while(root != NULL){
		_destroy(root->left);
		_destroy(root->right);
		root->data = 0;
		free(root);
	}
}

/* Inserts new data into the tree
	return	1 success
			0 overflow
*/
// _insert를 호출하여 사용
int BST_Insert( TREE *pTree, int data){
	if
	pTree->root = _insert(pTree->root, data);
	if(!pTree){
		return 0;
	}
	return 1;
}

/* internal function (not mandatory)
*/
static NODE *_insert( NODE *root, int data){
	if(root == NULL){
		return _makeNode(data);
	}else{
		if(data < root->data){
			root->left = _insert(root->left, data);
			
		}else{
			root->right = _insert(root->right, data);
			printf("2");
		}
	}
}

// 숫자를 하나 받아서 데이터 노들 만들기
NODE *_makeNode( int data){
	NODE *newNode = (NODE *)malloc(sizeof(NODE));
	if(!newNode){
		return NULL;
	}
	newNode->data = data;
	newNode->left = NULL;
	newNode->right = NULL;
	return newNode;
}

/* Deletes a node with dltKey from the tree
	return	1 success
			0 not found
*/
//삭제할 키를 받아서 내부에서 삭제
// int BST_Delete( TREE *pTree, int dltKey){
// 	int *maker;
// 	if(pTree->root == NULL){
// 		return 0;
// 	}else{
// 		pTree->root = _delete(pTree, dltKey, maker);
// 		if(*maker == 1){
// 			return 1;
// 		}else{
// 			return 0;
// 		}
// 	}
// }

/* internal function
	success is 1 if deleted; 0 if not
	return	pointer to root
*/
// 주로 작업
// root 노드부터 시작해서 삭제해야할 키를 받아서 해당되는 노드를 찾아서 삭제
//여러가지 경우 그림을 그려가면서 코드 작성
//삭제가 성공하면 success에 1을 삽입, 실패하면 0을 삽입
// static NODE *_delete( NODE *root, int dltKey, int *success){
// 	NODE *ptr;
// 	NODE *delete;
// 	if(dltKey < root->data){
// 		root->left = _delete(root->left, dltKey, success);
// 	}else if(dltKey > root->data){
// 		root->right = _delete(root->right, dltKey, success);
// 	}else{
// 		if(dltKey == root->data){
// 			if(root->left == NULL){
// 				ptr = root->right;
// 				free(root);
// 				*success = 1;
// 				return ptr;
// 			}else if(root->right == NULL){
// 				ptr = root->left;
// 				free(root);
// 				*success = 1;
// 				return ptr;
// 			}else{
// 				delete = root;

// 			}
// 		}else{
// 			*success = 0;
// 			return root;
// 		}
// 	}
// }

/* Retrieve tree for the node containing the requested key
	return	address of data of the node containing the key
			NULL not found
*/
int *BST_Retrieve( TREE *pTree, int key){
	NODE *address;
	if(pTree->root == NULL){
		return NULL;
	}
	address = _retrieve(pTree->root, key);
	if(address != NULL){
		return &(address->data);
	}else{
		return NULL;
	}
}

/* internal function
	Retrieve node containing the requested key
	return	address of the node containing the key
			NULL not found
*/
static NODE *_retrieve( NODE *root, int key){
	if(key < root->data){
		return _retrieve(root->left, key);
	}else if(key > root->data){
		return _retrieve(root->right, key);
	}else{
		return root;
	}
}

/* prints tree using inorder traversal
*/
void BST_Traverse( TREE *pTree){
	_traverse(pTree->root);
}

/* internal function (not mandatory)
*/
static void _traverse( NODE *root){
	if(root != NULL){
		_traverse(root->left);
		printf("%d ", root->data);
		_traverse(root->right);
	}
}

/* Print tree using inorder right-to-left traversal
*/
// 오른쪽에서 왼쪽방향으로의 inorder traversal 각 노드의 depth에 따라서 tap문자를 앞에 입력하고 찍으면 된다 
void printTree( TREE *pTree){
	int level = 0;
	if(pTree->root != NULL){
		_inorder_print(pTree->root, level);
	}
}

/* internal traversal function
*/
//level에 따라 tab문자를 몇개를 출력할것인지
static void _inorder_print( NODE *root, int level){
	if(root != NULL){
		_inorder_print(root->right, level+1);

		for(int i = 0; i < level; i++){
			printf("'\t");
		}
		printf("%d", root->data);
		printf("\n");

		_inorder_print(root->left, level+1);
	}
}

/* 
	return 1 if the tree is empty; 0 if not
*/
int BST_Empty( TREE *pTree){
	if(pTree->root == NULL){
		return 1;
	}else{
		return 0;
	}
}