#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 20:49:09 2019

@author: leejaehong
"""

#
# ps2pr7.py - Problem Set 2, Problem 7
#
# Fun with recursion, part II

# function 1
def letter_score(letter):
    """ returns the calue of that letter as a scrabble title. if letter is not
        a lowercase letter from 'a' to 'z', the function should return 0
        input letter: lowercase letter
    """
    assert(len(letter) == 1)
    if letter in ['a','e','i','l','n','o','s','r','t','u']:
        return 1
    elif letter in ['d','g']:
        return 2
    elif letter in ['b','c','m','p']:
        return 3
    elif letter in ['f','h','v','w','y']:
        return 4
    elif letter in ['k']:
        return 5
    elif letter in ['j','x']:
        return 8
    elif letter in ['q','z']:
        return 10
    else:
        return 0
    
# function 2
def scrabble_score(word):
    """ returns the scrabble score of that string
        input word: string
    """
    if word == '':
        return 0
    else:
        scrabble_rest = scrabble_score(word[1:])
        return letter_score(word[0]) + scrabble_rest

# function 3
def add(vals1, vals2):
    """ return a new list in which each element is the sum of the corresponding
        element of vals1 and vals2
        input vals1, vals2: list of numbers
    """
    if len(vals1) == 0:
        return []
    else:
        add_rest = add(vals1[1:],vals2[1:])
        return [vals1[0] + vals2[0]] + add_rest




# function 4
def weave(s1,s2):
    """ return a new string that is formed by 'weaving' together the characters
        in the strings s1 and s2 to create a single string
        input: s1, s2: string
    """
    if s1 == []:
        return s1
    elif s2 == []:
        return s2
    else:
        weave_rest_s1 = weave(s1[1:],s2[1:])
        return s1[0] + s2[0] + weave_rest_s1
         
def test():
    """ performs test calls on the functions above """
    # function 1 test
    print('letter_score("w") return', letter_score('w'))
    print('letter_score("q") return', letter_score('q'))
    print('letter_score("%") return', letter_score('%'))
    print('letter_score("A") return', letter_score('A'))
    # function 2 test
    print('scrabble_score("python") return', scrabble_score('python'))
    print('scrabble_score("a") return', scrabble_score('a'))
    print('scrabble_score("quetzal") return', scrabble_score('quetzal'))
    # function 3 test
    print('add([1,2,3],[3,5,8]) return', add([1,2,3], [3,5,8]))
    print('add([2,3,4,5],[-3,-2,-1,0]) return', add([2,3,4,5], [-3,-2,-1,0]))
    print('add([],[]) return', add([], []))
    # function 4 test
    print('weave("aaaaaa","bbbbbb") return', weave('aaaaaa','bbbbbb'))
    print('weave("abcde","VWXYZ") return', weave('abcde','VWXYZ'))
    print('weave("aaaaaa","bb") return', weave('aaaaaa','bb'))
    print('weave("aaaa","bbbbbb") return', weave('aaaa','bbbbbb'))
    print('weave("aaaa","") return', weave('aaaa',''))
    print('weave("","bbbb") return', weave('','bbbb'))
    print('weave("","") return', weave('',''))
    
    
    
    
