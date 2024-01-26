#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:42:05 2019

@author: leejaehong
"""

# 
# ps4pr2.py - Problem Set 4, Problem 2
#
# Using your cinversion functions
#
from ps4pr1 import *
def dec_to_bin(n):
    """ takes a non-negative integer n and uses recursion to convert it from 
        decimal to binary-constructing and returning a string version of the 
        binary representation of that number.
        input n: non-negative integer
    """
    if n == 0:
        a = ''
    elif n == 1:
        a =  '1'   
    else:
       rest_n = dec_to_bin(n//2)
       if n % 2 == 1:
           a = rest_n + '1'
       elif n % 2 == 0:
           a = rest_n + '0'
    if a == '':
        return '0'
    else: 
        return a
    
# function 2 
def bin_to_dec(b):
    """ takes a string b that represents a binary number and uses recursion to 
        convery the number from binary to decimal returning the resulting 
        integer.
        input b: a sting
    """
    if b =='':
        return 0
    else:
        rest = bin_to_dec(b[:-1])
        if b[-1] == '1':
            return 2 * rest + 1
        elif b[-1] == '0':
            return 2 * rest + 0

# function 1
def add(b1,b2):
    """ takes as inputs two strings b1 and b2 that represent binary numbers.
        input b1, b2: binary numbers
    """
    n1 = bin_to_dec(b1)
    n2 = bin_to_dec(b2)
    b_sum = dec_to_bin(n1+n2)
    return b_sum

# function 2
def increment(b):
    """ takes an 8-character string representation of a binary number and 
        returns the next larger binary number as an 8 - character string
        input b: 8 - character string
    """
    n1 = bin_to_dec(b)
    b1 = dec_to_bin(n1 + 1)
    zero = '0' * (8 - len(b1))
    ans = zero + b1
    return ans


"""
# function test
def test():
    #funtion 1
    print("add('11','1') return", add('11','1'))
    print("add('11100','11110') return", add('11100','11110'))
    # function 2
    print('increment("00000000") return', increment('00000000'))
    print('increment("00000111") return', increment('00000111'))
    print('increment("11111111") return', increment('11111111'))
"""
    