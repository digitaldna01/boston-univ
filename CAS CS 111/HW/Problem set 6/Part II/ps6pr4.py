#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 16:06:30 2019

@author: leejaehong
"""

#
# ps6pr4.py - problem set 6, problem 4
#
# Choosing the correct type of loop
#

# Problem 1
# Function 1
def log(b, n):
    """ uses a loop to compute and return the logarithm to the base b of a 
        number n - or, in cases in which n is not an integral power of b, an 
        integer estimate of the log
        input b, n : int
    """
    R = 0
    remainder = 0
    while n > 1:
       remainder = n // b
       print('dividing',n,'by',b,'gives',remainder)
       n = remainder
       R += 1
    return R 

# Function 2    
def add_powers(m,n):
    """ takes a positive integer m and an arbitrary integer n, and that uses a
        loop to add together the first m powers of n
        input m: positive integer, n: arbitrary integer
    """
    s = 0
    for i in range(m):
        r = n ** i
        print(n,'**',i,'=',r)
        s = s + r
    return s

# Fnction 3
def square_evens(values):
    """ takes a list of integers called values, and that modifies the list so
        that all of its eveb elements are replaced with their squeares, but all
        of its odd elements are left unchanged
        input values: list of integers
    """
    for i in range(len(values)):
        if values[i] % 2 == 0:
            values[i] = values[i] ** 2   
        else:
            values[i] = values[i]

# test function with a sample test call for function 0
def test():
    """ performs test calls on the functions above """
    print('log(5,125) return', log(5,125))
    print('log(5,1) return', log(5,1))
    print('log(5,3) return', log(5,3))
    print('log(2,20) return', log(2,20))
    print('add_powers(4,2) return',add_powers(4,2))
    print('add_powers(6,2) return',add_powers(6,3))
    print('add_powers(3,-6) return',add_powers(3,-6))
    

    # optional but encouraged: add test calls for your functions below