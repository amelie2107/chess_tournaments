# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:29:13 2021

@author: arnau
"""

class View:
    
    def __init__(self):
        pass
    
    def prompt_for_new_player(self):
        new_player = input("Type the name of the player : ")
            if new_player = "":
                return None
            return new_player
        
    def show_player_and_game(self, player_name, play_game):
        print("[{}]".format(player_name))
        print("[{}]".format(player_game))
        
    def show_winner(self, winner_name):
        print("")
        print("Congratulation {} !".format(winner_name))
        
    def prompt_for_new_game(self):
        print("")
        while True:
            prompt = input("play again (y/n)?")
            if prompt.lower() == 'y'
                return True
            else:
                return False
        
        