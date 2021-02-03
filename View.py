# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:29:13 2021

@author: arnau
"""
from math import ceil, floor
import pandas


def show_menu(menu_list, menu_name, display = True):
    if display:
        print('\n{} {} {}'.format("*"*floor((57-len(menu_name))/2), menu_name, "*"*ceil((57-len(menu_name))/2)))
        print('|{}|'.format(" "*57))
        for idx,elt in enumerate(menu_list):
            print('| {} - {}{}|'.format(idx, elt, " "*(60-len(elt)-len(str(idx))-7)))
        print('|{}|'.format(" "*57))
        print('***********************************************************')
    
def show_all_players_list(player_database):
    #transform the database in table
    if len(player_database) == 0:
        print("There is no players in the chess data base")
    else:
        print(pandas.DataFrame.from_dict(player_database))

def player_tournament(tournament_name, order_by)  :
    print("we will show you all players in a particular tournament here")

def tournament_result(tournament_selection):
    print("here we will show you tournament results")

def tournament_state(tournament_selection):
    print("here we will show you tournament state")

def round_state(round_selection):
    print("here we will show you round state")
    
def show_match_selection(match_selection, players_database, tournaments_database, rounds_database, matchs_database):
    pass

def show_tournament_selection(match_selection, players_database, tournaments_database, rounds_database, matchs_database):
    pass

def show_player_selection(match_selection, players_database, tournaments_database, rounds_database, matchs_database):
    pass

    
def show_sth_list(database):
    print(pandas.DataFrame.from_dict(database))