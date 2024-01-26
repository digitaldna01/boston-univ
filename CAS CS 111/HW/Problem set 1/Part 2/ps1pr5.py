#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 13:22:07 2019

@author: leejaehong
"""

# function 1
def first_and_last(values):
    """ returns a new list containing the first value of the original list
        followed by the last value of the original list.
        input: any list
    """
    first = values[0]
    last = values[-1]
    return [first, last]

# function 2
def longer_len(s1, s2):
    """ returns the length of the longer strings from two string inputs
        inputs: any string
    """
    
    if s1 == '':
        return 0 
    else:
        s1_rest = longer_len(s1[1:],0)
        return 1 + s1_rest
    if s2 == '':
        return 0 
    else:
        s2_rest = longer_len(0,s2[1:])
        return 1 + s2_rest
    
    if s1_rest > s2_rest:
        return s1_rest
    else:
        return s2_rest

# function 3
def move_to_end(s, n):
    """ returns the a new string in which the first n characters of s have 
        been moved to the end of the string
        input s: string, n: integer
    """
    if len(s) < n:
        return s
    else:
        return s[n:] + s[0:n] 


def test():
    """ performs test calls on the functions above """
    # function 1 test
    print('first_and_last([1,2,3,4]) return', first_and_last([1,2,3,4]))
    print('first_and_last([7]) return', first_and_last([7]))
    print('first_and_last(["how","are","you?"]) return', first_and_last(['how','are','you?']))
    #function 2 test
    print('longer_len("computer", "compute") return', longer_len('computer', 'compute'))
    print('longer_len("hi", "hello") return', longer_len('hi', 'hello'))
    print('longer_len("begin", "on") return', longer_len('begin', 'on'))
    # function 3 test
    print('move_to_end("computer", 3) return', move_to_end('computer',3))
    print('move_to_end("computer", 5) return', move_to_end('computer',5))
    print('move_to_end("computer", 0) return', move_to_end('computer',0))