# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:29:13 2021

@author: Amelie Noury
"""
from tinydb import TinyDB, Query, where
import controller
import view
import player
import tournament
import roundo
import match


def database_load(file_name, name, clear=False):
    """

    Parameters
    ----------
    file_name : name of the file name database .json
    name : name of the table
    clear : if we want to clear the database before reading, optional. The default is False.

    Returns
    -------
    db_table : the full database selected

    """
    database = TinyDB(file_name)
    db_table = database.table(name)
    if clear:
        # clear the table first
        db_table.truncate()
    return db_table

def load_all_database(CLEAR=False):
    """ This function load all the databases used in this programm """
    players_database = database_load('chess_players_database.json', 'players')
    tournaments_database = database_load('chess_tournaments_database.json',
                                               'tournaments', CLEAR)
    rounds_database = database_load('chess_rounds_database.json', 'rounds', CLEAR)
    matchs_database = database_load('chess_matchs_database.json', 'matchs', CLEAR)
    return players_database, tournaments_database, rounds_database, matchs_database


def read_database(db_name, order_by=None):
    """

    Parameters
    ----------
    db_name : a tinyDB data base
    order_by : We can choose to sort data by name or ranking, calling the function
    sorted_database

    Returns
    -------
    A list of dictionnary corresponding to the row of the database

    """
    database_value = db_name.all()
    if order_by == 'order by name':
        database_value = sorted_database(db_name.all(), 'last_name', 'first_name')

    if order_by == 'order by ranking':
        database_value = sorted_database(db_name.all(), 'ranking',
                                         order_by_multiple='last_name',
                                         reverse=True)
    return database_value


def sorted_database(dict_list, order_by, order_by_multiple=None, reverse=False):
    """This function sort the list of dictonnary by one or multiple keys enter in parameter"""
    database_value = sorted(dict_list, key=lambda x: x[order_by], reverse=reverse)
    if order_by_multiple is not None:
        database_value = sorted(dict_list, key=lambda x: (x[order_by], x[order_by_multiple]),
                                reverse=reverse)
    return database_value


def search_in_database(database, where_key, where_value, other_condition=None):
    """

    Parameters
    ----------
    database : a TinyDB database
    where_key : The field by which we want to search
    where_value : The value of the key by which we want to search
    other_condition : this OPTIONAL parameter allow to find a row by multiple fields

    Returns
    -------
    The list of dictionnary corresponding

    """
    database_value = database.search(where(where_key) == where_value)
    if other_condition is not None:
        database_value = database.search(where(where_key) == where_value and other_condition)
    return database_value

def search_match_in_database(database, uid_list):
    """Search matchs by a list of round uid"""
    my_query = Query()
    return database.search(my_query.round_uid.one_of(uid_list))


def search_uidlist_in_database(database, uid_list):
    """Search players by a list of uid"""
    my_query = Query()
    return sorted_database(database.search(my_query.uid.one_of(uid_list)),
                           'ranking', reverse=True)


def field_in_database(dict_list, field_key):
    """Search all value of a field enter in parameter"""
    return {each_dict[field_key] for each_dict in dict_list}


def insert_row_in_database(database, object_serialized, multiple_object=False):
    """Insert row serialized in a defined database"""
    if multiple_object:
        database_value = database.insert_multiple(object_serialized)
    else:
        database_value = database.insert(object_serialized)
    return database_value


def update_row_in_database(database, object_updated, uid_field, uid_value):
    """

    The function update an object in the database, for sample the score of the played match

    Parameters
    ----------
    database : TinyDB we want to update
    object_updated : updated object (Player, tournament, round or match)
    uid_field : name of the uid field used in the database (uid, tournament_uid,...)
    uid_value : uid of the object we want to update

    """
    object_updated_dict = object_updated.serialized()
    for key in object_updated_dict:
        database.update({key: object_updated_dict[key]}, where(uid_field) == uid_value)


def update_tournament_score(tournament_uid, round_score, tournaments_database):
    """ This function allow to update score in a tournament after a played match"""
    tournament_selected = search_in_database(tournaments_database, 'tournament_uid', tournament_uid)
    tournament_object = deserialized_tournament(tournament_selected)[0]
    tournament_object.update_score(round_score)
    update_row_in_database(tournaments_database, tournament_object,
                           'tournament_uid', tournament_uid)


def generate_uniqueid(database, uid_name='uid'):
    """This function generate an id never used in the database"""
    # Retreive the players database
    full_data_base = read_database(database)
    uid_used = [0]
    # Check all uid already used
    for elt in full_data_base:
        uid_used.append(int(elt.get(uid_name)))
    # Return a new uid one above the max already used
    return max(uid_used) + 1


def match_details(object_match_list, players_database, tournaments_database, rounds_database):
    """

    This function retreive all information regading a match, players name,
    tournament name and match name.

    """
    match_lst = []
    for object_match in object_match_list:
        player1 = search_in_database(players_database, 'uid', object_match.player1)[0]
        player1 = "{} {}".format(player1['first_name'], player1['last_name'])
        player2 = search_in_database(players_database, 'uid', object_match.player2)[0]
        player2 = "{} {}".format(player2['first_name'], player2['last_name'])
        tournament_name = search_in_database(tournaments_database, 'tournament_uid',
                                             object_match.tournament_uid)[0]
        round_name = search_in_database(rounds_database, 'round_uid', object_match.round_uid)[0]
        match_name = object_match.name
        match_lst.append({'player1': player1, 'player1_uid': object_match.player1,
                          'player2': player2, 'player2_uid': object_match.player2,
                          'tournament': tournament_name['name'],
                          'round': round_name['name'], 'match': match_name})
    return match_lst


def tournament_results(tournament_selection, players_database, tournaments_database,
                       rounds_database):
    """This function retreive all information needed to show the tournament results"""
    tournament_details = search_in_database(tournaments_database, 'tournament_uid',
                                            tournament_selection)[0]
    round_details = search_in_database(rounds_database, 'tournament_uid', tournament_selection)
    players_details = players_for_tournament(tournament_selection, players_database,
                                             tournaments_database)

    trnt_results = []
    for people in players_details:
        new_player = {}
        new_player['uid'] = people['uid']
        new_player['rk'] = people['ranking']
        new_player['Player'] = "{} {}".format(people['first_name'], people['last_name'])
        new_player['CTS'] = find_score_in_list(people['uid'], tournament_details['score'])

        for rnd in range(tournament_details['nb_round']):
            try:
                round_score = find_score_in_list(people['uid'], round_details[rnd]['score'])
                if round_score is None:
                    round_score = 'NP'
                new_player[round_details[rnd]['name']] = round_score
            except IndexError:
                new_player[f"Round{rnd+1}"] = 'NP'
        trnt_results.append(new_player)
    return trnt_results


def find_score_in_list(uid, scores_list):
    """This function find the score corresponding to a player uid"""
    score_value = float()
    for score in scores_list:
        if score[0] == uid:
            score_value = score[1]
    return score_value


def players_for_tournament(tournament_selection, players_database, tournaments_database):
    """This function retreive all players information for a tournament selected"""
    tournament_details = search_in_database(tournaments_database, 'tournament_uid',
                                            tournament_selection)[0]
    players_details_list = []
    for people in tournament_details['players_uid_lst']:
        player_details = search_in_database(players_database, 'uid', people)[0]
        players_details_list.append(player_details)
    return players_details_list


def is_the_round_finished(round_uid, tournaments_database, rounds_database, matchs_database):
    """This function return true if the round if finished, to start a new one"""
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
        update_tournament_score(round_object.tournament_uid, round_object.score,
                                tournaments_database)

    if round_finished:
        round_object.update_status(match_score_list)
        update_row_in_database(rounds_database, round_object, 'round_uid', round_uid)
        update_tournament_score(round_object.tournament_uid, round_object.score,
                                tournaments_database)

    return round_finished


def is_the_tournament_finised(tournament_uid):
    """This function return true if the tournament is finished"""
    players_database, tournaments_database, rounds_database, matchs_database = load_all_database()

    tournament_selected = search_in_database(tournaments_database, 'tournament_uid', tournament_uid)
    tournament_object = deserialized_tournament(tournament_selected)[0]
    round_list = search_in_database(rounds_database, 'tournament_uid', tournament_uid)#[0]['round_lst']
    tournament_finised = True

    if len(round_list) == tournament_object.nb_round:
        for elt in round_list:
            if elt['status'] != 'done':
                tournament_finised = False
    else:
        tournament_finised = False

    if tournament_finised:
        tournament_object.update_status()
        update_row_in_database(tournaments_database, tournament_object,
                               'tournament_uid', tournament_uid)
        
        view.show_menu([' !! TOURNAMENT IS FINISHED !! '], '***')
        trnt_results = tournament_results(tournament_uid, players_database,
                                                  tournaments_database, rounds_database)
        view.show_tournament_result(sorted_database(trnt_results, 'CTS', reverse=True))
        view.show_tournament_report_note()
        view.show_match_report_note()

    return tournament_finised


def is_process_continue(data_available):
    """

    This function return true, if the result of the previous function stocked in parameter
    is not empty

    """
    we_continue = True
    if data_available == []:
        we_continue = False
    return we_continue


def conditions_to_add_player(uid_available, uid_used, player_selection):
    """

    This method test 3 condictions to add player in the tournament :
        - Condition 1, It's not a new player
        - Condition 2, the player is not already in the tournament
        - Condition 3, the uid selected exist in the database

    """
    cond1_new_player = player_selection not in ['n', 'N']
    cond2_uid_used = player_selection in uid_used
    try:
        cond3_uid_available = int(player_selection) not in uid_available
    except ValueError:
        cond3_uid_available = player_selection not in uid_available

    return cond1_new_player and (cond2_uid_used or cond3_uid_available)


def deserialized_player(players_list):
    """This function transform a player dictionnary in a list of objects player"""
    deserialized_lst = []
    for people in players_list:
        deserialized_lst.append(player.Player(people['first_name'], people['last_name'],
                                              people['birth_date'], people['gender'],
                                              people['ranking'], people['uid']))
    return deserialized_lst


def deserialized_tournament(tournament_list):
    """This function transform a tournament dictionnary in a list of objects tournament"""
    deserialized_lst = []
    for trnt in tournament_list:
        deserialized_trnt = tournament.Tournament(trnt['name'], trnt['tournament_uid'], trnt['time_control'])
        deserialized_trnt.players_uid_lst = trnt['players_uid_lst']
        deserialized_trnt.score = trnt['score']
        deserialized_trnt.creation_date = trnt['creation_date']
        deserialized_trnt.end_date = trnt['end_date']
        deserialized_trnt.status = trnt['status']
        deserialized_trnt.round_lst = trnt['round_lst']
        deserialized_trnt.nb_round = trnt['nb_round']
        deserialized_lst.append(deserialized_trnt)
    return deserialized_lst


def deserialized_round(round_list):
    """This function transform a round dictionnary in a list of objects round"""
    deserialized_lst = []
    for one_round in round_list:
        deserialized_rnd = roundo.Round(one_round['name'], one_round['players_lst'],
                                        one_round['tournament_uid'], one_round['round_uid'])
        deserialized_rnd.matchs_lst = one_round['matchs_lst']
        deserialized_rnd.score = one_round['score']
        deserialized_rnd.start_date = one_round['start_date']
        deserialized_rnd.start_hour = one_round['start_hour']
        deserialized_rnd.end_date = one_round['end_date']
        deserialized_rnd.end_hour = one_round['end_hour']
        deserialized_rnd.status = one_round['status']
        deserialized_lst.append(deserialized_rnd)
    return deserialized_lst


def deserialized_match(match_list):
    """This function transform a match dictionnary in a list of objects match"""
    deserialized_lst = []
    for mch in match_list:
        deserialized_mch = match.Match(mch['name'], mch['player1'], mch['player2'],
                                       mch['tournament_uid'], mch['round_uid'], mch['match_uid'])
        deserialized_mch.score = mch['score']
        deserialized_mch.status = mch['status']
        deserialized_lst.append(deserialized_mch)
    return deserialized_lst


def menu_function(menu):
    """This function manage the input of the user regarding his choice in the menu"""
    menu_value = menu[0]
    under_menu_value = menu[1]

    players_database, tournaments_database, rounds_database, matchs_database = load_all_database()

    if menu_value == "add new player":
        controller.menu_new_player(players_database)

    if menu_value == "create tournament":
        controller.menu_new_tournament(players_database, tournaments_database)

    if menu_value == "show all players list":
        controller.menu_show_all_players_list(under_menu_value, players_database)

    if menu_value == "show players list of a tournament":
        controller.menu_show_players_list_for_tournament(under_menu_value, players_database, tournaments_database)

    if menu_value == "show tournaments list":
        controller.menu_show_tournaments_list(under_menu_value, tournaments_database)

    if menu_value == "show round list":
        controller.menu_show_round_list(tournaments_database, rounds_database)

    if menu_value == "show match list":
        controller.menu_show_match_list()

    if menu_value == "launch/continue tournament":
        controller.menu_launch_tournament()

    if menu_value == "input match result":
        controller.menu_input_match_result()

    if menu_value == "update player ranking":
        controller.menu_update_player_ranking(under_menu_value, players_database)

    if menu_value == "show tournament's results":
        controller.menu_show_tournaments_results()
    return exit_menu(menu_value)


def exit_menu(menu_value):
    """Function that return True if the user seleted exit in the menu, false otherwise"""
    exit_menu_bool = False
    if menu_value == "exit":
        exit_menu_bool = True
    return exit_menu_bool
