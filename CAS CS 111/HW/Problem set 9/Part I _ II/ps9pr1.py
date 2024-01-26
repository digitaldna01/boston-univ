#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 16:38:13 2019

@author: leejaehong
"""


class Board:
    """ a data type for a Connect Four board with
        arbitrary dimensions
    """
    def __init__(self, height, width):
        """ constructs a new Board object by initializing the following three
            attributes
        """
        self.height = height
        self.width = width
        self.slots = [[' '] * width for row in range(height)]
        
    def __repr__(self):
        """ Returns a string representation for a Board object.
        """
        s = ''         # begin with an empty string

        # add one row of slots at a time
        for row in range(self.height):
            s += '|'   # one vertical bar at the start of the row

            for col in range(self.width):
                s += self.slots[row][col] + '|'

            s += '\n'  # newline at the end of the row

        num = self.width * 2 + 1
        s += '-' * num 
        s += '\n'
        k = 0
        for i in range(self.width):
            s += ' ' + str(k)
            k += 1
            if k == 10:
                k = 0
    # and the numbers underneath it.

        return s
    
    def add_checker(self, checker, col):
        """ accepts two inputs, put checker in desinated column
        """
        assert(checker == 'X' or checker == 'O')
        assert(0 <= col < self.width)
            
        row = 0
        
        for i in range(self.height):
            if self.slots[i][col] == ' ':
                k = i
            row = k 
            
        self.slots[row][col] = checker
        
    def reset(self):
        """ reset the Board object on which it is called by setting all slots
            to contain a space character
        """
        for i in range(self.height):
            for c in range(self.width):
                self.slots[i][c] = ' '
        
    def add_checkers(self, colnums):
        """ takes in a string of column numbers and places alternating
            checkers in those columns of the called Board object, 
            starting with 'X'.
        """
        checker = 'X'   # start by playing 'X'

        for col_str in colnums:
            col = int(col_str)
            if 0 <= col < self.width:
                self.add_checker(checker, col)

            # switch to the other checker
            if checker == 'X':
                checker = 'O'
            else:
                checker = 'X'
                
    def can_add_to(self, col):
        """ returns True if it is valid to place a checker in the column col on
            the calling Board object. Otherwise, it should return False.
        """
        if 0 <= col < self.width:
            if self.slots[0][col] == ' ':
                return True
        
        return False
    
    def is_full(self):
        """ returns True if the called Board object is completely full of 
            checkers, and returns False otherwise.
        """
        for h in range(self.height):
            for w in range(self.width):
                if self.slots[h][w] == ' ':
                    return False
                
        return True
        
    def remove_checker(self, col):
        """ removes the top checker from column col of the called Board object.
            if the column is empty, then the method should do nothing.
        """
        row = 0 
        k = 0
        for i in range(self.height):
            if self.slots[i][col] == 'X' or self.slots[i][col] == 'O':
                k = i
                break
        row = k 
            
        self.slots[row][col] = ' ' 
        
    def is_horizontal_win(self, checker):
        """ Checks for a horizontal win for the specified checker.
        """
        for row in range(self.height):
            for col in range(self.width - 3):
                # Check if the next four columns in this row
                # contain the specified checker.
                if self.slots[row][col] == checker and \
                   self.slots[row][col + 1] == checker and \
                   self.slots[row][col + 2] == checker and \
                   self.slots[row][col + 3] == checker:
                    return True

        # if we make it here, there were no horizontal wins
        return False
    
    def is_vertical_win(self, checker):
        """ Checks for a vertical win for the specified checker
        """
        for row in range(self.height - 3):
            for col in range(self.width):
                if self.slots[row][col] == checker and \
                   self.slots[row + 1][col] == checker and \
                   self.slots[row + 2][col] == checker and \
                   self.slots[row + 3][col] == checker:
                       return True
        
    def is_down_diagonal_win(self, checker):
        """ Checks for a diagonals that go dowm from left to right win for the 
            specified checker
        """
        for row in range(self.height - 3):
            for col in range(3, self.width):
                if self.slots[row][col] == checker and \
                   self.slots[row + 1][col - 1] == checker and \
                   self.slots[row + 2][col - 2] == checker and \
                   self.slots[row + 3][col - 3] == checker:
                       return True
                   
        
    def is_up_diagonal_win(self, checker):
        """ Checks for a diagonals that go up from left to right win for the 
            specified checker
        """
        for row in range(3, self.height):
            for col in range(self.width - 3):
                if self.slots[row][col] == checker and \
                   self.slots[row - 1][col + 1] == checker and \
                   self.slots[row - 2][col + 2] == checker and \
                   self.slots[row - 3][col + 3] == checker:
                       return True
                
        
    def is_win_for(self, checker):
        """ accepts a parameter checker that is either 'X' or 'O', and returns
            True if there are four consectuve slots containing checker on the 
            board. Otherwise, it should return False
        """
        assert(checker =='X' or checker == 'O')
        
        if self.is_horizontal_win(checker) == True or \
           self.is_vertical_win(checker) == True or \
           self.is_down_diagonal_win(checker) == True or \
           self.is_up_diagonal_win(checker) == True:
               return True 
           
        return False
        
            

def test():
    b = Board(6, 7)
    print(b)