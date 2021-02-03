# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 18:14:03 2021

@author: arnau
"""
from time import strftime, localtime
import Model
import View
import Match

class Round:
    """
    This function must return a list 
    """
    def __init__(self, name, players_lst, tournament_uid, uid):
        self.name = name
        self.nb_round = 1
        self.players_lst = players_lst
        self.matchs_lst = []
        self.score = []
        self.start_date = str()
        self.start_hour = str()
        self.end_date = str()
        self.end_hour = str()
        self.tournament_uid = tournament_uid
        self.round_uid = uid
        self.status = 'new'
        
    def start_round(self):
        self.start_date = strftime("%d-%m-%Y",localtime())
        self.start_hour = strftime("%H:%M:%S",localtime())

    def end_round(self):
        self.end_date = strftime("%d-%m-%Y",localtime())
        self.end_hour = strftime("%H:%M:%S",localtime())
    
    def define_match(self, players_database, matchs_database):
#        import pdb ; pdb.set_trace()
        match_lst = []
        if int(self.name[-1]) == 1:
            self.start_round()
            match_lst = self.first_round(players_database, matchs_database)
        elif int(self.name[-1]) == 4:
            self.end_round()
        else:
            #check si score entré pour tous les matchs
            match_lst = self.others_rounds()
        return match_lst
    
    def first_round(self, players_database, matchs_database):
        match_list = []
        players_list_sorted = Model.search_uidlist_in_database(players_database, self.players_lst)
        half_list = int(len(players_list_sorted)/2)
        for idx in range(half_list):
            match_uid = Model.generate_uniqueid(matchs_database, 'match_uid')
            object_match = Match.Match(f'match{idx+1}', players_list_sorted[idx]['uid'],players_list_sorted[half_list + idx]['uid'],self.tournament_uid, self.round_uid, match_uid)
            
            self.matchs_lst.append(object_match.match_uid)
            Model.insert_object_in_database(matchs_database, object_match.serialized())
            match_list.append(object_match)

        return match_list    

    def others_rounds(self, players_database, matchs_database):
        pass
    
    def serialized(self):
        return self.__dict__


