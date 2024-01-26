#
# ps7pr5.py  (Problem Set 7, Problem 5)
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
                pixel is a 1-D list of RBG values of the form [R,G,B],
                     where each element is an integer between 0 and 255.
    """
    pixels = []

    for r in range(height):
        row = [pixel] * width
        pixels += [row]

    return pixels

def blank_image(height, width):
    """ creates and returns a 2-D list of pixels with height rows and
        width columns in which all of the pixels are green.
        inputs: height and width are non-negative integers
    """
    all_green = create_uniform_image(height, width, [0, 255, 0])
    return all_green

def brightness(pixel):
    """ takes a pixel (an [R, G, B] list) and returns a value
        between 0 and 255 that represents the brightness of that pixel.
    """
    red = pixel[0]
    green = pixel[1]
    blue = pixel[2]
    return (21*red + 72*green + 7*blue) // 100

## put your functions below
def grayscale(pixels):
    """ takes the 2-D list pixels containing pixels for an image, and that 
        creates and returns a new 2-D list of pixels for an image that is a 
        grayscale version of the original image.
        inputs: pixels is a 2-D list of RGB values of the form [R,G,B]
    """
    height = len(pixels)
    width = len(pixels[0])
    
    new_image = blank_image(height, width)
    
    for r in range(height):
        for c in range(width):
            b = brightness(pixels[r][c])
            new_image[r][c] = [b,b,b]
            
    return new_image

def fold_diag(pixels):
    """ takes the 2-D list pixels containing pixels for an image, and that 
        creates and returns a new 2-D list of pixels for an image in which the
        original image is 'folded' along its diagonal
        input: pixels is a 2-D list of RGB values of the form [R,G,B]
    """
    height = len(pixels)
    width = len(pixels[0])
    
    new_image = blank_image(height, width)
    
    for r in range(height):
        for c in range(width):
            new_image[r][c] = pixels[r][c]
            
    for r in range(height):
        for c in range(width):    
            if r > c:
                new_image[r][c] = [255,255,255]
    
    return new_image           

def mirror_horiz(pixels):
    """ takes 2-D list pixels containing pixels for an image, and that creates 
        and returns a new 2-D list of pixels for an image, and that creates and
        returns a new 2-D list of pixels for an image in which the original 
        image is 'mirrored' horizontally
        input: pixels is a 2-D list of RGB values of the form [R,G,B]
    """
    height = len(pixels)
    width = len(pixels[0])
    
    limit_point = width // 2
    
    new_image = blank_image(height, width)
    
    for r in range(height):
        for c in range(width):
            loc = width - 1 - c
            if c >= limit_point:
                new_image[r][c] = pixels[r][loc]
            else:
                new_image[r][c] = pixels[r][c]
    
    return new_image

def extract(pixels, rmin, rmax, cmin, cmax):
    """ takes the 2-D list pixels containing pixels for an image, and that 
        creates and returns a new 2-D list that represents the portion of the 
        original image that is specified by the other four parameters
        inputs: pixels is new_image[r][c] = pixels[r][c].
        rmin,rmx,cmin,cmax are postive integer
    """
    
    NH = rmax - rmin
    NW = cmax - cmin
    
    new_image = blank_image(NH,NW)
    
    for r in range(rmin, rmax):
        for c in range(cmin, cmax):
            extrar = r - rmin
            extrac = c - cmin
            new_image[extrar][extrac] = pixels[r][c]
            
    return new_image
    















  
        
            