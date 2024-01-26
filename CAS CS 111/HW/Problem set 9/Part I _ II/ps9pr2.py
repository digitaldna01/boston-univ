#
# ps9pr2.py  (Problem Set 9, Problem 2)
#
# A Connect-Four Player class 
#  

from ps9pr1 import Board

# write your class below

class Player:
    """ represent a player of the Connect Four game.
    """
    def __init__(self, checker):
        """ construct a new Player object by initializing the following two 
            attributes:
                an attribute checker - a one-character string that represents
                the gamepiece for the player, as specified by the parameter 
                checker.
                an attribute num_moves- an integer that stores how many moves 
                the player has made so far. This attributes should bnt 
                initialized to zero to signify that the Player object has not
                yet made any Connect Four moves.
        """
        assert(checker == 'X' or checker == 'O')
        self.checker = checker
        self.num_moves = 0
        
        
    def __repr__(self):
        """ returns a string representing a Player object. The string returned
            should indicate which checker the Player object is using. 
        """
        s = 'Player ' + self.checker
        return s
    
    def opponent_checker(self):
        """ returns a one-character string representing the checker of the 
            Player object's opponent. The method may assume that the calling 
            Player object has a checker attribute that is either 'X' or 'O'
        """
        if self.checker == 'X':
            return 'O'
        
        return 'X'
    
    def next_move(self, b):
        """ accepts a Board object b as a parameter and returns the column 
            where the player wants to make the next move.
        """

        self.num_moves += 1
        while True:
            n = int(input('Enter a column: '))
            self.sel_col_num = n
            if b.can_add_to(self.sel_col_num) == True:
                return self.sel_col_num
            else:
                print('Try again!')
            
            
        
        
        
    
        
            