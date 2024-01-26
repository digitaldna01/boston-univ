#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 00:16:18 2019

@author: leejaehong
"""

#
# ps2pr3.py - Problem Set 2, Problem 3
#
# More practice writing non-recursive functions

#function 1
def flipside(s):
    """ returns a string whose first half is s'second half and whose second 
        half is s's first half
        input s: a string
    """
    if len(s) / 2 == 0:
        a = len(s) / 2 
        return s[a:] + s[:a]
    else:
        a = len(s) // 2
        return s[a:] + s[:a]

# function 2
def adjust(s, length):
    """ returns s atring in which the value od s has been adjusted as necessary
        to produce a string with the specified length
        input s: string length: int
    """
    if len(s) >= length:
        return s[:length]
    else:
        a = length - len(s)
        return a * ' ' + s
        

def test():
    """ performs test calls on the functions above """
    # function 1 test
    print('flipside("homework") return', flipside('homework'))
    print('flipside("carpets") return', flipside('carpets'))
    # function 2 test
    print('adjust("alien",6) return', adjust('alien',6))
    print('adjust("compute", 10) return', adjust('compute',10))
    print('adjust("alien", 4) return', adjust('alien', 4))
    print('adjust("compute", 7) return', adjust('compute',7))