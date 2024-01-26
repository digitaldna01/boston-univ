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

def process_diffs(diffs, filename1, filename2):
    print(filename1, 'and', filename2, 'differ in', len(diffs), 'positions.')

    f1_comps = filename1.split('.')
    f2_comps = filename2.split('.')
    
    diffs_filename = f1_comps[0] + '-' + f2_comps[0] + '.txt'
    f = open(diffs_filename, 'w')
    for x in diffs:
        print(x, file=f)
    f.close()

    print('The positions with differences can be found in', diffs_filename)

def compare_images(filename1, filename2):
    pixels1 = load_pixels(filename1)
    pixels2 = load_pixels(filename2)

    h1 = len(pixels1)
    h2 = len(pixels2)
    w1 = len(pixels1[0])
    w2 = len(pixels2[0])

    if h1 != h2 or w1 != w2:
        print('The images do not have the same dimensions:')
        print(filename1 + ':', h1, 'rows,', w1, 'columns')
        print(filename2 + ':', h2, 'rows,', w2, 'columns')
    else:
        diffs = []
        for r in range(h1):
            for c in range(w1):
                if pixels1[r][c] != pixels2[r][c]:
                    diffs += [[r, c]]
 
        if diffs == []:
            print(filename1, 'and', filename2, 'are identical.')
        else:
            process_diffs(diffs, filename1, filename2)

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
