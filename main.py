# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:41:34 2021

@author: arnau
"""
import Controller
import Model


if __name__ == "__main__":
    
    # si fichier ouvert : os.close(29)
    clear = False
    players_database = Model.database_load('chess_players_database.json', 'players')
    tournaments_database = Model.database_load('chess_tournaments_database.json', 'tournaments',clear)
    rounds_database = Model.database_load('chess_rounds_database.json','rounds', clear)
    matchs_database = Model.database_load('chess_matchs_database.json','matchs', clear)

    continue_admin = True
    while continue_admin:    
        continue_admin = Controller.run_menu(players_database, tournaments_database, rounds_database, matchs_database)

        