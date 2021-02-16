# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 18:14:03 2021

@author: Amelie Noury
"""
from time import strftime, localtime
import model
import match


class Round:

    """

    This class create a round, a part of tournament
    Parameters are required : a name for the Round, the players list,
    the tournament reference (uid)
    the uid of the round
    We can then, start a round and upadte the start date and hour,
    create the match :
        - from players ranking for the first round
        - from the current score of the tournament for the others round
    The status of the round is updated when :
        - the first match is played from new to in progress
        - the last match is played from in progress to done

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
        """Update the start date and hour when the first round is created."""
        self.start_date = strftime("%d-%m-%Y", localtime())
        self.start_hour = strftime("%H:%M:%S", localtime())

    def end_round(self):
        """Update the end date and hour when the last match is played."""
        self.end_date = strftime("%d-%m-%Y", localtime())
        self.end_hour = strftime("%H:%M:%S", localtime())

    def first_round(self, players_database, matchs_database):
        """ Generate a list of match based on players ranking"""
        match_list = []

        players_list_sorted = model.search_uidlist_in_database(players_database,
                                                               self.players_lst)
        half_list = int(len(players_list_sorted)/2)
        for idx in range(half_list):
            match_uid = model.generate_uniqueid(matchs_database, 'match_uid')
            object_match = match.Match(f'match{idx+1}',
                                       players_list_sorted[idx]['uid'],
                                       players_list_sorted[half_list + idx]['uid'],
                                       self.tournament_uid, self.round_uid,
                                       match_uid)
            self.matchs_lst.append(object_match.match_uid)
            model.insert_row_in_database(matchs_database, object_match.serialized())
            match_list.append(object_match)
        self.start_round()
        return match_list

    def others_rounds(self, players_database, matchs_database, current_tournament_score):
        """Generate a list of match based on players score."""
        players_level = self.players_ranking(players_database,
                                             current_tournament_score)
        match_list = []
        idx_match = 1
        for idx in range(0, len(players_level), 2):
            match_uid = model.generate_uniqueid(matchs_database, 'match_uid')
            object_match = match.Match(f'match{idx_match}', players_level[idx]['uid'],
                                       players_level[idx+1]['uid'], self.tournament_uid,
                                       self.round_uid, match_uid)

            self.matchs_lst.append(object_match.match_uid)
            model.insert_row_in_database(matchs_database, object_match.serialized())
            match_list.append(object_match)
            idx_match += 1
        self.start_round()
        return match_list

    def players_ranking(self, players_database, tournament_score):
        """Sort the players list by tournament score."""
        players_rank = []
        for player in self.players_lst:
            player_information = model.search_in_database(players_database, 'uid', player)[0]
            player_name = player_information['first_name'] + " " + player_information['last_name']
            player_uid = player
            player_ranking = player_information['ranking']
            for players_score in tournament_score:
                if players_score[0] == player_uid:
                    player_score = players_score[1]
            players_rank.append({'name': player_name, 'uid': player_uid,
                                 'score': player_score, 'ranking': player_ranking})
        return sorted(players_rank, key=lambda x: (x['score'], x['ranking']))

    def update_status(self, round_score, update_value='done'):
        """Update the status of the Round."""
        self.status = update_value
        if update_value == 'done':
            self.score = round_score
            self.end_round()

    def serialized(self):
        """Transform the object in dictionary to save it it the database"""
        return self.__dict__
