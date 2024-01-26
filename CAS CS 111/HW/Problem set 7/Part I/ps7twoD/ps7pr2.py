#
# ps7pr2.py (Problem Set 7, Problem 2)
#
# 2-D Lists
#
# Computer Science 111
#
# If you worked with a partner, put his or her contact info below:
# partner's name:
# partner's email:
# 

# IMPORTANT: This file is for your solutions to Problem 2.
# Your solutions to problem 3 should go in ps7pr3.py instead.

import random

def create_grid(height, width):
    """ creates and returns a 2-D list of 0s with the specified dimensions.
        inputs: height and width are non-negative integers
    """
    grid = []
    
    for r in range(height):
        row = [0] * width     # a row containing width 0s
        grid += [row]

    return grid

def print_grid(grid):
    """ prints the 2-D list specified by grid in 2-D form,
        with each row on its own line, and nothing between values.
        input: grid is a 2-D list. We assume that all of the cell
               values are integers between 0 and 9.
    """
    height = len(grid)
    width = len(grid[0])
    
    for r in range(height):
        for c in range(width):
            print(grid[r][c], end='')   # print nothing between values
        print()                         # at end of row, go to next line

def diagonal_grid(height, width):
    """ creates and returns a height x width grid in which the cells
        on the diagonal are set to 1, and all other cells are 0.
        inputs: height and width are non-negative integers
    """
    grid = create_grid(height, width)   # initially all 0s

    for r in range(height):
        for c in range(width):
            if r == c:
                grid[r][c] = 1

    return grid

def inner_grid(height, width):
    """ creates and returns a 2-D list of height rows and with columns in whole
        the "inner" cells are all 1 and the cells on the outer border are all 0
        inputs: height and width are non-negative integers
    """
    grid = create_grid(height, width)
    
    for r in range(1,height-1):
        for c in range(1,width-1):
            grid[r][c] = 1
            
    return grid
            
def random_grid(height, width):
    """ creates and returns a 2 - D list of height rows and width columns in
        which the inner cells are randomly assigned either 0 or 1, but the
        cells on the outer border are all 0
        inputs: height and width are non-negative integers
    """
    grid = create_grid(height, width)
    
    for r in range(1, height -1 ):
        for c in range(1, width -1):
            grid[r][c] = random.choice([0,1])
            
    return grid
            
def copy(grid):
    """ creates and returns a deep copy of grid-a new, seperate 2-D list that 
        has the same dimensions and cell values as grid.
        input: grid that made with 0 and 1
    """
    new_grid = create_grid(len(grid), len(grid[0]))
    
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            new_grid[r][c] = grid[r][c]
            
    return new_grid
            
def invert(grid):
    """ takes an existing 2-D list of 0s and 1s and iverts it - changing all 0
        values to 1, and changing all 1 values to 0 
        input: grid that made with 0 and 1
    """
    height = len(grid)
    width = len(grid[0])
    
    for r in range(height):
        for c in range(width):
            if grid[r][c] == 1:
                grid[r][c] = 0
            else:
                grid[r][c] = 1
    
            
            
            