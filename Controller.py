# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:05:03 2021

@author: arnau
"""

import View
import Model
import Player
import Tournament

NEW_OBJECT = ["add new player", "create tournament"]
SHOW_PLAYERS = ["show all players list", "show players list of a tournament"]
SHOW_TRM = ["show tournaments list", "show round list", "show match list"]
LAUNCH_TRM = ["launch/continue tournament"]
UPDATE_OBJECT = ["input match result", "update player ranking"]
SHOW_REPORT = ["show tournament's results"]
EXIT = ["exit"]
MENU_LIST = NEW_OBJECT + SHOW_PLAYERS + SHOW_TRM + LAUNCH_TRM + UPDATE_OBJECT + SHOW_REPORT + EXIT

PLAYER_LIST_MENU = ["order by name", "order by ranking"]
SHOW_LIST_MENU = ["all", "done", "in progress", "new"]

def my_decorateur(function):
    def my_decorate_function(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except:    
            print("")
            View.show_list('There is not element for this selection')
    return my_decorate_function
    

def run_menu(players_database, tournaments_database, rounds_database, matchs_database):
    
    View.show_menu(MENU_LIST, "menu")
    menu_selection = menu_return_selection()
    
    menu_under_selection = None
    
    if MENU_LIST[menu_selection] == "show all players list":
        View.show_menu(PLAYER_LIST_MENU, "menu") 
        menu_under_selection = PLAYER_LIST_MENU[menu_return_selection()]
    
    if MENU_LIST[menu_selection] == "show tournaments list":
        View.show_menu(SHOW_LIST_MENU, "menu") 
        menu_under_selection = SHOW_LIST_MENU[menu_return_selection()]    
   
    continue_admin = Model.menu_function(MENU_LIST[menu_selection], menu_under_selection, players_database, tournaments_database, rounds_database, matchs_database) 
    print("")
    if continue_admin:
        wait_entry = input('******************* press entry to continue ******************')
    return continue_admin

def menu_return_selection(target = 'index'):
    return int(input("please enter your choice ("+target+") : "))

def database_return_selection(object_name = 'object', object_action = 'launch'):
    return int(input(f"select the {object_name} uid you want to {object_action} : "))

#0
def menu_new_player(players_database):
    new_one = new_player(players_database)
    return Model.insert_row_in_database(players_database, new_one.serialized())

#1
def menu_new_tournament(players_database, tournaments_database):
    new_one = new_tournament(tournaments_database)
    players_list = Model.read_database(players_database)
    View.show_all_players_list(players_list)
    new_one.add_players_in_tournament(players_list, players_database)
    Model.insert_row_in_database(tournaments_database, new_one.serialized())

#2
def menu_show_all_players_list(order_by_selection, players_database):
    #extract order by view
    players_list = Model.read_database(players_database, order_by_selection)
    View.show_all_players_list(players_list)

#3
def menu_show_players_list_for_tournament(players_database, tournaments_database):
    View.show_tournament_selection(tournaments_database)
    tournament_selection = database_return_selection('tournament','see')
    players_list = Model.players_for_tournament(tournament_selection, players_database, tournaments_database)
    View.show_player_selection(Model.sorted_database(players_list,'last_name'))
    
#4
def menu_show_tournaments_list(selected_field, tournaments_database):
    if selected_field == 'all':
        tournament_table_selection = Model.read_database(tournaments_database)
    else:
        tournament_table_selection = Model.search_in_database(tournaments_database, 'status', selected_field)
    View.show_tournament_selection(tournament_table_selection)

#5
def menu_show_round_list(tournaments_database, rounds_database):
    menu_show_tournaments_list('all', tournaments_database)
    tournament_selection = database_return_selection('tournament','see')
    selection_to_show = Model.search_in_database(rounds_database, 'tournament_uid', tournament_selection)
    View.show_round_selection(selection_to_show)
    return Model.is_process_continue(selection_to_show)
    
#6
def menu_show_match_list(players_database, tournaments_database, rounds_database, matchs_database):        
    is_available = menu_show_round_list(tournaments_database, rounds_database)
    if is_available:
        round_selection = database_return_selection('round','see')
        selection_to_show = Model.search_in_database(matchs_database, 'round_uid', round_selection)
        match_object = Model.deserialized_match(selection_to_show)
        match_list = Model.match_details(match_object, players_database, tournaments_database, rounds_database, matchs_database)
        View.show_match_details(selection_to_show, match_list)
        View.show_match_report_note()
    else:
        View.show_list("The tournament selected is not yet started")
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
    menu_show_match_list(players_database, tournaments_database, rounds_database, matchs_database)
    match_selection = database_return_selection('match','update')
    match_selected = Model.search_in_database(matchs_database, 'match_uid', match_selection)
    match_object = Model.deserialized_match(match_selected)[0]
    match_details_dict = Model.match_details([match_object], players_database, tournaments_database, rounds_database, matchs_database)[0]
    match_score = input_match_scores(match_details_dict)
    match_object.update_score(match_score)
    Model.update_row_in_database(matchs_database, match_object, 'match_uid',match_object.match_uid)
    Model.is_the_round_finished(match_object.round_uid, tournaments_database, rounds_database, matchs_database)
    Model.is_the_tournament_finised(match_object.tournament_uid, tournaments_database, rounds_database)

#9
def menu_update_player_ranking(PLAYER_LIST_MENU, players_database):
    #show the players list to select one
    menu_show_all_players_list(PLAYER_LIST_MENU, players_database)
    player_selection, new_rank_selection = input_player_rank()
    #Update the rank of the player selected
    player_selected = Model.search_in_database(players_database, 'uid', player_selection)
    player_object = Model.deserialized_player(player_selected)[0]
    View.show_update_player_rank(player_object.first_name, player_object.last_name, player_object.ranking, new_rank_selection)
    Model.update_row_in_database(players_database, player_object, 'uid',player_object.uid)

#10
def menu_show_tournaments_results(players_database, tournaments_database, rounds_database):
    menu_show_tournaments_list('all', tournaments_database)
    tournament_selection = database_return_selection('tournament','see results')
    tournament_results = Model.tournament_results(tournament_selection, players_database, tournaments_database, rounds_database)
    View.show_tournament_result(Model.sorted_database(tournament_results, 'CTS', reverse = True))
    View.show_tournament_report_note()

def new_player(players_database):
    print("\n *********Add information about the new player**************")
    first_name = input("First name : ")
    last_name = input("Last name : ")
    birth_date = input("Date of birth(dd/mm/yyyy) : ")
    gender = input("Gender (F/M) : ")
    ranking = 0
    unique_id = Model.generate_uniqueid(players_database)
    return Player.Player(first_name.capitalize(), last_name.capitalize(), birth_date, gender, ranking, unique_id)

def new_tournament(tournaments_database):
    print("\n ********* Add information about the new tournament **************")
    tournament_name = input("Please, choose a name for this new tournament : ")
    unique_id = Model.generate_uniqueid(tournaments_database, 'tournament_uid')
    return Tournament.Tournament(tournament_name, int(unique_id))
    
def input_match_scores(match_dict):
    print("\n you have selected : \n   * the tournament : {}, \n   * the round : {}, \n   * the match : {}".format(match_dict['tournament'], match_dict['round'], match_dict['match']))
    print("   * Currently {} is playing against {}".format(match_dict['player1'], match_dict['player2']))
    player1_score = input('Enter the score of {} : '.format(match_dict['player1']))
    player2_score = input('Enter the score of {} : '.format(match_dict['player2']))
    return [(match_dict['player1_uid'],player1_score),(match_dict['player2_uid'],player2_score)]

def input_player_rank():
    player_selection = input("select the uid of the player for who you want to update the ranking : ")
    new_rank_selection = input("Please, insert the new ranking of this player : ")
    return int(player_selection), int(new_rank_selection)