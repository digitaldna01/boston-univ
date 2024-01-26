#
# ps9pr4.py  (Problem Set 9, Problem 4)
#
# AI Player for use in Connect Four   
#

import random  
from ps9pr3 import *

class AIPlayer(Player):
    """ takes the approach outlined (below) to choose its next move.
    """
    def __init__(self, checker, tiebreak,lookahead):
        """ construct a new AIPlayer object
        """
        assert(checker == 'X' or checker == 'O')
        assert(tiebreak == 'LEFT' or tiebreak == 'RIGHT' or tiebreak == 'RANDOM')
        assert(lookahead >= 0)
        super().__init__(checker)
        self.tiebreak = tiebreak
        self.lookahead = lookahead
        
    def __repr__(self):
        """ returns a string representing an AIPlayer object.
        """ 
        s = 'Player ' + self.checker + ' (' + self.tiebreak + ', ' + str(self.lookahead) +')'
        return s 
    
    def max_score_column(self, scores):
        """ takes a list scores containing a score for each column of the board
            , and that returns the index of the column with the maximum score.
        """
        maxlst = []
        for i in range(len(scores)):
            if scores[i] == max(scores):
                maxlst += [i]
                
        if self.tiebreak == 'LEFT':
            return maxlst[0]
        elif self.tiebreak == 'RIGHT':
            return maxlst[-1]
        else:
            return random.choice(maxlst)
        
    def scores_for(self,b):
        """takes a Board object b and determines the called AIPlayer's scores 
            for the columns in b Each column should be assigned one of the four
            possible scores discussed in the Overview at the start of this 
            problem, based on the called AIPlayer‘s lookahead value. The method
            should return a list containing one score for each column.
        """
        scores = [0] * b.width
        for col in range(len(scores)):
            if b.can_add_to(col) == False:
                scores[col] = -1
            elif b.is_win_for(self.checker) == True:
                scores[col] = 100
            elif b.is_win_for(self.opponent_checker()) == True:
                scores[col] = 0
            elif self.lookahead == 0:
                scores[col] = 50
            else:
                b.add_checker(self.checker, col)
                oppo = AIPlayer(self.opponent_checker(), self.tiebreak, self.lookahead - 1)
                oppo_scores = oppo.scores_for(b)
                if max(oppo_scores) == 0:
                    scores[col] = 100
                elif max(oppo_scores) == 100:
                    scores[col] = 0
                else:
                    scores[col] = 50
                
                b.remove_checker(col)
                
        return scores
                
    def next_move(self,b):
        """ return the called AIPlayers's judgment of its best possible move. 
        """
        self.num_moves += 1
        return self.max_score_column(self.scores_for(b))
        
        
        
        
        
        
        
        
        
        
        
        
            
        