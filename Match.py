# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:39:28 2021

@author: arnau
"""

class Match:

    """
    This class represent a match between two players
    This class must return a tuple of two lists. 
    Each list contain a player instance and a score
    The winner has 1 point
    The loser has 0 point
    If it's a draw match the score is 0.5 for each player
    """
    def __init__(self, name, player1, player2, tournament_uid, round_uid, uid):
        self.name = name
        self.player1 = player1
        self.player2 = player2
        self.score = []
        self.tournament_uid = tournament_uid
        self.round_uid = round_uid
        self.match_uid = uid
        self.status = 'in progress'
  
    def update_score(self):
        self.status = 'done'

    def serialized(self):
        return self.__dict__
 
    def show_winner(self, winner_name):
        print("")
        print("Congratulation {} !".format(winner_name))


