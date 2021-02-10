# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:29:13 2021

@author: arnau
"""
from math import ceil, floor
import pandas

def my_decorateur(function):
    def my_decorate_function(*args, **kwargs):
        if args[0] == []:
            print("")
            show_list('There is not element for this selection')
        else:
            function(*args, **kwargs)
    return my_decorate_function
        

def show_menu(menu_list, menu_name, display = True):
    if display:
        print('\n{} {} {}'.format("*"*floor((57-len(menu_name))/2), menu_name, "*"*ceil((57-len(menu_name))/2)))
        print('|{}|'.format(" "*57))
        for idx,elt in enumerate(menu_list):
            print('| {} - {}{}|'.format(idx, elt, " "*(60-len(elt)-len(str(idx))-7)))
        print('|{}|'.format(" "*57))
        print('***********************************************************')

def show_list(name):
    nb_star = (60-len(name))/2
    print('{} {} {}'.format('*'*ceil(nb_star), name, '*'*floor(nb_star)))
    print("")

@my_decorateur
def show_all_players_list(player_database):
    if len(player_database) == 0:
        print("There is no players in the chess data base")
    else:
        show_player_selection(player_database)

def show_update_player_rank(first_name, last_name, old_ranking, new_ranking):
    print("{} {} ranking moved from {} to {}".format(first_name, last_name, old_ranking, new_ranking))

def show_tournament_report_note():
    print("* rk = ranking of the player, ** CTS = current tournament score")

def show_match_report_note():
    print("* NP = not played (yet)")

@my_decorateur
def show_tournament_selection(database_dict):
    print("")
    show_list('tournaments list')
    df_to_show = pandas.DataFrame.from_dict(database_dict)[['tournament_uid','name','creation_date', 'status']]
    print(df_to_show.to_string(index=False))

@my_decorateur
def show_round_selection(database_dict):
    print("")
    show_list('rounds list')
    df_to_show = pandas.DataFrame.from_dict(database_dict)[['round_uid','name','start_date', 'start_hour',  'status']]
    print(df_to_show.to_string(index=False))
    return 'coucou'

@my_decorateur
def show_match_selection(database_dict):
    print("")
    show_list('matchs list')
    df_to_show = pandas.DataFrame.from_dict(database_dict)[['match_uid','name','score', 'status']]
    print(df_to_show.to_string(index=False))

@my_decorateur
def show_player_selection(database_dict):
    print("")
    show_list('players list')
    df_to_show = pandas.DataFrame.from_dict(database_dict)[['uid','ranking','last_name','first_name','birth_date', 'gender']]
    print(df_to_show.to_string(index=False))

@my_decorateur
def show_tournament_result(database_dict):
    print("")
    show_list('tournament result')
    df_to_show = pandas.DataFrame.from_dict(database_dict)
    print(df_to_show.to_string(index=False))

def show_match_details(database_dict, players_details):
    print("")
    show_list('matchs list')
    for idx, elt in enumerate(players_details):
        database_dict[idx]['player1'] = players_details[idx]['player1']
        database_dict[idx]['player2'] = players_details[idx]['player2']
        if database_dict[idx]['score'] == []:
            database_dict[idx]['score1'] = 'NP'
            database_dict[idx]['score2'] = 'NP'
        else:
            database_dict[idx]['score1'] = database_dict[idx]['score'][0][1]
            database_dict[idx]['score2'] = database_dict[idx]['score'][1][1]
            
    df_to_show = pandas.DataFrame.from_dict(database_dict)[['match_uid', 'name', 'player1', 'score1', 'player2', 'score2', 'status']]
    print(df_to_show.to_string(index=False))
