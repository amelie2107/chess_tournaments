# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:40:43 2021

@author: arnau
"""
from datetime import date

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
    def __init__(self, name, uid):
        self.name = name
        self.players_lst = []
        self.creation_date = date.today()
        self.uid = uid
    
    def add_players(self, player):
        if len(self.players_lst) < 8:
            self.players_lst.append(player)
        else:
            print("there is already 8 players for this tournament")
    
    def start_game(self):
        if len(self.players_lst) == 8:
            return True
        else:
            return False
    
    def serialized(self):
        return self.__dict__
        
    def player_duo(self):
        pass
    