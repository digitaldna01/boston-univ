#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 21:47:31 2019

@author: leejaehong
"""
import random
#ps8pr3.py

def create_dictionary(filename):
    """ takes a string representing the name of a text file, and that returns
        a dictionary of key - value pairs in which: each key is a word 
        encountered in the text file & the corresponding value is a list of 
        words that follow the key word in the text file.
    """
    d = {}
    file = open(filename, 'r')
    document = file.read()
    words = document.split()
    current_word = '$'
    for next_word in words:
        if current_word not in d:
            d[current_word] = [next_word]
        else:
            d[current_word] += [next_word]
        if next_word[-1] in '?!.':
            current_word = '$'
        else:
            current_word = next_word
    return d
            

def generate_text(word_dict, num_words):
    """ takes as parameters a dictionary of word transitions named word_dict 
        and a positive integer named num_words.
    """
    current_word = '$'
    for i in range(num_words):
        next_word = random.choice(word_dict[current_word])
        print(next_word, end = ' ')
        if next_word[-1] in '?!.':
            current_word = '$'
        elif next_word not in word_dict:
            current_word = '$'
        else:
            current_word = next_word
        
            