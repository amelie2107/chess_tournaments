# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:29:13 2021

@author: arnau
"""
import Player
import Tournament
import Round
import Match
import Controller
import json
import os
from tinydb import TinyDB, Query, where
#    import pdb; pdb.set_trace()


def database_load(file_name, name , clear = False):
    db = TinyDB(file_name) 
    db_table = db.table(name)
    if clear:
        db_table.truncate()	# clear the table first
    return db_table


def read_database(db_name, order_by = None):
     
    if order_by == None:
        return db_name.all()
        #return db_deserialized
    else:
        if order_by == 'order by name':
            return sorted(db_name.all(), key= lambda x: x['first_name'])
            #return sorted(db_deserialized, key= lambda x: x.first_name)

        if order_by == 'order by ranking':
            #order_by = 'ranking'  
            #return sorted(db_deserialized, key= lambda x: x.ranking)
            return sorted(db_name.all(), key= lambda x: x['ranking'])

def generate_uniqueid(database, uid_name = 'uid'):
    #retreive the players database
    full_data_base = read_database(database)
    uid_used = [0]
    #check all uid already used
    for elt in full_data_base:
        uid_used.append(int(elt.get(uid_name)))
    #return a new uid one above the max already used
    return max(uid_used) + 1

def insert_player_in_database(database, player_serialized, multiple_players = False):
    if multiple_players:
        return database.insert_multiple(player_serialized)
    else:
        return database.insert(player_serialized)

def search_in_database(database, where_key, where_value, other_condition = None):
        if other_condition == None:
            return database.search(where(where_key) == where_value)
        else:
            return database.search(where(where_key) == where_value and other_condition)
 
def return_all_database(database):
    return database.all()

def search_uidlist_in_database(database, uid_list, uid_name = 'uid'):
    my_query = Query()
    return sorted(database.search(my_query.uid.one_of(uid_list)), key= lambda x: x['ranking'], reverse = True )


def field_in_database(dict_list, field_key):
    return {each_dict[field_key] for each_dict in dict_list}


def update_player_ranking(players_database, player_selection, new_rank_selection):
    try:
        player_information = players_database.search(where('uid') == int(player_selection))[0]
        first_name, last_name, old_ranking = player_information['first_name'], player_information['last_name'],player_information['ranking']
        players_database.update({'ranking': int(new_rank_selection)}, where('uid') == int(player_selection))
        print("{} {} ranking moved from {} to {}".format(first_name, last_name, old_ranking, new_rank_selection))
    except IndexError:
        print("The input uid does not exist!")
        
def update_row_in_database(database, object_updated, uid_field, uid_value):
    object_updated_dict = object_updated.serialized()
    for key in object_updated_dict:
        print("update field {} = {}".format(key, object_updated_dict[key]))
        database.update({key : object_updated_dict[key]}, where(uid_field) == uid_value)

def insert_tournament_in_database(database, tournament_serialized, multiple_tournament = False):
    if multiple_tournament:
        return database.insert_multiple(tournament_serialized)
    else:
        return database.insert(tournament_serialized)

def insert_object_in_database(database, object_serialized, multiple_object = False):
    if multiple_object:
        return database.insert_multiple(object_serialized)
    else:
        return database.insert(object_serialized)

def deserialized_player(players_list):
    deserialized_lst = []
    for player in players_list:        
        deserialized_lst.append(Player.Player(player['first_name'], player['last_name'], player['birth_date'], player['gender'], player['ranking'], player['uid']))
    return deserialized_lst


def deserialized_tournament(tournament_list):
    deserialized_lst = []
    for tournament in tournament_list:
        deserialized_tournament = Tournament.Tournament(tournament['name'], tournament['tournament_uid'])
        deserialized_tournament.players_uid_lst = tournament['players_uid_lst']    
        deserialized_tournament.creation_date = tournament['creation_date']
        deserialized_tournament.status = tournament['status']
        deserialized_tournament.round_lst = tournament['round_lst']
        deserialized_tournament.nb_round = tournament['nb_round']
        deserialized_lst.append(deserialized_tournament)
    return deserialized_lst


def deserialized_round(round_list):
    deserialized_lst = []
    for one_round in round_list:
        deserialized_round = Round.Round(one_round['name'], one_round['players_lst'], one_round['tournament_uid'], one_round['round_uid'])
        deserialized_round.matchs_lst = one_round['matchs_lst']
        deserialized_round.score = one_round['score']
        deserialized_round.start_date = one_round['start_date']
        deserialized_round.start_hour = one_round['start_hour']
        deserialized_round.end_date = one_round['end_date']
        deserialized_round.end_hour = one_round['end_hour']
        deserialized_round.status = one_round['status'] 
        deserialized_lst.append(deserialized_round)
    return deserialized_lst


def deserialized_match(match_list):
    deserialized_lst = []
    for match in match_list:
        deserialized_match = Match.Match(match['name'], match['player1'], match['player2'], match['tournament_uid'], match['round_uid'], match['uid'])
        deserialized_match.score = match['score']
        deserialized_match.status = match['status']
        deserialized_lst.append(deserialized_match)
    return deserialized_lst

def return_sth_list(sth_to_return, progression, sth_else):
    print("return a list of sth (round, tournament, match)")
    
def return_player_list():
    print("here we will return a list of all players")

def update_match_score(match_name, player_name):
    print("here we will update the player name")

def update_player_rank(player_identification, new_rank):
    print("here we will update the rank of a player")

def menu_function(menu_value, under_menu_value, players_database, tournaments_database, rounds_database, matchs_database):
    
    if menu_value == "add new player":
        Controller.menu_new_player(players_database)
    
    if menu_value == "show all players list": #, "show players list of a tournament"):
        Controller.menu_show_all_players_list(under_menu_value, players_database)
            
    if menu_value ==  "show players list of a tournament":
        Controller.menu_show_players_list_for_tournament(under_menu_value, players_database, tournaments_database)
        
    if menu_value == "show tournaments list":
        Controller.menu_show_tournaments_list(under_menu_value, tournaments_database)

    if menu_value == "show round list":
        Controller.menu_show_round_list(tournaments_database, rounds_database)

    if menu_value == "show match list":
        Controller.menu_show_match_list(tournaments_database, rounds_database, matchs_database)

    if menu_value == "show tournament's results":
        Controller.menu_show_tournaments_results()
        
    if menu_value == "create tournament":
        Controller.menu_new_tournament(players_database, tournaments_database)

    if menu_value == "launch tournament":
        updated_tournament = Controller.menu_launch_tournament(players_database, tournaments_database, rounds_database, matchs_database)
        update_row_in_database(tournaments_database, updated_tournament, 'tournament_uid',updated_tournament.tournament_uid)
        
    if menu_value == "launch round":   
        Controller.menu_launch_round(players_database, tournaments_database, rounds_database, matchs_database)
                
    if menu_value == "input match result":
        Controller.menu_input_match_result(players_database, tournaments_database, rounds_database, matchs_database)
    
    if menu_value == "update player ranking":
        Controller.menu_update_player_ranking(under_menu_value, players_database)
