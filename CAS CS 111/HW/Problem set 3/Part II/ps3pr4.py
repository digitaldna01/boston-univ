#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 23:52:25 2019

@author: leejaehong
"""
# 
# ps3pr4.py - Problem Set 3, Problem 4
#
# More algorithm design!
#

# function 1 
def index(elem, seq):
    """ return the index of the first occurance of elem in seq
        input elem: an element, seq: a sequence or string
    """
    if seq == [] or seq ==  '':
        return  -1
    elif seq[0] == elem: 
        return 0
    else:
        seq_rest = index(elem, seq[1:])
        if seq_rest == -1:
            return  -1
        else:
            return 1 + seq_rest

# function 2 
def index_last(elem, seq):
    """takes as inputs an element elem and a sequence seq, and that uses 
        recurion to find and return the index of the last occurence of elem in 
        seq
        input elem: an element, seq: a sequence
    """
    if seq  == [] or seq == '':
        return -1
    elif seq[-1] == elem:
        return len(seq) - 1
    else:
        return index_last(elem,seq[0:-1])
    
# function 3
# helper function
def rem_first(elem, values):
    """removes the first occurrence of elem from the list values
    """
    if values == '':
        return ''
    elif values[0] == elem:
        return values[1:]
    else:
        result_rest = rem_first(elem, values[1:])
        return values[0] + result_rest


def jscore(s1,s2):
    """takes two strings s1 and s2 as inputs and returns the jotto score of s1
        compared with s2
        input s1, s2: string
    """
    if s1 == '' or s2 == '' :
        return 0 
    elif s1[0] in s2:
        return 1 + jscore(s1[1:],rem_first(s1[0], s2))
    else:
        return jscore(s1[1:], s2)
        
# test function with a sample test call for functions
def test():
    """ performs test calls on the functions above """
    print('function 1 test')
    print('index(5,[4,10,5,3,7,5]) return', index(5,[4,10,5,3,7,5]))
    print('index("hi",["well","hi","there"]) return', index('hi',['well','hi','there']))
    print('index("b","banana"]) return', index('b','banana'))
    print('index("a","banana") return', index('a','banana'))
    print('index("i", "team") return', index('i','team'))
    print('index("hi",["hello",111,True]) return', index('hi',['hello',111,True]))
    print('index("a","") return', index('a',''))
    print('index(42,[]) return', index(42,[]))
    print( 'function 2 test')
    print('index_last(5,[4,10,5,3,7,5]) return',index_last(5,[4,10,5,3,7,5]))
    print('index_last("hi",["well","hi","there"]) return', index_last('hi',['well','hi','there']))
    print('index_last("b","banana"]) return', index_last('b','banana'))
    print('index_last("n","banana") return', index_last('n','banana'))
    print('index_last("i", "team") return', index_last('i','team'))
    print('index_last("hi",["hello",111,True]) return', index_last('hi',['hello',111,True]))
    print('index_last("a","") return', index_last('a',''))
    print('index_last(42,[]) return', index_last(42,[]))
    print('function 3 test')
    print('jscore("diner","syrup") return', jscore('diner','syrup'))
    print('jscore("always","bananas") return', jscore('always','bananas'))
    print('jscore("always","walking") return', jscore('always','walking'))
    print('jscore("recursion","excursion") return', jscore('recursion','excursion'))
    print('jscore("recursion","") return', jscore('recursion',''))
    
    
        