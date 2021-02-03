# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:40:43 2021

@author: arnau
"""
from time import strftime, localtime
import Model
import Round
import View

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
    def __init__(self, name, uid, nb_round = 4):
        self.name = name
        self.tournament_uid = uid
        self.players_uid_lst = []
        self.score = []
        self.creation_date = strftime("%d-%m-%Y",localtime())
        self.status = 'in progress'
        self.round_lst = []
        self.nb_round = nb_round
    
    def add_players(self, player):
        if len(self.players_uid_lst) < 8:
            self.players_uid_lst.append(int(player))
            self.score.append((int(player), 0))
        else:
            print("there is already 8 players for this tournament")
    
    def start_game(self):
        if len(self.players_uid_lst) == 8:
            return True
        else:
            return False
        
    def start_round(self, players_database, rounds_database, matchs_database):
        round_uid = Model.generate_uniqueid(rounds_database, 'round_uid')
        new_round = Round.Round(f'Round{len(self.round_lst)+1}', self.players_uid_lst, self.tournament_uid, round_uid)
        self.round_lst.append(new_round.round_uid)
        if len(self.round_lst) == 0:
            new_round.first_round(players_database, matchs_database)
        if len(self.round_lst) < self.nb_round:
            new_round.others_rounds(players_database, matchs_database)
        Model.insert_object_in_database(rounds_database, new_round.serialized())

        print("** the tournament : {} is {} **".format(self.name, self.status))
        print("****** the Round{} is {} ******".format(len(self.round_lst), new_round.status))
        return new_round
    
    def serialized(self):
        return self.__dict__
        

    