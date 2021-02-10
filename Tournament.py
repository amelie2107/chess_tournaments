# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:40:43 2021

@author: arnau
"""
from time import strftime, localtime
import Controller
import Model
import Round

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
        self.end_date = str()
        self.status = 'new'
        self.round_lst = []
        self.nb_round = nb_round
    
    def end_tournament(self):
        self.end_date = strftime("%d-%m-%Y",localtime())

    def add_players_in_tournament(self, players_list, players_database):
        uid_used = []
        while not self.start_game():
            player_selection = input("choose a player (by his uid) for this tournament or N for a new player: ")
            #Check if the player is already selected for the tournament, otherwise choose another player
            uid_available = Model.field_in_database(players_list, 'uid')

            while self.conditions_to_add_player(uid_available, uid_used, player_selection):
                print('\n *** This person is already selected or does not exist for this tournament ***')
                player_selection = input("choose another player (by his uid) for this tournament or N for a new player: ")
                
            if player_selection.lower() == 'n':
                new_player_in_tournament = Controller.menu_new_player(players_database)
            else:
                uid_used.append(player_selection)
                new_player_in_tournament = player_selection
            self.add_players(new_player_in_tournament) 

    def add_players(self, player):
        if len(self.players_uid_lst) < 8:
            self.players_uid_lst.append(int(player))
            self.score.append((int(player), 0))
        else:
            print("there is already 8 players for this tournament")
            
    def conditions_to_add_player(self, uid_available, uid_used, player_selection):
        cond1_new_player = player_selection not in ['n', 'N']
        cond2_uid_used = player_selection in uid_used
        try:
            cond3_uid_available = int(player_selection) not in uid_available
        except ValueError:
            cond3_uid_available = player_selection not in uid_available
        
        return cond1_new_player and (cond2_uid_used or cond3_uid_available)

    
    def start_game(self):
        if len(self.players_uid_lst) == 8:
            return True
        else:
            return False

    def is_first_round(self):
        if len(self.round_lst) == 0:
            return True
        else:
            return False

    def previous_round_finished(self, rounds_database):
        is_finished = False
        if len(self.round_lst) != 0:
            last_round = self.round_lst[-1]
            round_selected = Model.search_in_database(rounds_database, 'round_uid', last_round)[0]
            if round_selected['status'] == 'done':
                is_finished = True
        else:
            is_finished = True
        return is_finished

    def start_round(self, players_database, rounds_database, matchs_database):

        new_round = None
        if self.status != 'done':
            if self.previous_round_finished(rounds_database):
                if self.start_game():

                    round_uid = Model.generate_uniqueid(rounds_database, 'round_uid')
                    new_round = Round.Round(f'Round{len(self.round_lst)+1}', self.players_uid_lst, self.tournament_uid, round_uid)
                    if self.is_first_round():
                        self.status = 'in progress'
                        new_round.first_round(players_database, matchs_database)
                    else: 
                        new_round.others_rounds(players_database, matchs_database, self.score)                   
                    self.round_lst.append(new_round.round_uid)
                    Model.insert_row_in_database(rounds_database, new_round.serialized())
                    print("\n A new round, {}, have been created".format(new_round.name))
                else:
                    print("\n Players are missing to start this tournament.")
            else:
                print("\n A round of this tournament is already in progress.")
                print("You must finish the previous round to launch a new round.")
                print("select input match result in the menu")
        else:
            print("\n The tournament is already finished since {}".format(self.end_date))
        return new_round
        
    def update_status(self, updated_value = 'done'):
        self.status = updated_value
        if updated_value == 'done':
            self.end_tournament()

    def update_score(self, round_score_values):
        if len(self.score) == 0:
            self.score = round_score_values
        else:
            for round_score in round_score_values:
                for idx, tournament_score in enumerate(self.score):
                    if tournament_score[0] == round_score[0]:
                       self.score[idx][1] += round_score[1]

    def serialized(self):
        return self.__dict__
        

    