# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:41:34 2021

@author: Amelie Noury
"""
import controller


#############################################################
#                                                           #
#          PLEASE DO CTRL F5 TO LAUNCH THE PROGRAMM         #
#                                                           #
#############################################################

if __name__ == "__main__":

    # si fichier ouvert : os.close(29)
    SHOW_MENU = True
    while SHOW_MENU:
        SHOW_MENU = controller.run_menu()
