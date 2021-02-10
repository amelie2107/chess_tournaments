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
from tinydb import TinyDB, Query, where


def database_load(file_name, name , clear = False):
    db = TinyDB(file_name) 
    db_table = db.table(name)
    if clear:
        db_table.truncate()	# clear the table first
    return db_table


def read_database(db_name, order_by = None):
    if order_by == None:
        return db_name.all()
    else:
        if order_by == 'order by name':
            return sorted_database(db_name.all(), 'last_name', 'first_name')

        if order_by == 'order by ranking':
            return sorted_database(db_name.all(), 'ranking', order_by_multiple = 'last_name', reverse = True)

def sorted_database(dict_list, order_by, order_by_multiple = None, reverse = False):
    if order_by_multiple == None:
        return sorted(dict_list, key = lambda x: x[order_by], reverse = reverse)
    else:
        return sorted(dict_list, key = lambda x: (x[order_by], x[order_by_multiple]), reverse = reverse)
    
def search_in_database(database, where_key, where_value, other_condition = None):
        if other_condition == None:
            return database.search(where(where_key) == where_value)
        else:
            return database.search(where(where_key) == where_value and other_condition)

def search_uidlist_in_database(database, uid_list, uid_name = 'uid'):
    my_query = Query()
    return sorted_database(database.search(my_query.uid.one_of(uid_list)), 'ranking', reverse = True )

def field_in_database(dict_list, field_key):
    return {each_dict[field_key] for each_dict in dict_list}

def insert_row_in_database(database, object_serialized, multiple_object = False):
    if multiple_object:
        return database.insert_multiple(object_serialized)
    else:
        return database.insert(object_serialized)

def update_row_in_database(database, object_updated, uid_field, uid_value):
    object_updated_dict = object_updated.serialized()
    for key in object_updated_dict:
        database.update({key : object_updated_dict[key]}, where(uid_field) == uid_value)

def update_tournament_score(tournament_uid, round_score, tournaments_database):
    tournament_selected = search_in_database(tournaments_database, 'tournament_uid', tournament_uid)
    tournament_object = deserialized_tournament(tournament_selected)[0]
    tournament_object.update_score(round_score)
    update_row_in_database(tournaments_database, tournament_object, 'tournament_uid', tournament_uid)

def generate_uniqueid(database, uid_name = 'uid'):
    #retreive the players database
    full_data_base = read_database(database)
    uid_used = [0]
    #check all uid already used
    for elt in full_data_base:
        uid_used.append(int(elt.get(uid_name)))
    #return a new uid one above the max already used
    return max(uid_used) + 1

def match_details(object_match_list, players_database, tournaments_database, rounds_database, matchs_database):
    match_lst = []
    for object_match in object_match_list:
        player1 = search_in_database(players_database, 'uid', object_match.player1)[0]
        player1 = "{} {}".format(player1['first_name'], player1['last_name'])
        player2 = search_in_database(players_database, 'uid', object_match.player2)[0]
        player2 = "{} {}".format(player2['first_name'], player2['last_name'])
        tournament_name = search_in_database(tournaments_database, 'tournament_uid', object_match.tournament_uid)[0]
        round_name = search_in_database(rounds_database, 'round_uid', object_match.round_uid)[0]
        match_name = object_match.name
        match_lst.append({'player1' : player1, 'player1_uid' : object_match.player1, 'player2' : player2, 'player2_uid' : object_match.player2,'tournament' : tournament_name['name'], 'round' : round_name['name'], 'match' : match_name })
    return match_lst

def tournament_results(tournament_selection, players_database, tournaments_database, rounds_database):
    tournament_details = search_in_database(tournaments_database, 'tournament_uid', tournament_selection)[0]
    round_details = search_in_database(rounds_database, 'tournament_uid', tournament_selection)
    players_details = players_for_tournament(tournament_selection, players_database, tournaments_database)
    
    tournament_results = []
    for player in players_details:
        new_player = {}
        new_player['uid'] = player['uid']
        new_player['rk'] = player['ranking']
        new_player['Player'] = "{} {}".format(player['first_name'], player['last_name'])
        new_player['CTS'] = find_score_in_list(player['uid'], tournament_details['score'])
        
        for rnd in range(tournament_details['nb_round']):
            try:
                round_score = find_score_in_list(player['uid'],round_details[rnd]['score'])
                if round_score == None:
                    round_score = 'NP'
                new_player[round_details[rnd]['name']] = round_score
            except IndexError:
                new_player[f"Round{rnd+1}"] = 'NP'
        tournament_results.append(new_player)
    return tournament_results

def find_score_in_list(uid, scores_list):
    for score in scores_list:
        if score[0] == uid:
            return score[1]

def players_for_tournament(tournament_selection, players_database, tournaments_database):
    tournament_details = search_in_database(tournaments_database, 'tournament_uid', tournament_selection)[0]
    players_details_list = []
    for player in tournament_details['players_uid_lst']:
        player_details = search_in_database(players_database, 'uid', player)[0]
        players_details_list.append(player_details)
    return players_details_list

def is_the_round_finished(round_uid, tournaments_database, rounds_database, matchs_database):
    round_selected = search_in_database(rounds_database, 'round_uid', round_uid)
    round_object = deserialized_round(round_selected)[0]
    match_list = search_in_database(matchs_database, 'round_uid', round_uid)
    round_finished = True
    round_started = False
    match_score_list = []
    for elt in match_list:
        match_score_list += elt['score']
        if elt['status'] != 'done':
            round_finished = False
        if elt['status'] == 'done' and round_object.status == 'new':
            round_started = True
            
    if round_started:
        round_object.update_status(match_score_list, 'in progress')
        update_row_in_database(rounds_database, round_object, 'round_uid', round_uid)
        update_tournament_score(round_object.tournament_uid, round_object.score, tournaments_database)
         
    
    if round_finished:
        round_object.update_status(match_score_list)
        update_row_in_database(rounds_database, round_object, 'round_uid', round_uid)
        update_tournament_score(round_object.tournament_uid, round_object.score, tournaments_database)
    
    return round_finished
    
def is_the_tournament_finised(tournament_uid, tournaments_database, round_database):
    tournament_selected = search_in_database(tournaments_database, 'tournament_uid', tournament_uid)
    tournament_object = deserialized_tournament(tournament_selected)[0]
    round_list = search_in_database(tournaments_database, 'tournament_uid', tournament_uid)
    tournament_finised = True
    
    if len(round_list) == tournament_object.nb_round:
        for elt in round_list:
            if elt['status'] != 'done':
                tournament_finised = False
    else:
        tournament_finised = False
        
    if tournament_finised:
        tournament_object.update_status()
        update_row_in_database(tournaments_database, tournament_object, 'tournament_uid', tournament_uid)
    
    return tournament_finised

def is_process_continue(data_available):
    if data_available == []:
        return False
    else:
        return True


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
        deserialized_tournament.score = tournament['score']
        deserialized_tournament.creation_date = tournament['creation_date']
        deserialized_tournament.end_date = tournament['end_date']        
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
        deserialized_match = Match.Match(match['name'], match['player1'], match['player2'], match['tournament_uid'], match['round_uid'], match['match_uid'])
        deserialized_match.score = match['score']
        deserialized_match.status = match['status']
        deserialized_lst.append(deserialized_match)
    return deserialized_lst

def menu_function(menu_value, under_menu_value, players_database, tournaments_database, rounds_database, matchs_database):
    
    if menu_value == "add new player":
        Controller.menu_new_player(players_database)
    
    if menu_value == "create tournament":
        Controller.menu_new_tournament(players_database, tournaments_database)

    if menu_value == "show all players list": #, "show players list of a tournament"):
        Controller.menu_show_all_players_list(under_menu_value, players_database)
            
    if menu_value ==  "show players list of a tournament":
        Controller.menu_show_players_list_for_tournament(players_database, tournaments_database)
        
    if menu_value == "show tournaments list":
        Controller.menu_show_tournaments_list(under_menu_value, tournaments_database)

    if menu_value == "show round list":
        Controller.menu_show_round_list(tournaments_database, rounds_database)

    if menu_value == "show match list":
        Controller.menu_show_match_list(players_database, tournaments_database, rounds_database, matchs_database)

    if menu_value == "launch/continue tournament":
        Controller.menu_launch_tournament(players_database, tournaments_database, rounds_database, matchs_database)
                        
    if menu_value == "input match result":
        Controller.menu_input_match_result(players_database, tournaments_database, rounds_database, matchs_database)
    
    if menu_value == "update player ranking":
        Controller.menu_update_player_ranking(under_menu_value, players_database)

    if menu_value == "show tournament's results":
        Controller.menu_show_tournaments_results(players_database, tournaments_database, rounds_database)
        
    if menu_value == "exit":
        return False
    else:
        return True