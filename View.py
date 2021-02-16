# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:29:13 2021

@author: Amelie Noury
"""
from math import ceil, floor
import pandas


def my_decorateur(function):
    """This decorateur verify if there is something to show"""
    def my_decorate_function(*args, **kwargs):
        if args[0] == []:
            print("")
            show_list('There is not element for this selection')
        else:
            function(*args, **kwargs)
    return my_decorate_function


def show_menu(menu_list, menu_name, display=True):
    """This function show a nice menu display"""
    if display:
        print('\n{} {} {}'.format("*"*floor((57-len(menu_name))/2), menu_name,
                                  "*"*ceil((57-len(menu_name))/2)))
        print('|{}|'.format(" "*57))
        if len(menu_list) == 1:
            middle = (57-len(menu_list[0]))/2
            print('|{}{}{}|'.format(" "*floor(middle), menu_list[0], " "*ceil(middle)))
        else:
            for idx, elt in enumerate(menu_list):
                print('| {} - {}{}|'.format(idx, elt, " "*(60-len(elt)-len(str(idx))-7)))
        print('|{}|'.format(" "*57))
        print('***********************************************************')


def show_list(name):
    """This menu show a nice list display"""
    nb_star = (60-len(name))/2
    print('{} {} {}'.format('*'*ceil(nb_star), name, '*'*floor(nb_star)))
    print("")


def show_update_player_rank(first_name, last_name, old_ranking, new_ranking):
    """This function print the changement of ranking of a player"""
    print("{} {} ranking moved from {} to {}".format(first_name, last_name,
                                                     old_ranking, new_ranking))


def show_tournament_report_note():
    """This function show a foot note"""
    print("* rk = ranking of the player, ** CTS = current tournament score")


def show_match_report_note():
    """This function show a foot note"""
    print("* NP = not played (yet)")


@my_decorateur
def show_all_players_list(player_database):
    """This function print all players in the database"""
    if len(player_database) == 0:
        print("There is no players in the chess data base")
    else:
        show_player_selection(player_database)


@my_decorateur
def show_tournament_selection(database_dict):
    """This function show a tournament selection"""
    print("")
    show_list('tournaments list')
    df_to_show = pandas.DataFrame.from_dict(database_dict)[['tournament_uid', 'name', 'time_control',
                                                            'creation_date', 'status']]
    print(df_to_show.to_string(index=False))


@my_decorateur
def show_round_selection(database_dict):
    """This function show a round selection"""
    print("")
    show_list('rounds list')
    df_to_show = pandas.DataFrame.from_dict(database_dict)[['round_uid', 'name', 'start_date',
                                                            'start_hour', 'end_date', 'end_hour', 'status']]
    print(df_to_show.to_string(index=False))
    return 'coucou'


@my_decorateur
def show_match_selection(database_dict):
    """This function show a match list"""
    print("")
    show_list('matchs list')
    df_to_show = pandas.DataFrame.from_dict(database_dict)[['match_uid', 'name', 'score', 'status']]
    print(df_to_show.to_string(index=False))


@my_decorateur
def show_player_selection(database_dict):
    """This function show a player"""
    print("")
    show_list('players list')
    df_to_show = pandas.DataFrame.from_dict(database_dict)[['uid', 'ranking', 'last_name',
                                                            'first_name', 'birth_date', 'gender']]
    print(df_to_show.to_string(index=False))


@my_decorateur
def show_tournament_result(database_dict):
    """This function show the result of a tournament"""
    print("")
    show_list('tournament result')
    df_to_show = pandas.DataFrame.from_dict(database_dict)
    print(df_to_show.to_string(index=False))


def show_match_details(database_dict, players_details):
    """This function show the details of a match"""
    print("")
    show_list('matchs list')
    for idx, elt in enumerate(players_details):
        database_dict[idx]['player1'] = elt['player1']
        database_dict[idx]['player2'] = elt['player2']
        if database_dict[idx]['score'] == []:
            database_dict[idx]['score1'] = 'NP'
            database_dict[idx]['score2'] = 'NP'
        else:
            database_dict[idx]['score1'] = database_dict[idx]['score'][0][1]
            database_dict[idx]['score2'] = database_dict[idx]['score'][1][1]

    df_to_show = pandas.DataFrame.from_dict(database_dict)[['match_uid', 'name', 'player1',
                                                            'score1', 'player2', 'score2',
                                                            'status']]
    print(df_to_show.to_string(index=False))
