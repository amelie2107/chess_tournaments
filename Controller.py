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


def run_menu(players_database, tournaments_database):
    menu_list = ["show menu", "add new player", "show all players list", "show players list of a tournament", "show tournaments list",\
                 "show round list", "show match list", "show tournament's results", \
                 "launch tournament", "launch round", "input match result", "update player ranking"]
    player_list_menu = ["order by name", "order by ranking"                        ]
    trm_list_menu = ["all", "done", "in progress"]
    launch_menu = ["new", "in progress"]
    
    View.show_menu(menu_list, "menu")
    menu_selection = input("please enter your choice (index) : ")
    
    if menu_list[int(menu_selection)] == "add new player":
        menu_new_player(players_database)
    
    if menu_list[int(menu_selection)] == "show all players list": #, "show players list of a tournament"):
        menu_show_all_players_list(player_list_menu, players_database)
            
    if menu_list[int(menu_selection)] ==  "show players list of a tournament":
        View.show_menu(player_list_menu, "player list")
        menu_under_selection = input("please enter your choice (index) : ")
        View.show_sth_list("tournament", "all")
        tournament_name_selection = input("please select a tournament")
        View.player_tournament(tournament_name_selection, player_list_menu[int(menu_under_selection)])
    
    if menu_list[int(menu_selection)] in ("show tournaments list", "show round list", "show match list"):
        sth_to_show = re.findall("show (.*) list", menu_list[int(menu_selection)])[0]
        View.show_menu(trm_list_menu, sth_to_show)
        menu_under_selection = input("please enter your choice (index) : ")
        View.show_sth_list(sth_to_show, trm_list_menu[menu_under_selection])

    if menu_list[int(menu_selection)] == "show tournament's results":
        View.show_sth_list('tournament', 'all')
        tournament_selection = input("select your tournament index : ")
        View.tournament_result(tournament_selection)
        
    if menu_list[int(menu_selection)] == "launch tournament":
        menu_new_tournament(players_database, tournaments_database)
        
        
    if menu_list[int(menu_selection)] in ("launch round"):
        View.show_menu(launch_menu, re.findall("launch (.*)", menu_list[int(menu_selection)])[0])
        menu_under_selection = input("please enter your choice (index) : ")
        if menu_list[int(menu_selection)] == "launch tournament":
            if launch_menu[int(menu_under_selection)] == "new":
                new_tournament()
            else:
                View.show_sth_list('tournament', 'in progress')
                tournament_selection = input("select your tournament index : ")
                View.tournament_state(tournament_selection)
        if menu_list[int(menu_selection)] == "launch round":
            if launch_menu[int(menu_under_selection)] == "new":
                new_round()
            else:
                View.show_sth_list('round', 'in progress')
                round_selection = input("select your tournament index : ")
                View.round_state(round_selection)
        
    if menu_list[int(menu_selection)] == "input match result":
       #select the tournament name
       tournament_lst = Model.return_sth_list("tournament", "in progress")
       View.show_sth_list("tournament", "in progress")
       tournament_selection = input("please, select the tournament index of the match : ")
       #select the round name of the selected tournament
       round_lst = Model.return_sth_list("round", "in progress", f"Where tournament = {tournament_lst[tournament_selection]}")
       View.show_sth_list("round", "in progress")
       round_selection = input("please, select the tournament index of the match : ")
       #select the match of the selected tournament and round
       match_lst = Model.return_sth_list("match", "in progress", f"Where tournament = {tournament_lst[tournament_selection]} and round = {round_lst[round_selection]}")
       View.show_sth_list("match", "in progress")
       match_selection = input("please, select the match you want to update")
       #update the scores of the match selected
       update_match(f"Where tournament = {tournament_lst[tournament_selection]} and round = {round_lst[round_selection]} and match = {match_lst[match_selection]}")
    
    if menu_list[int(menu_selection)] == "update player ranking":
       menu_update_player_ranking(player_list_menu, players_database)
 
def menu_new_player(players_database):
    new_one = new_player(players_database)
    return Model.insert_player_in_database(players_database, new_one.serialized())

def menu_new_tournament(players_database, tournaments_database):
    new_one = new_tournament(tournaments_database)
    #Model.insert_tournament_in_database(tournaments_database, new_one.serialized())
    
    players_list = Model.read_database(players_database)
    View.show_all_players_list(players_list)
    uid_used = []
    while not new_one.start_game():
        player_selection = input("choose a player (by his uid) for this tournament or N for a new player: ")
        
        #Check if the player is already selected for the tournament, otherwise choose another player
        while player_selection in uid_used and player_selection:
            print('\n *********** This person is already selected for this tournament **********')
            player_selection = input("choose another player (by his uid) for this tournament or N for a new player: ")
            
        if player_selection.lower() == 'n':
            new_player_in_tournament = menu_new_player(players_database)
        else:
            uid_used.append(player_selection)
            new_player_in_tournament = Model.deserialized_player(Model.search_in_database(players_database,'uid', player_selection))
        new_one.add_players(new_player_in_tournament)
    Model.insert_tournament_in_database(tournaments_database, new_one.serialized())


def menu_show_all_players_list(player_list_menu, players_database):
    #Show under menu to select the order by view
    View.show_menu(player_list_menu, "player list")
    menu_under_selection = input("please enter your choice (index) : ")
    #extract order by view
    order_by_selection = player_list_menu[int(menu_under_selection)]
    View.show_all_players_list(Model.read_database(players_database, order_by_selection))

def menu_update_player_ranking(player_list_menu, players_database):
    #show the players list to select one
    menu_show_all_players_list(player_list_menu, players_database)
    player_selection = input("select the uid of the player for who you want to update the ranking : ")
    #Update the rank of the player selected
    new_rank_selection = input("Please, insert the new ranking of this player : ")
    Model.update_player_ranking(players_database, player_selection, new_rank_selection)


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
    unique_id = Model.generate_uniqueid(tournaments_database)
    return Tournament.Tournament(tournament_name, unique_id)
    
def new_round():
    print("\n *********Add information about the new player**************")
    first_name = input("First name : ")
    last_name = input("Last name : ")
    birth_date = input("Date of birth : ")
    gender = input("Gender (F/M) : ")
    ranking = 0
    return Player.Player(first_name, last_name, birth_date, gender, ranking)

def new_match():
    print("\n *********Add information about the new player**************")
    first_name = input("First name : ")
    last_name = input("Last name : ")
    birth_date = input("Date of birth : ")
    gender = input("Gender (F/M) : ")
    ranking = 0
    return Player.Player(first_name, last_name, birth_date, gender, ranking)

def update_match(arguments):
    print("here we will input the score of the match")
    match_identification = "input"
    player_identification = "input"
    scores = "input"
    Model.update_match_score(match_identification, player_identification, scores)

def update_player_rank(arguments):
    print("here we will input the rank of the player")
    player_identification = "input"
    new_rank = "input"
    Model.update_player_rank(player_identification, new_rank)