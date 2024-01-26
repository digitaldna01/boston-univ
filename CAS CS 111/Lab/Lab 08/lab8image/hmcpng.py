import png
import os

def save_pixels( boxed_pixels, filename="out.png" ):
    """ need docstrings! """
    #print('Starting to save', filename, '...')
    f = open(filename, 'wb')      # binary mode is important
    W, H = getWH( boxed_pixels )
    w = png.Writer( W, H )
    #print "boxed_pixels are", boxed_pixels
    pixels = unbox( boxed_pixels )
    #print "pixels are", pixels
    w.write(f, pixels)
    f.flush()
    os.fsync(f.fileno())
    f.close()
    print(filename, "saved.")

def unbox( boxed_pixels ):
    """ assumes the pixels came from box
        and unboxes them!
    """
    flat_pixels = []
    for boxed_row in boxed_pixels:
        flat_row = []
        for pixel in boxed_row:
            flat_row.extend( pixel )
        flat_pixels.append( flat_row )
    return flat_pixels

def box( L ):
    """ boxes the flat pixels in row L
        assumes three channels!
    """
    newL = []
    STRIDE = 4  # since we're using RGBA!
    for i in range(len(L) // STRIDE):
        newL.append( L[STRIDE*i:STRIDE*i+3] ) # since we're providing RGB
    return newL


def load_pixels( filename="in.png" ):
    """ need docstrings! """
    #print("Opening the", filename, " file (each dot is a row)", end=' ')
    reader = png.Reader(filename)
    #data = reader.read()
    data = reader.asRGBA()
    width = data[0]
    height = data[1]
    pixels = data[2]  # this is an iterator...
    PIXEL_LIST = []
    while True:
        try:
            a = next(pixels)
            #print(".", end=' ')
            PIXEL_LIST.append( box( a.tolist() ) )
        except StopIteration:
            #print("\nFile read.")
            break

    return PIXEL_LIST

def getWH( PX ):
    """ need docstrings! """
    H = len(PX)
    W = len(PX[0])
    return W, H

def binaryIm( s, cols, rows ):
    """ need docstrings! """
    PX = []
    for row in range(rows):
        ROW = []
        for col in range(cols):
            c = int(s[row*cols + col])*255
            px = [ c, c, c ]
            ROW.append( px )
        PX.append( ROW )
    save_pixels( PX, 'binary.png' )
    #return PX
