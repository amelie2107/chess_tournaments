# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:05:03 2021

@author: Amelie Noury
"""
from datetime import datetime
import view
import model
import player
import tournament

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

TIME_CONTROL = ["bullet", "blitz", "speed"]


def run_menu():
    """
    Parameters
    ----------
    players_database : TinyDB database, contain the players information
    tournaments_database : TinyDB database, contain the tournaments information
    rounds_database : TinyDB database, contain the rounds information
    matchs_database : TinyDB database, contain the matchs information

    Returns
    -------
    This function launch and show the menu, it return True to show the menu again
    and false to exit the program

    """
    players_database, tournaments_database, rounds_database, matchs_database = model.load_all_database()

    view.show_menu(MENU_LIST, "menu")
    error_selection = True
    while error_selection:
        menu_selection = menu_return_selection()
        if menu_selection < len(MENU_LIST):
            error_selection = False
        else:
            print("ERROR : The entrance is not conform")

    menu_under_selection = None

    if MENU_LIST[menu_selection] in SHOW_PLAYERS:
        view.show_menu(PLAYER_LIST_MENU, "menu")
        error_under_selection = True
        while error_under_selection:
            under_menu_selection = menu_return_selection()
            if under_menu_selection not in range(0,len(PLAYER_LIST_MENU)):
                error_under_selection = True
                print("ERROR : The entrance is not conform")
            else:
                error_under_selection = False        
        menu_under_selection = PLAYER_LIST_MENU[under_menu_selection]

    if MENU_LIST[menu_selection] == "show tournaments list":
        view.show_menu(SHOW_LIST_MENU, "menu")
        error_under_selection = True
        while error_under_selection:
            under_menu_selection = menu_return_selection()
            if under_menu_selection not in range(0,len(SHOW_LIST_MENU)):
                error_under_selection = True
                print("ERROR : The entrance is not conform")
            else:
                error_under_selection = False        
        menu_under_selection = SHOW_LIST_MENU[menu_return_selection()]

    exit_menu = model.menu_function([MENU_LIST[menu_selection], menu_under_selection])
    if not exit_menu:
        input('\n ****************** press entry to continue ******************')
    return not exit_menu


def menu_return_selection(target='index'):
    """This function return a user selection regarding the menu"""
    input_no_error = True
    while input_no_error:
        try:
            input_no_error = False
            return int(input("please enter your choice ("+target+") : "))
        except ValueError:
            input_no_error = True
            print("ERROR : The entrance is not conform")


def database_return_selection(object_name='object', object_action='launch'):
    """This function return a user selection regarding the database"""
    input_no_error = True
    while input_no_error:
        try:
            input_no_error = False
            return int(input(f"select the {object_name} uid you want to {object_action} : "))
        except ValueError:
            input_no_error = True
            print("ERROR : The entrance is not conform")


# 0
def menu_new_player(players_database):
    """
    Parameters
    ----------
    players_database : TinyDB, the players database

    Returns
    -------
    This function add a new player in the database

    """
    new_one = new_player(players_database)
    return model.insert_row_in_database(players_database, new_one.serialized())


# 1
def menu_new_tournament(players_database, tournaments_database):
    """

    Parameters
    ----------
    players_database : TinyDB, the players database
    tournaments_database : TinyDB, the tournaments database

    Returns
    -------
    This function add a new tournament in the database

    """
    new_one = new_tournament(tournaments_database)
    players_list = model.read_database(players_database, 'order by name')
    view.show_all_players_list(players_list)
    new_one.add_players_in_tournament(players_list, players_database)
    model.insert_row_in_database(tournaments_database, new_one.serialized())


# 2
def menu_show_all_players_list(order_by_selection, players_database):
    """

    Parameters
    ----------
    order_by_selection : string, the user selection to sort the players, by Name or by ranking
    players_database : TinyDB, the players database

    Returns
    -------
    The function show the full list of players

    """
    players_list = model.read_database(players_database, order_by_selection)
    view.show_all_players_list(players_list)


# 3
def menu_show_players_list_for_tournament(order_by_selection, players_database, tournaments_database):
    """

    Parameters
    ----------
    players_database : TinyDB, the players database
    tournaments_database : TinyDB, the tournaments database

    Returns
    -------
    And return the list of players for a selected tournament

    """
    view.show_tournament_selection(tournaments_database)
    error_selection = True
    while error_selection:
        tournament_selection = database_return_selection('tournament', 'see')
        if tournament_selection in model.field_in_database(tournaments_database, 'tournament_uid'):
            error_selection = False
        else:
            print("ERROR : The entrance is not conform")

    players_list = model.players_for_tournament(tournament_selection, players_database,
                                                tournaments_database)
    order_by_lst = 'last_name'
    order_by_next = 'first_name'
    if order_by_selection == 'order by ranking':
        order_by_lst = 'ranking'
        order_by_next = 'last_name'
    view.show_player_selection(model.sorted_database(players_list, order_by_lst, order_by_next))


# 4
def menu_show_tournaments_list(selected_field, tournaments_database):
    """

    Parameters
    ----------
    selected_field : string, the user selection regarding the progression
    of the tournament to filter the display
    tournaments_database : TinyDB, the tournaments database

    Returns
    -------
    Show the list of all tournament database filtred

    """
    if selected_field == 'all':
        tournament_table_selection = model.read_database(tournaments_database)
    else:
        tournament_table_selection = model.search_in_database(tournaments_database,
                                                              'status', selected_field)
    view.show_tournament_selection(tournament_table_selection)


# 5
def menu_show_round_list(tournaments_database, rounds_database):
    """

    Parameters
    ----------
    tournaments_database : TinyDB, the tournaments database
    rounds_database : TinyDB, the rounds database

    Returns
    -------
    This function show the rounds list of the selected tournament
    This function return True if a round list exist for the selected tournament, false otherwise

    """
    menu_show_tournaments_list('all', tournaments_database)
    error_selection = True
    while error_selection:
        tournament_selection = database_return_selection('tournament', 'see')
        if tournament_selection in model.field_in_database(tournaments_database, 'tournament_uid'):
            error_selection = False
        else:
            print("ERROR : The entrance is not conform")

    selection_to_show = model.search_in_database(rounds_database, 'tournament_uid',
                                                 tournament_selection)
    view.show_round_selection(selection_to_show)
    return model.is_process_continue(selection_to_show)


# 6
def menu_show_match_list():
    """

    Parameters
    ----------
    players_database : TinyDB, the players database
    tournaments_database : TinyDB, the tournaments database
    rounds_database : TinyDB, the rounds database
    matchs_database : TinyDB, the tournaments database

    Returns
    -------
    The function show the matchs list of a selected tournament and round

    """
    players_database, tournaments_database, rounds_database, matchs_database = model.load_all_database()
    is_available = menu_show_round_list(tournaments_database, rounds_database)
    if is_available:
        error_selection = True
        while error_selection:
            round_selection = database_return_selection('round', 'see')
            if round_selection in model.field_in_database(rounds_database, 'round_uid'):
                error_selection = False
            else:
                print("ERROR : The entrance is not conform")
        
        change_score = 'y'
        if model.search_in_database(rounds_database, 'round_uid', round_selection)[0]['status'] == 'done':
            change_score = input(' This round is finished, do you want to change a score (y/n)? ')
        if change_score.lower() == 'y':
            selection_to_show = model.search_match_in_database(matchs_database,[round_selection])
            match_object = model.deserialized_match(selection_to_show)
            match_list = model.match_details(match_object, players_database, tournaments_database,
                                             rounds_database)
            view.show_match_details(selection_to_show, match_list)
            view.show_match_report_note()
            process_continue = model.is_process_continue(selection_to_show)
        else:
            process_continue = False
    else:
        view.show_list("The round selected is not yet started")
        process_continue = False
    return process_continue


# 7
def menu_launch_tournament():
    """

    Parameters
    ----------
    players_database : TinyDB, the players database
    tournaments_database : TinyDB, the tournaments database
    rounds_database : TinyDB, the rounds database
    matchs_database : TinyDB, the tournaments database

    Returns
    -------
    This function allow to the players to launch a tournament or continue a tournament,
    that means a new round and the corresponding matchs are created for the selected tournament
    and all the database concerned are updated

    """
    players_database, tournaments_database, rounds_database, matchs_database = model.load_all_database()
    menu_show_tournaments_list('all', tournaments_database)
    error_selection = True
    while error_selection:
        tournament_selection = database_return_selection('tournament')
        if tournament_selection in model.field_in_database(tournaments_database, 'tournament_uid'):
            error_selection = False
        else:
            print("ERROR : The entrance is not conform")

    tournament_selected = model.search_in_database(tournaments_database, 'tournament_uid',
                                                   tournament_selection)
    tournament_object = model.deserialized_tournament(tournament_selected)[0]
    tournament_object.start_round(players_database, rounds_database, matchs_database)
    model.update_row_in_database(tournaments_database, tournament_object, 'tournament_uid',
                                 tournament_object.tournament_uid)
    try:
        tournament_object.round_lst[-1]
        show_match_in_progress = True
    except:
        print("No match are defined")
        show_match_in_progress = False
        
    if show_match_in_progress:
        match_selected = model.search_in_database(matchs_database, 'round_uid', tournament_object.round_lst[-1])
        match_object = model.deserialized_match(match_selected)
        match_details_dict = model.match_details(match_object, players_database,
                                                 tournaments_database, rounds_database)
        view.show_match_details(match_selected, match_details_dict)

# 8
def menu_input_match_result():
    """

    Parameters
    ----------
    players_database : TinyDB, the players database
    tournaments_database : TinyDB, the tournaments database
    rounds_database : TinyDB, the rounds database
    matchs_database : TinyDB, the tournaments database

    Returns
    -------
    This function show the detail of a match and invite the user to input the results of the matchs.
    Results are convert 0 for the looser, 0.5 for draw and 1 for the winner,
    the status of the match is updated
    Databases concerned are updated.

    """
    players_database, tournaments_database, rounds_database, matchs_database = model.load_all_database()

    is_available = menu_show_match_list()
    if is_available:
        error_selection = True
        while error_selection:
            match_selection = database_return_selection('match', 'update')
            if match_selection in model.field_in_database(matchs_database, 'match_uid'):
                error_selection = False
            else:
                print("ERROR : The entrance is not conform")

        match_selected = model.search_in_database(matchs_database, 'match_uid', match_selection)
        match_object = model.deserialized_match(match_selected)[0]
        
        change_score = 'y'
        if match_object.status == 'done':
            print("")
            view.show_list(' !! This match is finished !! ')
            change_score = input("Do you want to change the score (y/n)?")
        if change_score.lower() == 'y':
            match_details_dict = model.match_details([match_object], players_database,
                                                     tournaments_database, rounds_database)[0]
            match_score = input_match_scores(match_details_dict)
            match_object.update_score(match_score)
            model.update_row_in_database(matchs_database, match_object, 'match_uid',
                                         match_object.match_uid)
            model.is_the_round_finished(match_object.round_uid, tournaments_database, rounds_database,
                                        matchs_database)
            model.is_the_tournament_finised(match_object.tournament_uid)


# 9
def menu_update_player_ranking(player_list_menu, players_database):
    """

    Parameters
    ----------
    PLAYER_LIST_MENU : list of string, menu to sort the player by name or ranking
    players_database : TinyDB, players database

    Returns
    -------
    The user can choose the player by entring his uid
    and than enter the new ranking of the player.
    The function confirm the change

    """
    # Show the players list to select one
    menu_show_all_players_list(player_list_menu, players_database)
    player_selection, new_rank_selection = input_player_rank(players_database)
    # Update the rank of the player selected
    player_selected = model.search_in_database(players_database, 'uid', player_selection)
    player_object = model.deserialized_player(player_selected)[0]
    view.show_update_player_rank(player_object.first_name, player_object.last_name,
                                 player_object.ranking, new_rank_selection)
    print(player_object.uid)
    print(player_object.ranking)
    model.update_row_in_database(players_database, player_object, 'uid', player_object.uid)


# 10
def menu_show_tournaments_results():
    """

    Parameters
    ----------
    players_database : TinyDB, the players database
    tournaments_database : TinyDB, the tournaments database
    rounds_database : TinyDB, the rounds database

    Returns
    -------
    This function show the full results of a selected tournament.

    """
    players_database, tournaments_database, rounds_database, matchs_database = model.load_all_database()

    menu_show_tournaments_list('all', tournaments_database)
    error_selection = True
    while error_selection:
        tournament_selection = database_return_selection('tournament', 'see results')
        if tournament_selection in model.field_in_database(tournaments_database, 'tournament_uid'):
            error_selection = False
        else:
            print("ERROR : The entrance is not conform")

    trnt_results = model.tournament_results(tournament_selection, players_database,
                                                  tournaments_database, rounds_database)
    view.show_tournament_result(model.sorted_database(trnt_results, 'CTS', reverse=True))
    view.show_tournament_report_note()
    view.show_match_report_note()


def new_player(players_database):
    """ This function return a player from input """
    print("\n *********Add information about the new player**************")
    first_name = input("First name : ")
    last_name = input("Last name : ")

    bith_date_error = True
    while bith_date_error:
        birth_date = input("Date of birth(dd/mm/yyyy) : ")
        try:
            datetime.strptime(birth_date, "%d/%m/%Y")
            bith_date_error = False
        except ValueError:
            print("ERROR : the entrance is not correct")

    gender_error = True
    while gender_error:
        gender = input("Gender (F/M) : ")
        if gender.upper() in ("F", "M"):
            gender_error = False
        else:
            print("ERROR : the entrance is not correct")
    ranking = 0
    unique_id = model.generate_uniqueid(players_database)
    return player.Player(first_name.capitalize(), last_name.capitalize(), birth_date,
                         gender, ranking, unique_id)


def new_tournament(tournaments_database):
    """ This function return a tournament from input """
    print("\n ********* Add information about the new tournament **************")
    tournament_name = input("Please, choose a name for this new tournament : ")
    unique_id = model.generate_uniqueid(tournaments_database, 'tournament_uid')
    view.show_menu(TIME_CONTROL, " choose a chess speed mode ")
    time_error = True
    while time_error:
        try:
            time_control = int(input("Please, choose a chess speed mode : "))
            if time_control in range(0, len(TIME_CONTROL)):
                time_error = False
            else:
                print("ERROR : the entrance is not correct")
        except ValueError:
            print("ERROR : the entrance is not correct")

    return tournament.Tournament(tournament_name, int(unique_id), TIME_CONTROL[time_control])


def input_match_scores(match_dict):
    """

    This function ask to the user the score of the players for a match in parameter
    and return a list of tuple with, for each, the player uid and his score

    """
    print("\n you have selected : \n   * the tournament : {}, \
          \n   * the round : {}, \n   * the match : {}".format(match_dict['tournament'],
          match_dict['round'], match_dict['match']))
    print("   * Currently {} is playing against {}".format(match_dict['player1'],
                                                           match_dict['player2']))
    score_error = True
    while score_error:
        try:
            player1_score = input('Enter the score of {} : '.format(match_dict['player1']))
            player2_score = input('Enter the score of {} : '.format(match_dict['player2']))
            int(player1_score)
            int(player2_score)
            score_error = False
        except ValueError:
            print("ERROR : the entrance is not correct")
    return [(match_dict['player1_uid'], player1_score), (match_dict['player2_uid'], player2_score)]


def input_player_rank(players_database):
    """

    This function ask to the user the new ranking of a player
    and return the player uid and his new ranking

    """
    error_selection = True
    while error_selection:
        player_selection = input("select the uid of the player for " +
                                 "who you want to update the ranking : ")
        try:
            if int(player_selection) in model.field_in_database(players_database, 'uid'):
                error_selection = False
            else:
                print("ERROR : The entrance is not conform")
        except ValueError:
            print("ERROR : The entrance is not conform")

    ranking_error = True
    while ranking_error:
        try:
            new_rank_selection = input("Please, insert the new ranking of this player : ")
            int(new_rank_selection)
            ranking_error = False
        except ValueError:
            print("ERROR : the entrance is not correct")

    return int(player_selection), int(new_rank_selection)
