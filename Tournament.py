# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:40:43 2021

@author: arnau
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:39:28 2021

@author: arnau
"""

class Tournament:
    """ 
    A tournament begin with 8 players. 
    This program must generate 4 pairs of players for each game round
    This program save the score of each round 
    and start again the two previous line. When each playeur played against each other players,
    the Tournament is finish.
    Parameters are name, place, date, nb_round (4 by default), round, players, 
    time control (bullet, blitz or quick play), description.
    
    """
    def __init__(self, name, players_lst):
        self.name = name
        self.players_lst = players_lst
    
    def player_duo(self):
        pass