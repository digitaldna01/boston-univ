#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 19:45:50 2019

@author: leejaehong
"""

# 
# ps4pr3.py - Problem Set 4, Problem 3
#
# Recursive operations on binary numbers
#

# function 1 
def bitwise_and(a, b):
    """ each pair of corresponding bits is ANDed together to produce the 
        appropriate bit for the result
        input a, b: two binary numbers
    """
    if a == '' :
        return '0' * len(b) 
    elif b == '':
        return '0' * len(a)
    else:
        rest = bitwise_and(a[0:-1], b[0:-1])
        if int(a[-1] + b[-1]) == 11:
            return rest + '1'
        else:
            return rest + '0'

# function 2
def add_bitwise(b1,b2):
    """ adds two binary numbers
        input b1,b2: two binary numbers
    """
    if b1 == '':
        return b2
    elif b2 == '':
        return b1
    else:
        sum_rest = add_bitwise(b1[:-1],b2[:-1])
        if b1[-1] == '0' and b2[-1] == '0':
            return sum_rest + '0'
        elif int(b1[-1]) + int(b2[-1]) == 1:
            return sum_rest + '1'
        else: 
            return add_bitwise(sum_rest,'1') + '0'
    
def test():
    #test the function
    # function 1 
    print('bitwise_and("11010", "10011") return', bitwise_and('11010','10011'))
    print('bitwise_and("1001111", "11011") return', bitwise_and('1001111','11011'))
    print('bitwise_and("101", "") return', bitwise_and('101',''))
    print('bitwise_and("", "11010") return', bitwise_and('','11010'))
    # function 2
    print('add_bitwise("11","100") return', add_bitwise('11','100'))
    print('add_bitwise("11","1") return', add_bitwise('11','1'))
    print('add_bitwise("","101") return', add_bitwise('','101'))
    print('add_bitwise("11100","11110") return', add_bitwise('11100','11110'))