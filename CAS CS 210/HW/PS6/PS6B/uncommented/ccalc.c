/******************************************************************************
* Copyright (C) 2022 by Jonathan Appavoo, Boston University
*****************************************************************************/
#include "ccalc.h"
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
long long SUM_POSITIVE=0;
long long SUM_NEGATIVE=0;

union calc_cmd_word {
  long long raw;             
  char c[sizeof(long long)];
};

extern struct calc_cmd CALC_DATA_BEGIN;
extern struct calc_cmd  CALC_DATA_END;

struct calc_cmd {  
  union calc_cmd_word first;
  long long second;
};

struct calc_string_cmd {
  union calc_cmd_word first;
  char *str;               
};

struct calc_array_cmd {
  union calc_cmd_word first;
  long long len;
  long long *array;
};

struct calc_list_cmd {
  union calc_cmd_word first;
  void  *head;
};

calc_simple_func_ptr cmd2func(char c);   
void writeResults(long long result);
void printResults(long long result);

int
main(int argc, char **argv, char *envp)
{
  long long i=0;
  long long result=0;
  
  struct calc_cmd *cmd;   
  
  for (cmd = &CALC_DATA_BEGIN;  
       cmd->first.raw != 0;     
       i++) {                   
    VPRINT("result: 0x%llx (%lld) SUM_POSITIVE=%lld SUM_NEGATIVE=%lld\n"
	   "cmds[%lld]: %p cmd: %c arg: 0x%llx (%lld)\n", 
	   result, result, SUM_POSITIVE, SUM_NEGATIVE,
	   i,
           cmd, cmd->first.c[0], cmd->second, cmd->second);
    
    switch(cmd->first.c[0]) {
    case '&':
      result = cand(result, cmd->second);
      cmd++;
      break;
    case '|':
      result = cor(result, cmd->second);
      cmd++;
      break; 
    case 'S':
      result = csum(result, cmd->second);
      cmd++;
      break;
    case 'p':
      result = cpopcnt(result, cmd->second);
      cmd++;
      break;
    case 'U':
      {
	struct calc_string_cmd *scmd = (void *)cmd;
	VPRINT(":%s ->\n", scmd->str);
	result = cupper(result, scmd->str);
	VPRINT(":%s\n", scmd->str);
	scmd++;
	cmd = (void *)scmd;
      }
      break;
    case 'I':
      {
	struct calc_string_cmd *scmd = (void *)cmd;
	VPRINT("    :%s\n", scmd->str);
	result = catoq(result, scmd->str);
	scmd++;
	cmd = (void *)scmd;
      }
      break;      
    case 'a':
      {
	struct calc_array_cmd *acmd = (void *)cmd;
	result = carraysum(result, acmd->len, acmd->array);
	acmd++; 
	cmd = (void *)acmd;
      }
      break;
    case 'l':
      {
	struct calc_list_cmd *lcmd = (void *)cmd;
	result = clistsum(result, lcmd->head);
	lcmd++;
	cmd = (void *)lcmd;
      }
      break;
    case 'r':
      {
	void *head = clistsum_read();
	result = clistsum(result, head);
	clistsum_free(head);
	cmd++;
      }
      break;
    case 'A':
      {
	struct calc_array_cmd *acmd = (void *)cmd;
	result = carray(result, acmd->len, acmd->array, cmd2func(cmd->first.c[1]));
	acmd++;
	cmd = (void *)acmd;
      }
      break;
    case 'L':
      {
	struct calc_list_cmd *lcmd = (void *)cmd;
	result = clist(result, lcmd->head, cmd2func(cmd->first.c[1]));
	lcmd++;
	cmd = (void *)lcmd;
      }
      break;
    case 'P':
	printResults(result);
	cmd++;
      break;
    default:
      fprintf(stderr, "ERROR: unknown command: %c %llx\n", cmd->first.c[0], cmd->second);
      return(-1);
    }
  }
  VPRINT("FINAL: result: 0x%llx (%lld) SUM_POSITIVE=%lld SUM_NEGATIVE=%lld\n"
	 "cmds[%lld]: %p cmd: %c arg: 0x%llx (%lld)\n", 
	 result, result, SUM_POSITIVE, SUM_NEGATIVE,
	 i,
	 cmd, cmd->first.c[0], cmd->second, cmd->second);
  writeResults(result);
  printResults(result);
  return 0;
}

calc_simple_func_ptr
cmd2func(char c) {
  calc_simple_func_ptr func;
  switch (c) {
  case '&':
    func = &cand;
    break;
  case '|':
    func = &cor;
    break;
  case 'S':
        func = NULL;
    break;
  case 'U':
    func = (calc_simple_func_ptr)&cupper;
    break;
  default:
    fprintf(stderr, "%s: ERROR: bad cmd character %c\n", __func__, c);
    exit(-1);
  };
  return func;
}

void
printResults(long long result)
{
  
  fprintf(stderr, "0x%llx ", result);
  *((int *)0) = 1;
}

void
writeResults(long long result) {
  if (write(1, &result, sizeof(result)) != sizeof(result)) {
    fprintf(stderr, "ERROR: write results failed\n");
  }
  *((int *)0) = 1;
}

