# 
# ps1pr3.py - Problem Set 1, Problem 3
#
# Functions with numeric inputs
#
# If you worked with a partner, put their contact info below:
# partner's name:
# partner's email:
#

# function 0
def opposite(x):
    """ returns the opposite of its input
        input x: any number (int or float)
    """
    return -1*x

# put your definitions for the remaining functions below

# function 1
def cube(x):
    """ returns the cube of its input
        input x: any number (int or float)
    """
    return x ** 3
        
# funtion 2
def convert_to_inches(yards, feet):
    """ returns the corresponding length in inches
        input yards,feet: any number (int or float)
    """
    if yards >= 0 :
        yards_to_inches = yards * 36
    else:
        yards_to_inches = 0
    if feet >= 0:
        feet_to_inches = feet * 12
    else:
        feet_to_inches = 0
    return yards_to_inches + feet_to_inches 

# function 3
def area_sq_inches(height_yds, height_ft, width_yds, width_ft):
    """ returns the area of the rectangle in square inches
        input height_yds, height_ft, width_yds, width_ft: any number(int or float)
    """
    height_to_inches = convert_to_inches(height_yds, height_ft)
    width_to_inches = convert_to_inches(width_yds, width_ft)
    
    area = height_to_inches * width_to_inches
    return area

# function 4
def median(a, b, c):
    """ returns the median of the three inputs
        input a, b, c: any number (int or float)
    """
    if a >= c and a >= b:
        if b >= c:
            return b
        else: 
            return c
    elif b >= a and b >= c:
        if a >= c:
            return a
        else: 
            return c
    elif c >= a and c >= b:
        if a >= b:
            return a
        else: 
            return b
        

# test function with a sample test call for function 0
def test():
    """ performs test calls on the functions above """
    print('opposite(-8) returns', opposite(-8))

    # optional but encouraged: add test calls for your functions below
    print('cube(2) returns', cube(2))
    print('convert_to_inches(4, 2) returns', convert_to_inches(4, 2))
    print('convert_to_inches(-4,2) returns', convert_to_inches(-4, 2))
    print('area_sq_inches(1, 2, 3, 1) returns', area_sq_inches(1, 2, 3, 1) )
    print('median(10,2,7) returns', median(10,2,7))
    print('median(7,2,10) returns', median(7, 2, 10))
    print('median(8, 6, 4) returns', median(8, 6, 4))
    print('median(10,2,2) returns', median(10, 2, 2))
    
    
    
    
    