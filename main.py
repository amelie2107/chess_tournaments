# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:41:34 2021

@author: arnau
"""
import Player
import Match
import os
from tinydb import TinyDB, Query, where
import numpy
import pandas

# #creer une instance
# player = Player(name='John', age=22)
# #serialiser une instance
# serialized_player = {'name': player.name, 'age': player.age}
# #reconvertir une instance serialisé
# name = serialized_player['name']
# age = serialized_player['age']
# player = Player(name=name, age=age)


def new_player():
    print("*********Add information about the new player**************")
    first_name = input("First name : ")
    last_name = input("Last name : ")
    birth_date = input("Date of birth : ")
    gender = input("Gender (F/M) : ")
    ranking = 0
    return Player.Player(first_name, last_name, birth_date, gender, ranking)

def deserialized(players_list):
    deserialized_player = []
    for player in players_list:
        deserialized_player.append(Player.Player(player['first_name'], player['last_name'], player['birth_date'], player['gender'], player['ranking']))
    return deserialized_player

def view_all_players(lst_players, order_by='last_name'):
     for player in sorted(lst_players.items(), key = order_by):
         print(player)
         
def select_players_list(serialized_players, nb_player, tournament_name):
    print(f"**********choose your {nb_player} players to start a new tournament*************")
    players_tournament = []
    all_players = list(serialized_players)
    #all_players_report = pandas.DataFrame.from_dict(serialized_players)
    while len(players_tournament) < nb_player:
        print("Select a new player for the tournament : {}".format(tournament_name))
        print(pandas.DataFrame.from_dict(all_players))
        player_selection = input("Select the index of the player or 'N' for a new player : ")
        if player_selection.upper() == 'N':
            player = new_player()
            players_tournament.append(player.serialized())
            players_table.insert(player.serialized())
        else:
            try:
                players_tournament = all_players[int(player_selection)]
                del all_players[int(player_selection)]
            except IndexError:
                print("They is no players corresponding to your entrance")
            except NameError:
                print("You entrance is not conform.")
    return players_tournament
 
"""
Pour sauvegarder plusieurs joueurs en utilisant TinyDB, 
tu dois d'abord sérialiser toutes les instances de joueurs, 
puis les charger dans la table des joueurs comme ceci :
"""

if __name__ == "__main__":
    Amelie = Player.Player(first_name='Amelie', last_name = 'Noury', birth_date = '21/07/1987', gender = 'F', ranking = 0)
    
    
    add_player = True
    new_player_lst = []
    while add_player:
        player = new_player()
        new_player_lst.append(player.serialized())
        another_player = input("Do you want to add another player (y/n)?")
        if another_player.lower() != 'y':
            add_player = False
        

#    if not os.path.isfile('chess_players_database.json'):
    #create the database
    db = TinyDB('chess_players_database.json')    
    players_table = db.table('players')
    players_table.truncate()	# clear the table first
    players_table.insert_multiple(new_player_lst)
    
    
    #select 8 players to start a new Tournament
    tournament_name = input("Enter a name for this new tournament : ")
       #view_all_players(deserialized_players)
    serialized_players = players_table.all()
    tournament_players = select_players_list(serialized_players, 8, tournament_name)
0
# 
# 
# 
# players_table.insert_multiple(serialized_players)


# #charger les joueurs
# serialized_players = players_table.all()

# #Model controller view
# match = match()
# view = view()

# game_controller = controller(match, view)
# game_controller.run
