#define SHOW_STEP 1 // 제출시 0
#define BALANCING 1 // 제출시 1 (used in _insert function)

#include <stdlib.h> // malloc
#include <stdio.h>
#include <string.h> //strcmp, strdup

#define max(x, y)	(((x) > (y)) ? (x) : (y))

////////////////////////////////////////////////////////////////////////////////
// AVL_TREE type definition
typedef struct node
{
	char		*data;
	struct node	*left;
	struct node	*right;
	int			height;
} NODE;

typedef struct
{
	NODE	*root;
	int		count;  // number of nodes
} AVL_TREE;

////////////////////////////////////////////////////////////////////////////////
// Prototype declarations

/* Allocates dynamic memory for a AVL_TREE head node and returns its address to caller
	return	head node pointer
			NULL if overflow
*/
AVL_TREE *AVL_Create( void);

/* Deletes all data in tree and recycles memory
*/
void AVL_Destroy( AVL_TREE *pTree);

static void _destroy( NODE *root);

/* Inserts new data into the tree
	return	1 success
			0 overflow
*/
int AVL_Insert( AVL_TREE *pTree, char *data);

/* internal function
	This function uses recursion to insert the new data into a leaf node
	return	pointer to new root
*/
static NODE *_insert( NODE *root, NODE *newPtr);

static NODE *_makeNode( char *data);

/* Retrieve tree for the node containing the requested key
	return	address of data of the node containing the key
			NULL not found
*/
char *AVL_Retrieve( AVL_TREE *pTree, char *key);

/* internal function
	Retrieve node containing the requested key
	return	address of the node containing the key
			NULL not found
*/
static NODE *_retrieve( NODE *root, char *key);

/* Prints tree using inorder traversal
*/
void AVL_Traverse( AVL_TREE *pTree);
static void _traverse( NODE *root);

/* Prints tree using inorder right-to-left traversal
*/
void printTree( AVL_TREE *pTree);
/* internal traversal function
*/
static void _infix_print( NODE *root, int level);

/* internal function
	return	height of the (sub)tree from the node (root)
*/
static int getHeight( NODE *root);

//rotate를 하면서 높이가 달라지는것을 잘 확인해서 바꾸기
/* internal function
	Exchanges pointers to rotate the tree to the right
	updates heights of the nodes
	return	new root
*/
static NODE *rotateRight( NODE *root);

/* internal function
	Exchanges pointers to rotate the tree to the left
	updates heights of the nodes
	return	new root
*/
static NODE *rotateLeft( NODE *root);

////////////////////////////////////////////////////////////////////////////////
int main( int argc, char **argv)
{
	AVL_TREE *tree;
	char str[1024];
	
	if (argc != 2)
	{
		fprintf( stderr, "Usage: %s FILE\n", argv[0]);
		return 0;
	}
	
	// creates a null tree
	tree = AVL_Create();
	
	if (!tree)
	{
		fprintf( stderr, "Cannot create tree!\n");
		return 100;
	}

	FILE *fp = fopen( argv[1], "rt");
	if (fp == NULL)
	{
		fprintf( stderr, "Cannot open file! [%s]\n", argv[1]);
		return 200;
	}

	while(fscanf( fp, "%s", str) != EOF)
	{

#if SHOW_STEP
		fprintf( stdout, "Insert %s>\n", str);
#endif		
		// insert function call
		AVL_Insert( tree, str);

#if SHOW_STEP
		fprintf( stdout, "Tree representation:\n");
		printTree( tree);
#endif
	}
	
	fclose( fp);
	
#if SHOW_STEP
	fprintf( stdout, "\n");

	// inorder traversal
	fprintf( stdout, "Inorder traversal: ");
	AVL_Traverse( tree);
	fprintf( stdout, "\n");

	// print tree with right-to-left infix traversal
	fprintf( stdout, "Tree representation:\n");
	printTree(tree);
#endif

	// fprintf( stdout, "Height of tree: %d\n", tree->root->height);
	fprintf( stdout, "# of nodes: %d\n", tree->count);
	
	
	// retrieval
	char *key;
	fprintf( stdout, "Query: ");
	while( fscanf( stdin, "%s", str) != EOF)
	{
		key = AVL_Retrieve( tree, str);
		
		if (key) fprintf( stdout, "%s found!\n", key);
		else fprintf( stdout, "%s NOT found!\n", str);
		
		fprintf( stdout, "Query: ");
	}
	
	// destroy tree
	AVL_Destroy( tree);

	return 0;
}

////////////////////////////////////////////////////////////////////////////////
// Prototype declarations

/* Allocates dynamic memory for a AVL_TREE head node and returns its address to caller
	return	head node pointer
			NULL if overflow
*/
AVL_TREE *AVL_Create( void){
	AVL_TREE *newTree = (AVL_TREE *)malloc(sizeof(AVL_TREE));
	if(! newTree){
		return NULL;
	}

	newTree->count = 0;
	newTree->root = NULL;

	return newTree;
}

/* Deletes all data in tree and recycles memory
*/
void AVL_Destroy( AVL_TREE *pTree){
	_destroy(pTree->root);
    free(pTree);
}

static void _destroy( NODE *root){
	if(root != NULL){
        _destroy(root->left);
        root->left = NULL;
        _destroy(root->right);
        root->right = NULL;
		root->height = 0;
        root->data = 0;
        free(root);
    }
}

/* Inserts new data into the tree
	return	1 success
			0 overflow
*/
int AVL_Insert( AVL_TREE *pTree, char *data){
	NODE *newNode = _makeNode(data);
	if(pTree->count == 0){
		pTree->root = newNode;
		pTree->count = 1;
	}else{
		pTree->root = _insert(pTree->root, newNode);
		pTree->count = pTree->count + 1;
	}if(!pTree){
        return 0;
    }
    return 1;
	//그냥 _insert(pTree->root) 넣어야 할 듯
	// if(strcmp(data, pTree->root->data) < 0){
	// 	pTree->root->left = _insert(pTree->root->left, newNode);
	// }
}

/* internal function
	This function uses recursion to insert the new data into a leaf node
	return	pointer to new root
*/
static NODE *_insert( NODE *root, NODE *newPtr){
	if(root == NULL){
		return newPtr;
	}
	printf("0\n");
	if(strcmp(newPtr->data, root->data) < 0){
		root->left = _insert(root->left, newPtr);

	}else{
		root->right = _insert(root->right, newPtr);
		
	}

	root->height = max(getHeight(root->left), getHeight(root->right)) + 1;

	int balance = getHeight(root->left) - getHeight(root->right);
	if(balance > BALANCING && (strcmp(newPtr->data, root->left->data) < 0)){
		return rotateRight(root);
	}else if(balance > BALANCING && (strcmp(newPtr->data, root->left->data) >= 0)){
		root->left = rotateLeft(root->left);
		return rotateRight(root);
	}
	else if(balance < (-1 * BALANCING) && (strcmp(newPtr->data, root->left->data) > 0)){
		return rotateLeft(root);
	}else{
		root->right = rotateRight(root->right);
		return rotateLeft(root);
	}
}

static NODE *_makeNode( char *data){
	NODE *newNode = (NODE *)malloc(sizeof(NODE));
    if(!newNode){
        return NULL;
    }
    newNode->data = data;
    newNode->left = NULL;
    newNode->right = NULL;
	newNode->height = 1;

    return newNode;
}

/* Retrieve tree for the node containing the requested key
	return	address of data of the node containing the key
			NULL not found
*/
char *AVL_Retrieve( AVL_TREE *pTree, char *key){
	NODE *address;
	if(pTree->root == NULL){
		return NULL;
	}
	address = _retrieve(pTree->root, key);
	if(address != NULL){
		return address->data;
	}else{
		return NULL;
	}
}

/* internal function
	Retrieve node containing the requested key
	return	address of the node containing the key
			NULL not found
*/
static NODE *_retrieve( NODE *root, char *key){
	if(strcmp(key, root->data) < 0){
		return _retrieve(root->left, key);
	}else if(strcmp(key, root->data) > 0){
		return _retrieve(root->right, key);
	}else{
		return root;
	}
}

/* Prints tree using inorder traversal
*/
void AVL_Traverse( AVL_TREE *pTree){
	_traverse(pTree->root);
}

static void _traverse( NODE *root){
	if(root != NULL){
		_traverse(root->left);
		printf("%s ", root->data);
		_traverse(root->right);
	}
}

/* Prints tree using inorder right-to-left traversal
*/
void printTree( AVL_TREE *pTree){
	int level = 0;
	_infix_print(pTree->root, level);
}

/* internal traversal function
*/
static void _infix_print( NODE *root, int level){
	if(root != NULL){
		_infix_print(root->right, level+1);

		for(int i = 0; i < level; i++){
			printf("\t");
		}
		printf("%s", root->data);
		printf("\n");

		_infix_print(root->left, level+1);
	}
}

/* internal function
	return	height of the (sub)tree from the node (root)
*/
static int getHeight( NODE *root){
	if(root == NULL){
		return 0;
	}
	return root->height;
}

//rotate를 하면서 높이가 달라지는것을 잘 확인해서 바꾸기
/* internal function
	Exchanges pointers to rotate the tree to the right
	updates heights of the nodes
	return	new root
*/
//포인터 연산 후 높이가 달라지는 부분에 있어서 수정작업
// use getHeight
static NODE *rotateRight( NODE *root){
	NODE *child = root->left;
	NODE *grandchild = child->right;

	child->right = root;
	root->left = grandchild;

	root->height = max(getHeight(root->left), getHeight(root->right)) + 1;
	child->height = max(getHeight(child->left), getHeight(child->right)) + 1;

	return child;
}

/* internal function
	Exchanges pointers to rotate the tree to the left
	updates heights of the nodes
	return	new root
*/
static NODE *rotateLeft( NODE *root){
	NODE *child = root->right;
	NODE *grandchild = child->left;

	child->left = root;
	root->right = grandchild;

	root->height = max(getHeight(root->left), getHeight(root->right)) + 1;
	child->height = max(getHeight(child->left), getHeight(child->right)) + 1;

	return child;
}

////////////////////////////////////////////////////////////////////////////////