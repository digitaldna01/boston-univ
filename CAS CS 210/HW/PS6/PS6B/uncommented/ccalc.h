/******************************************************************************
* Copyright (C) 2022 by Jonathan Appavoo, Boston University
*****************************************************************************/
#ifndef __CCALC_H__       
#define __CCALC_H__

extern long long SUM_POSITIVE;
extern long long SUM_NEGATIVE;

typedef long long (*calc_simple_func_ptr)(long long, long long);

long long cand(long long x, long long y);
long long cor(long long x, long long y);
long long csum(long long x, long long y);
long long cpopcnt(long long x, long long y);
long long cupper(long long x, char *cptr);				     
long long catoq(long long x, char *cptr);
long long carraysum(long long x, long long len, long long *array);
long long clistsum(long long x, void *head);

long long carray(long long x, long long len, long long *array, calc_simple_func_ptr func);
long long clist(long long x, void *head, calc_simple_func_ptr func);

void *clistsum_read(void);
void clistsum_free(void *head);

#ifdef VERBOSE
#define VPRINT(fmt, ...) fprintf(stderr, "%s: " fmt, __func__,__VA_ARGS__)
#else
#define VPRINT(...)
#endif

#endif  // __CCALC_H__
