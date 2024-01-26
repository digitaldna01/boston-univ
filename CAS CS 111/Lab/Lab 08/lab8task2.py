#
# lab8task2.py (Lab 8, Task 2)
#
# 2-D Lists
#
# Computer Science 111
#

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
        with each row on its own line, and one space between values.
        input: grid is a 2-D list. We assume that all of the cell
               values are integers between 0 and 9.
    """
    height = len(grid)
    width = len(grid[0])
    
    for r in range(height):
        for c in range(width):
            print(grid[r][c], end=' ')  # print a space instead of a newline
        print()                         # at end of row, go to next line

def mod_grid(grid, n):
    """ takes a 2-D list of integers (grid) and an integer n, and
        replaces each value in the list with the result of
        computing the modulus of that value with n.
        inputs: grid is a 2-D list of integers between 0 and 9.
                n is a positive integer.
    """
    height = len(grid)
    width = len(grid[0])
    
    for r in range(height):
        for c in range(width):
            val = grid[r][c]
            grid[r][c] = val % n
            
    # no return value needed, because we're modifying the internals
    # of the original 2-D list
