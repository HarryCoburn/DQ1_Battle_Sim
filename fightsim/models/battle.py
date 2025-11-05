"""
battle.py - Battle code for DQ1 sim. Holds both player and enemy code.
"""

import random
import tkinter as tk


class BattleEngine:
    """
    Main battle controller
    """

    def __init__(self, main_controller):
        self.controller = main_controller
        self.model = self.controller.model      
        self.player = self.model.player
        self.enemy = self.model.enemy
        self.fight_over = tk.BooleanVar()
        self.fight_over.set(False)

    def end_fight(self):
        """Triggers the flag that tells the controller battle is over"""
        self.fight_over.set(True)
        
   