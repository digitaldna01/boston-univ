#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 17:08:16 2019

@author: leejaehong
"""

#
# ps2pr4.py - Problem Set 2, Problem 4
#
# Fun with recursion, part I

# function 1
def copy(s, n):
    """ return a string in which n copies of s have been concatenated together
        input s: string n: int
    """
    if n <= 0:
        return ''
    else:
        n_rest = copy(s, n-1)
        return s + n_rest
    
# function 2 
def compare(list1, list2):
    """ return the number of values in list 1 that are smaller than their 
        corresponding value in list 2     
        input list1, list2: list
    """
    if len(list1) == 0 or len(list2) == 0:
        return 0
    else:
        list1_rest = compare(list1[1:], list2[1:])
        if list1[0] < list2[0]:
            return 1 + list1_rest
        else:
            return 0 + list1_rest
        
        

# function 3 
def double(s):
    """ return the string formed by doubling each character in the string.
        input s: string
    """
    if s == '':
        return ''
    else:
        s_rest = double(s[1:])
        return s[0]*2 + s_rest 
                 
def test():
    """ performs test calls on the functions above """
    # function 1 test
    print('copy("da",2) return', copy('da',2))
    print('copy("Go BU!",4) return', copy('Go BU!',4))
    print('copy("hello",1) return', copy('hello',1))
    print('copy("hello",0) return', copy('hello',0))
    print('copy("hello",-7) return', copy('hello',-7))
    # function 2 test
    print('compare([5,3,7,9,1], [2,4,7,8,3]) return', compare([5,3,7,9,1],[2,4,7,8,3]))
    print('compare([4,2,3,7], [1,5]) return', compare([4,2,3,7],[1,5]))
    print('compare([4,2,3], [6,5,0,8]) return', compare([4,2,3],[6,5,0,8]))
    print('compare([5,3], []) return', compare([5,3],[]))
    print('compare([], [5,3,7]) return', compare([],[5,3,7]))
    # function 3 test
    print('double("hello") return',double('hello'))
    print('double("python") return',double('python'))
    print('double("") return',double(''))
    
    
    
    
    
    
    
    