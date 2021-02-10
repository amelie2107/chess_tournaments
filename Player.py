# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from slugify import slugify

class Player:
    """
    This class is a database of players
    Parameters are first name, last name, date of birth, gender and ranking
    """
    
    def __init__(self, first_name, last_name, birth_date, gender, ranking, uid):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.ranking = ranking
        self.uid = uid
        
    def __repr__(self):
        if self.gender == 'F':
            title = "Miss."
        if self.gender == 'M':
            title = "Mr."
        return (f"{title} {self.first_name} {self.last_name} born the {self.birth_date} is ranked : {self.ranking}")
    
    def __str__(self):
        if self.gender == 'F':
            title = "Miss."
        if self.gender == 'M':
            title = "Mr."
        return (f"{title} {self.first_name} {self.last_name} born the {self.birth_date} is ranked : {self.ranking}")

    
    def serialized(self):
        self.birth_date  = slugify(self.birth_date)
        return self.__dict__
    
    
         
        
        
        
        
        
# Amelie = Player(first_name='Amelie', last_name = 'Noury', birth_date = '21/07/1987', gender = 'F', ranking = 0)
# Amelie.view() 
# serialized_Amelie = Amelie.serialized()
