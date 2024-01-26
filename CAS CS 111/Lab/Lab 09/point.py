#
# point.py
#
# The beginnings of a class for Point objects
#
# CS 111
#

import math

class Point:
    """ A class for objects that represent points in
        the Cartesian plane.
    """
    
    def __init__(self, init_x, init_y):
        """ constructor for a Point object that represents a point
            with coordinates (init_x, init_y)
        """
        self.x = init_x
        self.y = init_y

    def distance_from_origin(self):
        """ computes and returns the distance of the called Point object
            (self) from the origin (i.e., from (0, 0))
        """
        dist = math.sqrt(self.x**2 + self.y**2)
        return dist

    def move_down(self, amount):
        """ moves the called Point object (self) in a downwards
            direction by the specified amount
        """
        self.y -= amount

    def __repr__(self):
        """ returns a string representation for the called Point
        object (self)
        """
        s = '(' + str(self.x) + ', ' + str(self.y) + ')'
        return s