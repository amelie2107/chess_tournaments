# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:29:13 2021

@author: arnau
"""
import Player
import Tournament
import Round
import Match
import json
import os
from tinydb import TinyDB, Query, where
#    import pdb; pdb.set_trace()


def players_database_load(file_name, clear = False):
    db = TinyDB(file_name) 
    players_table = db.table('players')
    if clear:
        players_table.truncate()	# clear the table first
    return players_table

def tournament_database_load(file_name):
    db = TinyDB(file_name) 
    tournaments_table = db.table('tournament')
    #tournaments_table.truncate()	# clear the table first
    return tournaments_table

def read_database(db_name, order_by = None):
    #treatement of the order by argument
    #import pdb; pdb.set_trace()
    #db_deserialized = deserialized_player(db_name.all())
    
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

def generate_uniqueid(players_database):
    #retreive the players database
    full_data_base = read_database(players_database)
    uid_used = [0]
    #check all uid already used
    for elt in full_data_base:
        uid_used.append(int(elt.get('uid')))
    #return a new uid one above the max already used
    return max(uid_used) + 1

def insert_player_in_database(database, player_serialized, multiple_players = False):
    if multiple_players:
        return database.insert_multiple(player_serialized)
    else:
        return database.insert(player_serialized)

def search_in_database(database, where_key, where_value):
    return database.search(where(where_key) == int(where_value))

def update_player_ranking(players_database, player_selection, new_rank_selection):
    try:
        player_information = players_database.search(where('uid') == int(player_selection))[0]
        first_name, last_name, old_ranking = player_information['first_name'], player_information['last_name'],player_information['ranking']
        players_database.update({'ranking': int(new_rank_selection)}, where('uid') == int(player_selection))
        print("{} {} ranking moved from {} to {}".format(first_name, last_name, old_ranking, new_rank_selection))
    except IndexError:
        print("The input uid does not exist!")

def insert_tournament_in_database(database, tournament_serialized, multiple_tournament = False):
    if multiple_tournament:
        return database.insert_multiple(tournament_serialized)
    else:
        return database.insert(tournament_serialized)

def deserialized_player(players_list):
    deserialized_lst = []
    for player in players_list:        
        deserialized_lst.append(Player.Player(player['first_name'], player['last_name'], player['birth_date'], player['gender'], player['ranking'], player['uid']))
    return deserialized_lst


def deserialized_tournament(tournament_list):
    deserialized_lst = []
    for tournament in tournament_list:
        pass
        #deserialized_lst.append(Player.Player(tournament['first_name'], player['last_name'], player['birth_date'], player['gender'], player['ranking']))
    return deserialized_lst


def deserialized_round(tournament_list):
    deserialized_lst = []
    for tournament in tournament_list:
        pass
        #deserialized_lst.append(Player.Player(tournament['first_name'], player['last_name'], player['birth_date'], player['gender'], player['ranking']))
    return deserialized_lst


def deserialized_match(tournament_list):
    deserialized_lst = []
    for tournament in tournament_list:
        pass
        #deserialized_lst.append(Player.Player(tournament['first_name'], player['last_name'], player['birth_date'], player['gender'], player['ranking']))
    return deserialized_lst

def return_sth_list(sth_to_return, progression, sth_else):
    print("return a list of sth (round, tournament, match)")
    
def return_player_list():
    print("here we will return a list of all players")

def update_match_score(match_name, player_name):
    print("here we will update the player name")

def update_player_rank(player_identification, new_rank):
    print("here we will update the rank of a player")