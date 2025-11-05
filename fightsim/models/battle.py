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

    def enemy_casts_heal(self, more):
        """ Enemy handling of heal and healmore"""
        spell_name = "Healmore" if more else "Heal"
        if self.model.enemy.enemy_spell_stopped:
            self.model.text(f"""The {self.model.enemy.name} casts {spell_name}, but their spell has been blocked!""")
            return

        heal_range = [20, 27]
        healmore_range = [85, 100]

        heal_max = self.model.enemy.max_hp - self.model.enemy.current_hp

        heal_rand = random.randint(healmore_range[0], healmore_range[1]) if more else random.randint(heal_range[0],
                                                                                                     heal_range[1])

        heal_amt = heal_rand if heal_rand < heal_max else heal_max

        self.model.enemy.current_hp += heal_amt
        self.model.text(f"""The {self.model.enemy["name"]} casts {spell_name}! {self.model.enemy["name"]} is healed {heal_amt} hit points!""")
        self.controller.update_enemy_info()
        self.player_turn()

    def enemy_casts_sleep(self):
        """Enemy attempts to cast sleep"""
        spell_name = "Sleep"
        if self.model.enemy.enemy_spell_stopped:
            self.model.text(f"""The {self.model.enemy.name} casts {spell_name}, but their spell has been blocked!""")
        else:
            self.model.player.is_asleep = True
            self.model.text(f"""The {self.model.enemy.name} casts {spell_name}. You fall asleep!!""")
        self.player_turn()

    def enemy_casts_stopspell(self):
        """ Enemy attempts to cast stopspell. 50% chance of failure"""
        spell_name = "Stopspell"
        if self.model.enemy.enemy_spell_stopped:
            self.model.text(f"The {self.model.enemy.name} casts {spell_name}, but their spell has been blocked!")
        elif random.randint(1, 2) == 2:
            self.model.player.is_spellstopped = True
            self.model.text(f"""The {self.model.enemy.name} casts {spell_name}! Your magic has been blocked!""")
        else:
            self.model.text(f"""The {self.model.enemy.name} casts {spell_name}, but the spell fails!""")
        self.player_turn()