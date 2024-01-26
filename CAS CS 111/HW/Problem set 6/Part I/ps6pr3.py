#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:07:07 2019

@author: leejaehong
"""

#
# ps6pr3.py - problem set 6, problem 3
#
# Processing sequences with loops
#

# Problem 1
def double(s):
    """ takes an arbitrary string s as input, and that uses a loop to construct
        and return the string formed by doubling each character in the string.
        input s: string
    """
    result = ''
    for c in s:
        result += c * 2
    return result

# Problem 2
def weave(s1, s2):
    """ takes as inputs two strings s1 and s2 and uses a loop to construct and
        return a new string that is formed by 'weaving' together the characters
        in the strings s1 and s2 to create a single string.
        input: s1, s2: string
    """
    result = ''
    len_shorter = min(len(s1), len(s2))
    for i in range(len_shorter):
        result += s1[i] + s2[i]
    if len(s1) > len(s2):
        result += s1[-(len(s1) - len(s2)):]
    elif len(s1) == len(s2):
        result += ''
    else:
        result += s2[-(len(s2) - len(s1)):]
    return result
    
# Problem 3
def index(elem, seq):
    """ takes as inputs an element elem and a sequence seq, and that used a 
        loop to find and return the index of the first occurrence of elem in 
        seq.
        input elem: element of seq, seq: sequence of either str or int
    """
    for i in range(len(seq)):
        if seq[i] == elem:
            return i
    return -1

# test function with a sample test call for function 0
def test():
    """ performs test calls on the functions above """
    print("double('hello') return", double('hello'))
    print("double('python') return", double('python'))
    print("weave('aaaaaa','bbbbbb') return", weave('aaaaaa','bbbbbb'))
    print("weave('abcde','VWXYZ') return", weave('abcde','VWXYZ'))
    print("weave('aaaaaa','bb') return", weave('aaaaaa','bb'))
    print("index(5,[4,10,8,5,3,5]) return", index(5,[4,10,8,5,3,5]))
    print("index('b', 'banana') return", index('b', 'banana'))
    print("index('i','team') return", index('i', 'team'))
    


    # optional but encouraged: add test calls for your functions below