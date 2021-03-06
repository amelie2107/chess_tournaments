# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:39:28 2021

@author: Amelie Noury
"""


class Match:

    """

    This class represent a match between two players
    This class return a list of two tuple in the attribut score
    Each tuple contain a player instance and a score
    The winner has 1 point
    The loser has 0 point
    If it's a draw match the score is 0.5 for each player

    """
    def __init__(self, name, player1, player2, tournament_uid, round_uid, uid):
        self.name = name
        self.player1 = player1
        self.player2 = player2
        self.score = []
        self.tournament_uid = tournament_uid
        self.round_uid = round_uid
        self.match_uid = uid
        self.status = 'in progress'

    def update_score(self, scores):
        """

        Parameters
        ----------
        scores : a list of 2 tuples, each tuple contain
        the player uid and his score

        Returns
        -------
        transform the score in 0/0.5/1 point and update the attribut score
        and the status of the match

        """
        if scores[0][0] == self.player1:
            score1 = scores[0][1]
            score2 = scores[1][1]
        if scores[0][0] == self.player2:
            score1 = scores[1][1]
            score2 = scores[0][1]

        confirmed = 'y'
        if score1 + score2 == 0:
            confirmed = input("are you sure the score for " +
                              "both players is zero (y/n)?")

        if confirmed.lower() == 'y':
            if score1 > score2:
                score1 = 1
                score2 = 0
            if score1 < score2:
                score1 = 0
                score2 = 1
            if score1 == score2:
                score1 = score2 = 0.5
            # self.score = [(self.player1, score1), (self.player2, score2)]
            self.score = [(self.player1, score1), (self.player2, score2)]
            self.status = 'done'

    def serialized(self):
        """Transform the object in dictionary to save it it the database"""
        return self.__dict__
