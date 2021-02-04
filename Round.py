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

    def others_rounds(self, players_database, matchs_database, current_tournament_score):
        players_level = self.players_status(players_database, current_tournament_score)
        match_list = []
        idx_match = 1
        for idx in range(0, len(players_level), 2):
            match_uid = Model.generate_uniqueid(matchs_database, 'match_uid')
            object_match = Match.Match(f'match{idx_match}', players_level[idx]['uid'],players_level[idx+1]['uid'],self.tournament_uid, self.round_uid, match_uid)         
            
            self.matchs_lst.append(object_match.match_uid)
            Model.insert_object_in_database(matchs_database, object_match.serialized())
            match_list.append(object_match)
            idx_match += 1
        return match_list
            
    def players_status(self, players_database, tournament_score):
        players_status = []
        for player in self.players_lst:
            player_information = Model.search_in_database(players_database, 'uid', player)[0]
            player_name = player_information['first_name']+" "+player_information['last_name']
            player_uid = player
            player_ranking = player_information['ranking']
            for players_score in tournament_score:
                if players_score[0] == player_uid:
                    player_score = players_score[1]
            players_status.append({'name': player_name, 'uid': player_uid, 'score': player_score, 'ranking': player_ranking})
        return sorted(players_status, key = lambda x: (x['score'], x['ranking']))
            
                    
    def update_status(self, round_score, update_value = 'done'):
        self.status = update_value
        if update_value == 'done':
            self.score = round_score
            self.end_round()
        
    def serialized(self):
        return self.__dict__


