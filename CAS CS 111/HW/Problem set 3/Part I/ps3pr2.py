#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 17:34:47 2019

@author: leejaehong
"""

# 
# ps3pr2.py - Problem Set 3, Problem 2
#
# Algorithm design 
#

# function 1 
def cube_all_lc(values):
    """ return a list containing the cubes of the numbers in values
        input values: a list of numbers
    """
    return [x ** 3 for x in values]

# function 2
def cube_all_rec(values):
    """ return a list containing the cubes of the numbers in values
        input values: a list of numbers
    """
    if values == []:
        return []
    else:
        values_rest = cube_all_rec(values[1:])
        return [values[0] ** 3] + values_rest  
# function 3
def num_larger(threshold,values):
    """ returns the number of elements of values that are larger than threshold
        input threshold: a number, values: a list of numbers
    """
    if values == []:
        return 0
    else: 
        values_rest = num_larger(threshold, values[1:])
        if threshold < values[0]:
            return 1 + values_rest
        else:
            return values_rest
        
# function 4
# helper function 
def num_vowels(s):
    """ returns the number of vowels in the string s
        input: s is a string of 0 or more lowercase letters
    """
    if s == '':
        return 0
    else:
        num_in_rest = num_vowels(s[1:])
        if s[0] in 'aeiou':
            return 0 + num_in_rest
        else:
            return 1 + num_in_rest

def most_consonants(words):
    """ returns the string in the list with the most consonants
        input words: a list of string
    """
    vowels = [[num_vowels(x),x] for x in words]
    bestpairs = max(vowels)
    return bestpairs[1]

# function 5 
def price_string(cents):
    """ returns a string in which the price is expressed as a combination of 
        dollars and cents
        input cents: a postive integer
    """
    d = cents // 100
    c = cents % 100 
    price = ''
    if d == 1:
        if c == 1:
            price = '1 dollar, 1 cent'
        elif c == 0:
            price = '1 dollar '
        else: 
            price = '1 dollar, ' + str(c) + ' cents'
    elif d == 0:
        if c == 1:
            price = '1 cent'
        elif c == 0:
            price = ''
        else:
            price = str(c) + ' cents'
    else:
        if c == 1:
            price = str(d) + ' dollars, 1 cent'
        elif c == 0:
            price = str(d) + ' dollars '
        else:
test            price = str(d) + ' dollars, ' + str(c) + ' cents'
    return price
        
# test function with a sample test call for function 0
def test():
    """ performs test calls on the functions above """
    # function 1 test
    print('cube_all_lc([-2,5,4,-3]) return', cube_all_lc([-2,5,4,-3]))
    # function 2 test
    print('cube_all_rec([-2,5,4,-3]) return', cube_all_rec([-2,5,4,-3]))
    print('cube_all_rec([1,2,3]) return', cube_all_rec([1,2,3]))
    # function 3 test
    print('num_larger(5,[1,7,3,5,10]) return', num_larger(5,[1,7,3,5,10]))
    print('num_larger(2, [1,7,3,5,10]) return', num_larger(2,[1,7,3,5,10]))
    print('num_larger(10,[1,7,3,5,10]) return', num_larger(10,[1,7,3,5,10]))
    # function 4
    print('most_consonants(["python","is","such","fun"]) return',most_consonants(['python','is','such','fun']))
    print('most_consonants(["oooooooh","i","see","now"]) return',most_consonants(['oooooooh','i','see','now']))
    # function 5
    print('price_string(452) return', price_string(452))
    print('price_string(871) return', price_string(871))
    print('price_string(27) return', price_string(27))
    print('price_string(300) return', price_string(300))
    print('price_string(201) return', price_string(201))
    print('price_string(117) return', price_string(117))
    print('price_string(101) return', price_string(101))
    # optional but encouraged: add test calls for your functions below