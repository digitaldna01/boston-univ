#
# lab8task3.py (Lab 8, Task 3)
#
# Images as 2-D lists
#
# Computer Science 111
# 

from hmcpng import *

def create_uniform_image(height, width, pixel):
    """ creates and returns a 2-D list of pixels with height rows and
        width columns in which all of the pixels have the RGB values
        given by pixel
        inputs: height and width are non-negative integers
                pixel is a list of RBG values of the form [R,G,B],
                     where each element is an integer between 0 and 255.
    """
    pixels = []
    
    for r in range(height):
        row = [pixel] * width
        pixels += [row]

    return pixels

def invert(pixels):
    """ takes the specified 2-D list of pixels (where each pixel is
        a list of the form [R,G,B]) and creates and returns a new 
        2-D list of pixels in which the colors of the pixels are
        inverted.
        input: pixels is a rectangular 2-D list of pixels
    """
    height = len(pixels)
    width = len(pixels[0])

    # Create a 2-D list that we'll use for the inverted image. 
    # We start with a uniform image filled with green pixels, 
    # but then we'll replace the green pixels with ones that 
    # represent the inverted colors.
    new_pixels = create_uniform_image(height, width, [0, 255, 0])
    
    for r in range(height):
        for c in range(width):
            # get the colors of the pixel at row r, column c
            pixel = pixels[r][c]
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            # Create a new pixel in which the colors of the
            # original pixel are inverted, and assign it to the 
            # appropriate location in new_pixels.
            new_pixels[r][c] = [255 - red, 255 - green, 255 - blue]

    return new_pixels

def rescue(pixels):
    """ takes the specified 2-D list of pixels (where each pixel is
        a list of the form [R,G,B]) and creates and returns a new 
        2-D list of pixels in which maroon pixels are replaced with 
        red ones and gold pixels are replaced with black ones,
        while pixels of other colors remain the same.
        input: pixels is a rectangular 2-D list of pixels
    """
    # rgb values for the relevant colors
    maroon = [140, 0, 30]
    gold = [195, 175, 100]
    red = [255, 0, 0]
    black = [0, 0, 0]


    h = len(pixels) 
    w = len(pixels[0])
    for r in range(h):
        for c in range(w):
            if pixels[r][c] == [140,0,30]:
                pixels[r][c] = [255,0,0]
            elif pixels[r][c] == [195,175,100]:
                pixels[r][c] = [0,0,0]
