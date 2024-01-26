#
# ps7pr3.py  (Problem Set 7, Problem 3)
#
# Conway's Game of Life
#
# Computer Science 111  
#

# IMPORTANT: this file is for your solutions to Problem 3.
# Your solutions to Problem 2 should go in ps7pr2.py instead.

from ps7pr2 import *
from gol_graphics import *
import random

def count_neighbors(cellr, cellc, grid):
    """ returns the number of alive neighbors of the cell at position [cellr]
        [cellc] in the specified grid
        inputs: cellr, cellc are non-negative numbers, grid: grid made out of 
        0s and 1s
    """
    count = 0
    
    for r in range(cellr - 1, cellr + 2):
        for c in range(cellc - 1, cellc + 2):
            if r == cellr and c == cellc:
                continue
            else:
                if grid[r][c] == 1:
                    count += 1
    return count

def next_gen(grid):
    """ takes a 2-D list called grid that represents the current generation of
        cells, and that uses the rules of the Game of Life to create and 
        return a new 2-D list representing the next generation of cells
        inputs: grid made with 0s and 1s
    """
    new_grid = copy(grid)
    
    height = len(grid)
    width = len(grid[0])
    
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            num_neighbors = count_neighbors(r, c, grid)
            new_grid[r][c] = grid[r][c]
            if num_neighbors < 2:
                new_grid[r][c] = 0
            if num_neighbors > 3:
                new_grid[r][c] = 0
            if num_neighbors == 3:
                new_grid[r][c] = 1
                
    return new_grid