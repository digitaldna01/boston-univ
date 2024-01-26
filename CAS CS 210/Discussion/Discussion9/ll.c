#include <stdio.h>
#include <stdlib.h>

/* Definition of a linked list node */
struct Node {
  int num;
  struct Node *next;
  struct Node *prev;
};

// Global pointer to the current node
// if this pointer is null then the list is empty
struct Node *cur = NULL;

/* insertbefore */
/* Accepts an int and modifies the list to include a new node inserted       */
/* before the current node if the list is empty then a single node list is   */
/* created with the new node the new node contains the int passed as an      */
/* argument */
void 
insertbefore(int num)
{
  struct Node *newNode;
  struct Node *previous;

  /* Allocate memory for the new node */
  newNode = (struct Node *)malloc(sizeof(struct Node));

  /* Check that the memory allocation worked */
  if (newNode == NULL) {
    printf("ERROR: Memory allocation failed\n");
    return;
  }

  newNode->num  = num;
  newNode->next = NULL;
  newNode->prev = NULL;

  /* If the list is empty, just set the list to have the new node */
  if (cur == NULL)  {
    cur = newNode;
    return;
  }

  previous = cur->prev;
  cur->prev = newNode;

  newNode->next = cur;
  newNode->prev = previous;

  /* if the node before the current node existed, then it now has to point
     forward to the new node */
  if (previous != NULL) {
    previous->next = newNode;
  }
}

/* insertafter */
/* Accepts an int and modifies the list to include a new node inserted after */
/* the current node if the list is empty then a single node list is created  */
/* with the new node the new node contains the int passed as an argument     */
void
insertafter(int num)
{
  ////////////////////////////////////////////////////////////////////////////
  //////////////////////////    IMPLEMENT ME    //////////////////////////////
  ////////////////////////////////////////////////////////////////////////////
  struct Node *newNode;

  /* Allocate memory for the new node */
  newNode = (struct Node *)malloc(sizeof(struct Node));

  /* Check that the memory allocation worked*/
  if(newNode == NULL){
    printf("Error: Memory allocation failed\n");
    return;
  }

  newNode->num = num;
  newNode->prev = NULL;
  newNode->next = NULL;

  /* If the list is empty, just set the list to have the new node*/
  if (cur == NULL){
    cur = newNode;
    return;
  }

  cur->next = newNode;
  newNode->prev = cur;
  cur = newNode;
}

/* rm */
/* removes the current node from the list */
/* if the list is empty, then this function has no effect */
/* the memory of the removed node must be freed */
void
rm(void)
{
  /////////////////////////////////////////////////////////////////////////////
  ///////////////////////////    IMPLEMENT ME    //////////////////////////////
  /////////////////////////////////////////////////////////////////////////////
  struct Node *temp;

  if (cur == NULL){
    return;
  }
  /* if there is a previous node to the current node remove current and previous is the current node */
  if (cur->prev != NULL){
    temp = cur;
    cur = cur->prev;
    free(temp);
    return;
  }

  /* if there is no previous but there is a next node then after the removal the next node should be the new current node */
  if(cur->next != NULL){
    temp = cur;
    cur = cur->next;
    free(temp);
    return;
  }

  /* if there is no previous and next then remove the current node and cur should be NULL */
  if(cur->prev == NULL && cur->next == NULL){
  temp = cur;
  cur = NULL;
  free(temp);
  return;
  }
}

/* clear */
/* removes all nodes from the list, freeing the memory */
/* calling this function will result in an empty list */
/* if the list is already empty, then this function has no effect */
void
clear()
{
  struct Node *temp;

  /* if the list is empty then its already done */
  if (cur == NULL) {
    return;
  }

  /* move the current pointer to the beginning of the list */
  while (cur->prev != NULL) {
    cur = cur->prev;
  }

  /* Free the nodes from the list */
  while (cur != NULL) {
    temp = cur;
    cur = cur->next;
    free(temp);
  }
}

/* display */
/* accepts a pointer to the node and displays the memory address of the node,*/
/* the number stored by the node, and the pointers to the previous and next  */
/* nodes in the list */
void
display(struct Node *n)
{
  if (n == NULL) {
    printf("NULL\n");
  } else {
    printf("Node: %p : num=%d\tnext=%p\tprev=%p\n", 
	   n, n->num, n->next, n->prev);
  }
}

/* displayall */
/* For each node in the list, displays the memory address of the node,      */
/* the number stored by the node, and the pointers to the previous and next */
/* nodes in the list if the list is empty, then this function has no effect */
void
displayall(void)
{
  struct Node *temp = cur;

  /* if the list is empty, nothing to display */
  if (temp == NULL) {
    return;
  }

  /* move the pointer to the beginning of the list */
  while (temp->prev) {
    temp = temp->prev;
  }

  /* display each node in the list */
  while (temp != NULL) {
    display(temp);
    temp = temp->next;
  }
}

/* forward */
/* moves the current pointer forward */
/* if the pointer is currently at the end of the list or the list is empty, */
/* this function has no effect */
void
forward(void)
{
  if (cur != NULL && cur->next != NULL) {
    cur=cur->next;
  }
}

/* backward */
/* moves the current pointer backward */
/* if the pointer is currently at the beginning of the list or the list is */
/* empty, this function has no effect */
void
backward(void)
{
  ////////////////////////////////////////////////////////////////////////////
  //////////////////////////    IMPLEMENT ME    //////////////////////////////
  ////////////////////////////////////////////////////////////////////////////
  if(cur != NULL && cur->prev != NULL){
    cur=cur->prev;
  }
}

/* docmd */
/* accepts a character representing the command requested by the user */
/* and calls the appropriate function */
int 
docmd(char cmd)
{
  int rc = 1;

  switch (cmd) {
  case 'd':
    display(cur);
    break;
  case 'D':
    displayall();
    break;
  case 'f':
    forward();
    break;
  case 'b': 
    backward();
    break;
  case 'I': {
    int val;
    scanf("%d", &val);
    insertbefore(val);
  }
    break;
  case 'i': {
    int val;
    scanf("%d", &val);
    insertafter(val);
  }
    break;
  case 'r':
    rm();
    break;
  case 'c':
    clear();
    break;
  case 'q':
    rc = 0;
    break;
  case '\n':
    break;
  default:
    printf("Unknown Command\n");
  }
  return rc;
}

/* main */
/* continuously reads a character from stdin and calls docmd to dispatch the */
/* command */
int
main(int argc, char **argv)
{
  char cmd;
  int rc;

  while (1) {
    scanf("%c", &cmd);
    rc = docmd(cmd);
    if (rc == 0) break;
  }
  return 0;
}
