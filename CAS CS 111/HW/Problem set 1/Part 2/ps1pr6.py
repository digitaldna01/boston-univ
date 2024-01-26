#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:10:46 2019

@author: leejaehong
"""
# function 1 
def mirror(s):
    """ return a mirrored version of s that is twice the length of the
        original string
        input s: any string
    """
    return s + s[::-1]

# function 2 
def is_mirror(s):
    """ returns True if s is a mirrored string and false otherwies
        input s: any string
    """
    a = len(s) // 2
    b = s[:a]
    c = s[a:]
    if b == c[::-1]:
        return True
    else:
        return False

# function 3 test
def replace_end(values, new_end_vals):
    """ returns a new list in which the elements in new_end_vals have replaced
        the last n elements of the list values, where n is the length of 
        new_end_vals
        input values, new_end_vals : list
    """
    a = len(values); b = len(new_end_vals)
    if a <= b:
        return new_end_vals
    else:
        return values[:a-b] + new_end_vals

# function 4 test
def repeat_elem(values, index, num_times):
    """ returns a new list in which the element of values at position index
        has been repeated num_times
        input values: list, index: int, new_times: int
    """
    
    return values[0:index] + values[index:index+1] * num_times + values[index+1:]



def test():
    """ performs test calls on the functions above """
    # function 1 test
    print('mirror("bacon") return', mirror('bacon'))
    print('mirror("XYZ") return', mirror('XYZ'))
    # function 2 test
    print('is_mirror("baconnocab") return', is_mirror('baconnocab'))
    print('is_mirror("baconnoca") return', is_mirror('baconnoca'))
    # function 3 test
    print('replace_end([1,2,3,4,5], [7,8,9]) return', replace_end([1,2,3,4,5], [7,8,9]))
    print('replace_end([1,2,3,4,5], [10,11]) return', replace_end([1,2,3,4,5], [10,11]))
    print('replace_end([1,2,3,4,5], [12]) return', replace_end([1,2,3,4,5], [12]))
    print('replace_end([0,2,4,6], [4,3,2,1]) return', replace_end([0,2,4,6], [4,3,2,1]))
    print('replace_end([0,2,4,6], [4,3,2,1,0]) return', replace_end([0,2,4,6], [4,3,2,1,0]))
    # function 4 test
    print('repeat_elem([10,11,12,13],2,4) return',repeat_elem([10,11,12,13],2,4))
    print('repeat_elem([10,11,12,13],2,6) return',repeat_elem([10,11,12,13],2,6))
    print('repeat_elem([5,6,7],1,3) return',repeat_elem([5,6,7],1,3))
    
    
    
    
    
    
    
    
    
    
    
    