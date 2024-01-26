#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 11:22:52 2019

@author: leejaehong
"""

# 
# ps4pr1.py - Problem Set 4, Problem 1
#
# From binary to decimal and back!
#
# function 1 
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
"""   
def test():
    test the function
    # function 1 
    print('dec_to_bin(5) return', dec_to_bin(5))
    print('dec_to_bin(12) return', dec_to_bin(12))
    print('dec_to_bin(0) return', dec_to_bin(0))
    # function 2 test
    print('bin_to_dec("101") return', bin_to_dec('101'))
    print('bin_to_dec("1100") return', bin_to_dec('1100'))
    print('bin_to_dec("0") return', bin_to_dec('0'))
"""