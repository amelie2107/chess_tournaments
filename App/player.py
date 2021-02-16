# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from slugify import slugify


class Player:
    """

    This class allow to create a player with many information in parameters.
    Parameters are first name, last name, date of birth, gender, ranking, uid

    """

    def __init__(self, first_name, last_name, birth_date,
                 gender, ranking, uid):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.ranking = ranking
        self.uid = uid

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    def serialized(self):
        """Transform the object in dictionary to save it it the database"""
        self.birth_date = slugify(self.birth_date)
        return self.__dict__
