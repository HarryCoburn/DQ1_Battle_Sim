"""
battle.py - Battle code for DQ1 sim. Holds both player and enemy code.
"""

import random
import tkinter as tk
from ..common.messages import EnemyActions

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

    def enemy_turn(self):
            # Do a combat action
            self.perform_enemy_action()

    def perform_enemy_action(self):
        """Selects and performs an action from the enemy's set of possible actions."""
        action_methods = {
            EnemyActions.ATTACK: self.enemy_attack,
            EnemyActions.HURT: lambda: self.enemy_casts_hurt(False),
            EnemyActions.HURTMORE: lambda: self.enemy_casts_hurt(True),
            EnemyActions.HEAL: lambda: self.enemy_casts_heal(False),
            EnemyActions.HEALMORE: lambda: self.enemy_casts_heal(True),
            EnemyActions.SLEEP: self.enemy_casts_sleep,
            EnemyActions.STOPSPELL: self.enemy_casts_stopspell,
            EnemyActions.FIRE: lambda: self.enemy_breathes_fire(False),
            EnemyActions.STRONGFIRE: lambda: self.enemy_breathes_fire(True)
        }

        chosen_attack = self.enemy_choose_attack()
        action = action_methods.get(chosen_attack, self.handle_unknown_action)
        action()

    def handle_unknown_action(self):
        """ Handles unknown enemy actions """
        raise NotImplementedError("Enemy tried to attack with something not programmed yet!!")



    def enemy_choose_attack(self):
        atk_list = self.model.enemy.pattern
        choice = None
        for item in atk_list:
            chance = item["weight"]
            if random.randint(1, 100) <= chance:
                action = item["id"]
                if action in [EnemyActions.ATTACK, EnemyActions.HURT, EnemyActions.FIRE, EnemyActions.HURTMORE, EnemyActions.STRONGFIRE]:
                    choice = action
                    break
                if action in [EnemyActions.HEAL, EnemyActions.HEALMORE] and self.enemy.trigger_healing():
                    choice = action
                    break
                if action == EnemyActions.SLEEP and not self.model.player.is_asleep:
                    choice = action
                    break
                if action == EnemyActions.STOPSPELL and not self.model.player.is_spellstopped:
                    choice = action
                    break

        return choice or EnemyActions.ATTACK

    def end_fight(self):
        """Triggers the flag that tells the controller battle is over"""
        self.fight_over.set(True)

    def is_player_defeated(self):
        if self.model.player.is_defeated():
            self.model.text(f"You have been defeated by the {self.enemy.name}!\n")
            self.end_fight()
        else:
            self.player_turn()

  
    def enemy_attack(self):
        """Enemy attacks normally"""
        self.model.text(f"\nEnemy turn\n")
        enemy_damage_dealt = self.enemy.attack(self.player.defense())
        self.model.player.current_hp -= enemy_damage_dealt
        self.controller.update_player_info()

        self.model.text(f"{self.model.enemy.name} attacks! {self.model.enemy.name} hits you for {enemy_damage_dealt} damage.\n")
        self.is_player_defeated()

    def enemy_casts_hurt(self, more):
        """ Enemy handling of hurt and hurtmore"""
        spell_name = "Hurtmore" if more else "Hurt"
        if self.enemy.is_spell_stopped(spell_name):
            self.player_turn()

        hurt_high = [3, 10]
        hurt_low = [2, 6]
        hurtmore_high = [30, 45]
        hurtmore_low = [20, 30]

        mag_def = self.model.player.reduce_hurt_damage
        hurt_dmg = 0

        if mag_def and more:
            hurt_dmg = random.randint(hurtmore_low[0], hurtmore_low[1])
        elif mag_def and not more:
            hurt_dmg = random.randint(hurt_low[0], hurt_low[1])
        elif more:
            hurt_dmg = random.randint(hurtmore_high[0], hurtmore_high[1])
        else:
            hurt_dmg = random.randint(hurt_high[0], hurt_high[1])

        self.model.player.current_hp -= hurt_dmg
        self.model.text(f"""The {self.model.enemy.name} casts {spell_name}! {self.model.player.name} is hurt for {hurt_dmg} damage!""")
        self.is_player_defeated()

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

    def enemy_breathes_fire(self, more):
        """ Enemy handling of breath attacks"""
        spell_name = "strong flames at you!" if more else "fire"
        if self.model.enemy.enemy_spell_stopped:
            self.model.text(f"""The {self.model.enemy.name} casts {spell_name}, but their spell has been blocked!""")

        fire_high = [16, 23]
        fire_low = [10, 14]
        strongfire_high = [65, 72]
        strongfire_low = [42, 48]

        fire_def = self.model.player.reduce_fire_damage
        fire_dmg = 0

        if fire_def and more:
            fire_dmg = random.randint(strongfire_low[0], strongfire_low[1])
        elif fire_def and not more:
            fire_dmg = random.randint(fire_low[0], fire_low[1])
        elif more:
            fire_dmg = random.randint(strongfire_high[0], strongfire_high[1])
        else:
            fire_dmg = random.randint(fire_high[0], fire_high[1])

        self.model.player.current_hp -= fire_dmg
        self.model.text(f"""The {self.model.enemy.name} breathes {spell_name}! {self.model.player.name} is hurt for {fire_dmg} damage!""")
        self.is_player_defeated()
