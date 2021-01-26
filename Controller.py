# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:05:03 2021

@author: arnau
"""

class Controller:
    def __init__(self, match, view):
        #Model
        self.players = []
        self.match = match
        #view
        #self.view = 
        
    def run(self):
        while len(self.players) < 8:
            #ask a view for the name of the next player
            new_player = self.view.prompt_for_new_player()
            if new_player is None:
                break
            self.add_player(new_player)
        self.start_game()
        for player in self.players:
            self.view.show_player_and_game (player.name, player.game)
        
        self.view.prompt_for_play_turn()
            for player in self.players:
                for pawn in player.game:
                    pawn.move = True
                self.view.show_player_and_game(player.name, player.game)
    
    def evaluate_game(self):
        best_player = None
        
        return best_player.name
        
    def start_game(self):
        pass
    
    def rebuild_game(self):
        pass