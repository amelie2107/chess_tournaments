# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:05:03 2021

@author: arnau
"""

import re
import View
import Model
import Player
import Tournament
import Round

NEW_OBJECT = ["add new player", "create tournament"]
SHOW_PLAYERS = ["show all players list", "show players list of a tournament"]
SHOW_TRM = ["show tournaments list", "show round list", "show match list"]
LAUNCH_TRM = ["launch/continue tournament"]
UPDATE_OBJECT = ["input match result", "update player ranking"]
SHOW_REPORT = ["show tournament's results"]
MENU_LIST = NEW_OBJECT + SHOW_PLAYERS + SHOW_TRM + LAUNCH_TRM + UPDATE_OBJECT + SHOW_REPORT

PLAYER_LIST_MENU = ["order by name", "order by ranking"]
SHOW_LIST_MENU = ["all", "done", "in progress"]



def run_menu(players_database, tournaments_database, rounds_database, matchs_database):
    
    View.show_menu(MENU_LIST, "menu")
    menu_selection = menu_return_selection()
    
    menu_under_selection = None
    
    if MENU_LIST[menu_selection] in SHOW_PLAYERS:
        View.show_menu(PLAYER_LIST_MENU, "menu") 
        menu_under_selection = PLAYER_LIST_MENU[menu_return_selection()]
    
    if MENU_LIST[menu_selection] == "show tournaments list":
        View.show_menu(SHOW_LIST_MENU, "menu") 
        menu_under_selection = SHOW_LIST_MENU[menu_return_selection()]    
   
    Model.menu_function(MENU_LIST[menu_selection], menu_under_selection, players_database, tournaments_database, rounds_database, matchs_database)


def menu_return_selection(target = 'index'):
    return int(input("please enter your choice ("+target+") : "))

def database_return_selection(object_name = 'object'):
    return int(input("select the "+object_name+" uid you want to launch : "))

#0
def menu_new_player(players_database):
    new_one = new_player(players_database)
    return Model.insert_player_in_database(players_database, new_one.serialized())

#1
def menu_new_tournament(players_database, tournaments_database):
    new_one = new_tournament(tournaments_database)
    #Model.insert_tournament_in_database(tournaments_database, new_one.serialized())
    players_list = Model.read_database(players_database)
    View.show_all_players_list(players_list)
    uid_used = []
    while not new_one.start_game():
        player_selection = input("choose a player (by his uid) for this tournament or N for a new player: ")
        #Check if the player is already selected for the tournament, otherwise choose another player
        uid_available = Model.field_in_database(players_list, 'uid')
        while player_selection in uid_used or int(player_selection) not in uid_available:
            print('\n *********** This person is already selected or does not exist for this tournament **********')
            player_selection = input("choose another player (by his uid) for this tournament or N for a new player: ")
            
        if player_selection.lower() == 'n':
            new_player_in_tournament = menu_new_player(players_database)
        else:
            uid_used.append(player_selection)
            #A definir soit on ne met que les uid soit les players!!!
            new_player_in_tournament = player_selection
        new_one.add_players(new_player_in_tournament) 
    Model.insert_tournament_in_database(tournaments_database, new_one.serialized())

#2
def menu_show_all_players_list(order_by_selection, players_database):
    #extract order by view
    View.show_all_players_list(Model.read_database(players_database, order_by_selection))

#3
def menu_show_players_list_for_tournament(under_menu_value, players_database, tournaments_database):
    View.show_sth_list(tournaments_database)
    tournament_name_selection = database_return_selection('tournament')
    View.player_tournament(tournament_name_selection, under_menu_value)

#4
def menu_show_tournaments_list(selected_field, tournaments_database):
    if selected_field == 'all':
        tournament_table_selection = Model.return_all_database(tournaments_database)
    else:
        tournament_table_selection = Model.search_in_database(tournaments_database, 'status', selected_field)
    View.show_sth_list(tournament_table_selection)

#5
def menu_show_round_list(tournaments_database, rounds_database):
    menu_show_tournaments_list('all', tournaments_database)
    tournament_selection = database_return_selection('tournament')
    selection_to_show = Model.search_in_database(rounds_database, 'tournament_uid', tournament_selection)
    View.show_sth_list(selection_to_show)

#6
def menu_show_match_list(tournaments_database, rounds_database, matchs_database):        
    menu_show_round_list(tournaments_database, rounds_database)
    round_selection = database_return_selection('round')
    selection_to_show = Model.search_in_database(matchs_database, 'round_uid', round_selection)
    View.show_sth_list(selection_to_show)

#7
def menu_launch_tournament(players_database, tournaments_database, rounds_database, matchs_database):
    menu_show_tournaments_list('all', tournaments_database)
    tournament_selection = database_return_selection('tournament')
    tournament_selected = Model.search_in_database(tournaments_database, 'tournament_uid', tournament_selection)
    tournament_object = Model.deserialized_tournament(tournament_selected)[0]    
    tournament_object.start_round(players_database, rounds_database, matchs_database)
    Model.update_row_in_database(tournaments_database, tournament_object, 'tournament_uid',tournament_object.tournament_uid)

#8
def menu_input_match_result(players_database, tournaments_database, rounds_database, matchs_database):
    menu_show_match_list(tournaments_database, rounds_database, matchs_database)
    #update the scores of the match selected
    match_selection = database_return_selection('match')
    match_selected = Model.search_in_database(matchs_database, 'match_uid', match_selection)
    match_object = Model.deserialized_match(match_selected)[0]
    #round_object.(players_database, matchs_database)
    match_details_dict = Model.match_details(match_object, players_database, tournaments_database, rounds_database, matchs_database)
    match_score = input_match_scores(match_details_dict)
    match_object.update_score(match_score)
    Model.update_row_in_database(matchs_database, match_object, 'match_uid',match_object.match_uid)
    Model.is_the_round_finished(match_object.round_uid, tournaments_database, rounds_database, matchs_database)
    Model.is_the_tournament_finised(match_object.tournament_uid, tournaments_database, rounds_database)
    
    
#9
def menu_update_player_ranking(PLAYER_LIST_MENU, players_database):
    #show the players list to select one
    menu_show_all_players_list(PLAYER_LIST_MENU, players_database)
    player_selection = input("select the uid of the player for who you want to update the ranking : ")
    #Update the rank of the player selected
    new_rank_selection = input("Please, insert the new ranking of this player : ")
    Model.update_player_ranking(players_database, player_selection, new_rank_selection)

#10
def menu_show_tournaments_results():
    View.show_sth_list('tournament', 'all')
    tournament_selection = database_return_selection('tournament')
    View.tournament_result(tournament_selection)
    

def new_player(players_database):
    print("\n *********Add information about the new player**************")
    first_name = input("First name : ")
    last_name = input("Last name : ")
    birth_date = input("Date of birth : ")
    gender = input("Gender (F/M) : ")
    ranking = 0
    unique_id = Model.generate_uniqueid(players_database)
    return Player.Player(first_name, last_name, birth_date, gender, ranking, unique_id)

def new_tournament(tournaments_database):
    print("\n ********* Add information about the new tournament **************")
    tournament_name = input("Please, choose a name for this new tournament : ")
    unique_id = Model.generate_uniqueid(tournaments_database, 'tournament_uid')
    return Tournament.Tournament(tournament_name, int(unique_id))
    
def input_match_scores(match_dict):
    print("you have selected the tournament : {}, the round : {} and the match : {}".format(match_dict['tournament'], match_dict['round'], match_dict['match']))
    print("Currently {} is playing against {}".format(match_dict['player1'], match_dict['player2']))
    player1_score = input('Enter the score of {} : '.format(match_dict['player1']))
    player2_score = input('Enter the score of {} : '.format(match_dict['player2']))
    return [(match_dict['player1_uid'],player1_score),(match_dict['player2_uid'],player2_score)]

def update_player_rank(arguments):
    print("here we will input the rank of the player")
    player_identification = "input"
    new_rank = "input"
    Model.update_player_rank(player_identification, new_rank)