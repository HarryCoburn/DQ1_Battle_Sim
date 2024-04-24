"""
battle.py - Battle code for DQ1 sim. Holds both player and enemy code.
"""

import random
import tkinter as tk
from ..common.messages import EnemyActions
from ..common.randomizer import Randomizer


class Battle:
    """
    Main battle controller
    """

    def __init__(self, main_controller):
        self.controller = main_controller
        self.model = self.controller.model
        self.view = self.controller.view
        self.player = None
        self.enemy = None
        self.fight_over = tk.BooleanVar()
        self.fight_over.set(False)
        self.herb_range = (23, 30)

    # Core Fight Routines

    def setup_battle(self):
        """Performs setup tasks for the battle prior to start"""
        self.player = self.model.player
        self.enemy = self.model.enemy
        self.controller.prepare_battle()
        self.start_fight()

    def start_fight(self):
        """Starts the battle loop"""
        self.controller.start_battle_interaction()
        surprise_check = self.does_enemy_surprise()
        self.first_turn(surprise_check)

    def first_turn(self, enemy_surprises):
        """ Determines the first turn. """
        if enemy_surprises:
            self.controller.player_surprised()
            self.enemy_turn()
        else:
            self.player_turn()

    def does_enemy_surprise(self):
        """ Determine if the enemy surprises the player based on agility and randomness. """
        player_roll = Randomizer.agility_roll(self.player.agility)
        enemy_roll = Randomizer.agility_roll(self.enemy.agility, surprise_factor=0.25)
        return player_roll < enemy_roll

    # Player Actions

    def player_turn(self):
        """Runs at the start of player turn. Checks for sleep status and updates it, then waits for user to
        enter a command."""
        if self.player.check_sleep():  # If the player is asleep, switch to the enemy's turn.
            self.enemy_turn()

    def is_enemy_defeated(self):
        """ Checks if the enemy is defeated. Ends fight if true. Starts enemy turn if false. """
        if self.enemy.is_defeated():
            self.controller.player_wins()
            self.end_fight()
        else:
            self.enemy_turn()

    # Player Attack

    def did_player_critical_hit(self):
        return self.player.did_crit() and self.enemy.void_critical_hit is False

    def check_for_player_critical_hit(self):
        return self.did_player_critical_hit()

    def check_for_enemy_dodge(self):
        return self.enemy.did_dodge()

    def calculate_player_critical_hit_damage(self):
        low, high = self.player.crit_range(self.player.attack_num())
        return Randomizer.randint(low, high)

    def calculate_player_attack_damage(self, critical_hit):
        if critical_hit:
            return self.calculate_player_critical_hit_damage()
        return self.calculate_player_normal_hit_damage()

    def calculate_player_normal_hit_damage(self):
        low, high = self.player.damage_range(self.player.attack_num(), self.enemy.agility)
        return Randomizer.randint(low, high)

    def player_attack(self, *_):
        """ Orchestrates what happens when the player clicks the attack button on their turn. """
        player_crit_this_turn = self.check_for_player_critical_hit()
        enemy_dodge_this_turn = self.check_for_enemy_dodge()

        damage_dealt = self.calculate_player_attack_damage(player_crit_this_turn)
        self.process_player_attack_result(player_crit_this_turn, enemy_dodge_this_turn, damage_dealt)

    def process_player_attack_result(self, crit, dodge, damage):
        self.player.attack_msg(crit, dodge, damage, self.enemy.name)
        if dodge and not crit:
            self.enemy_attack()
        else:
            self.apply_attack_damage_to_enemy(damage)

    def apply_attack_damage_to_enemy(self, damage):
        self.enemy.take_damage(damage)
        self.controller.update_enemy_info()
        self.is_enemy_defeated()

    # Player uses an herb

    def use_herb(self):
        """ Handle herb consumption by the player """
        if self.model.player.herb_count <= 0:
            self.controller.no_herbs()
            return  # Use return here so player can select another option.

        self.model.player.herb_count -= 1
        if self.model.player.curr_hp >= self.model.player.max_hp:
            self.controller.eat_herb_at_full_hp()
            self.is_enemy_defeated()

        heal_amt = self.calculate_player_herb_heal_amount()
        self.model.player.curr_hp += heal_amt
        self.controller.eat_herb(heal_amt)
        self.is_enemy_defeated()

    def calculate_player_herb_heal_amount(self):
        """ Calculates the amount of health an herb will restore. """
        heal_amt = Randomizer.randint(*self.herb_range)
        return min(heal_amt, self.model.player.max_hp - self.model.player.curr_hp)

    # Enemy Actions

    def handle_enemy_sleep(self):
        if self.enemy.is_asleep():
            self.player_turn()
        elif self.should_enemy_flee():
            self.enemy_flees()
        else:
            self.perform_enemy_action()

    def should_enemy_flee(self):
        return self.model.player.strength > self.model.enemy.strength * 2 and random.randint(1, 4) == 4

    def enemy_turn(self):
        """ Handles the Enemy's turn """

        if self.model.enemy.enemy_sleep_count > 0:
            self.handle_enemy_sleep()
            # Enemy is asleep. Handle sleep.

        elif self.should_enemy_flee():
            # Handle fleeing
            self.enemy_flees()
        else:
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

    def enemy_flees(self):
        """ Enemy runs away. End the combat"""
        self.model.text(f"The {self.enemy.name} flees from your superior strength!")
        self.fight_over.set(True)

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

    @staticmethod
    def resist(chance):
        return Randomizer.randint(1, 16) <= chance

    def enemy_attack(self):
        """Enemy attacks normally"""
        self.model.text(f"\nEnemy turn\n")
        enemy_damage_dealt = self.enemy.attack(self.player.defense())
        self.model.player.curr_hp -= enemy_damage_dealt
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

        mag_def = self.model.player["mag_def"]
        hurt_dmg = 0

        if mag_def and more:
            hurt_dmg = random.randint(hurtmore_low[0], hurtmore_low[1])
        elif mag_def and not more:
            hurt_dmg = random.randint(hurt_low[0], hurt_low[1])
        elif more:
            hurt_dmg = random.randint(hurtmore_high[0], hurtmore_high[1])
        else:
            hurt_dmg = random.randint(hurt_high[0], hurt_high[1])

        self.model.player["hp"] -= hurt_dmg
        self.output.output = f"""The {self.model.enemy["name"]} casts {spell_name}! {self.model.player["name"]} is hurt for {hurt_dmg} damage!"""
        self.is_player_defeated()

    def enemy_casts_heal(self, more):
        """ Enemy handling of heal and healmore"""
        spell_name = "Healmore" if more else "Heal"
        if self.model.enemy["e_stop"]:
            self.output.output = f"""The {self.model.enemy["name"]} casts {spell_name}, but their spell has been blocked!"""
            return

        heal_range = [20, 27]
        healmore_range = [85, 100]

        heal_max = self.model.enemy["maxhp"] - self.model.enemy["hp"]

        heal_rand = random.randint(healmore_range[0], healmore_range[1]) if more else random.randint(heal_range[0],
                                                                                                     heal_range[1])

        heal_amt = heal_rand if heal_rand < heal_max else heal_max

        self.model.enemy["hp"] += heal_amt
        self.output.output = f"""The {self.model.enemy["name"]} casts {spell_name}! {self.model.enemy["name"]} is healed {heal_amt} hit points!"""
        self.view.update_enemy_info(self.model.enemy)
        self.player_turn()

    def enemy_casts_sleep(self):
        """Enemy attempts to cast sleep"""
        spell_name = "Sleep"
        if self.model.enemy["e_stop"]:
            self.output.output = f"""The {self.model.enemy["name"]} casts {spell_name}, but their spell has been blocked!"""
        else:
            self.p.asleep = True
            self.output.output = f"""The {self.model.enemy["name"]} casts {spell_name}. You fall asleep!!"""
        self.player_turn()

    def enemy_casts_stopspell(self):
        """ Enemy attempts to cast stopspell. 50% chance of failure"""
        spell_name = "Stopspell"
        if self.model.enemy["e_stop"]:
            self.output.output = f"""The {self.model.enemy["name"]} casts {spell_name}, but their spell has been blocked!"""
        elif random.randint(1, 2) == 2:
            self.model.player["p_stop"] = True
            self.output.output = f"""The {self.model.enemy["name"]} casts {spell_name}! Your magic has been blocked!"""
        else:
            self.output.output = f"""The {self.model.enemy["name"]} casts {spell_name}, but the spell fails!"""
        self.player_turn()

    def enemy_breathes_fire(self, more):
        """ Enemy handling of breath attacks"""
        spell_name = "strong flames at you!" if more else "fire"
        if self.model.enemy["e_stop"]:
            self.output.output = f"""The {self.model.enemy["name"]} casts {spell_name}, but their spell has been blocked!"""
            return

        fire_high = [16, 23]
        fire_low = [10, 14]
        strongfire_high = [65, 72]
        strongfire_low = [42, 48]

        fire_def = self.model.player["fire_def"]
        fire_dmg = 0

        if fire_def and more:
            fire_dmg = random.randint(strongfire_low[0], strongfire_low[1])
        elif fire_def and not more:
            fire_dmg = random.randint(fire_low[0], fire_low[1])
        elif more:
            fire_dmg = random.randint(strongfire_high[0], strongfire_high[1])
        else:
            fire_dmg = random.randint(fire_high[0], fire_high[1])

        self.model.player["hp"] -= fire_dmg
        self.output.output = f"""The {self.model.enemy["name"]} breathes {spell_name}! {self.model.player["name"]} is hurt for {fire_dmg} damage!"""
        self.is_player_defeated()



    def run_away(self, *_):
        """Player attempts to flee battle."""
        run_modifiers = [0.25, 0.375, 0.75, 1]
        p_run_chance = random.randint(0, 254)
        e_block_chance = random.randint(0, 254)
        e_block_mod = run_modifiers[self.model.enemy["run"]]
        self.output.output = """You attempt to run away...\n"""
        succeed_flee = self.model.player["agility"] * p_run_chance > self.model.enemy[
            "agility"] * e_block_chance * e_block_mod
        if succeed_flee:
            self.output.output = """You successfully flee!\n"""
            self.end_fight()
        else:
            self.output.output = f"""...but the {self.model.enemy["name"]} blocks you from running away!\n"""
            self.enemy_turn()

    def player_cast_magic(self, *_):
        spell = self.view.chosen_magic.get()
        spell_switch = {
            "Heal": lambda: self.player_heal(False),
            "Healmore": lambda: self.player_heal(True),
            "Hurt": lambda: self.player_hurt(False),
            "Hurtmore": lambda: self.player_hurt(True),
            "Sleep": self.player_casts_sleep,
            "Stopspell": self.player_casts_stopspell
        }
        spell_cost = {
            "Heal": 4,
            "Healmore": 10,
            "Hurt": 2,
            "Hurtmore": 5,
            "Sleep": 2,
            "Stopspell": 2
        }

        can_cast = self.model.player["mp"] > spell_cost.get(spell)
        if not can_cast:
            self.output.output = f"""Player tries to cast {spell}, but doesn't have enough MP!\n"""
        else:
            self.model.player["mp"] -= spell_cost.get(spell)
            if self.model.player["p_stop"]:
                self.output.output = f"""Player casts {spell}, but their magic has been sealed!\n"""
            else:
                spell_switch.get(spell)()
        self.view.update_ptext(self.model.player)
        self.is_enemy_defeated()

    def player_heal(self, more):
        player_heal_range = [10, 17]
        player_healmore_range = [85, 100]
        spell_name = "Healmore" if more else "Heal"
        heal_total = 0

        if more:
            heal_total = self.calc_heal(player_healmore_range)
        else:
            heal_total = self.calc_heal(player_heal_range)

        if heal_total == 0:
            self.view.main_frame.txt.insert(
                tk.END,
                f"""Player casts {spell_name}, but their hit points were already at maximum!\n"""
            )
        else:
            self.model.player["hp"] += heal_total
            self.view.main_frame.txt.insert(
                tk.END,
                f"""Player casts {spell_name}! Player is healed {str(heal_total)} hit points!\n"""
            )

    def calc_heal(self, heal_range):
        heal_max = self.model.player["maxhp"] - self.model.player["hp"]
        heal_amount = random.randint(heal_range[0], heal_range[1])
        return heal_max if heal_max < heal_amount else heal_amount

    def player_hurt(self, more):
        """ Handles player casting of Hurt and Hurtmore"""
        player_hurt_range = [5, 12]
        player_hurtmore_range = [58, 65]
        enemy_hurt_resistance = self.model.enemy["hurtR"]
        spell_name = "Hurtmore" if more else "Hurt"
        hurt_dmg = random.randint(player_hurtmore_range[0], player_hurtmore_range[1]) if more else random.randint(
            player_hurt_range[0], player_hurt_range[1])

        if self.resist(enemy_hurt_resistance):
            self.view.main_frame.txt.insert(
                tk.END,
                f"""Player casts {spell_name}, but the enemy resisted!\n"""
            )
        else:
            self.view.main_frame.txt.insert(
                tk.END,
                f"""Player casts {spell_name}! {self.model.enemy["name"]} is hurt by {str(hurt_dmg)} hit points!\n"""
            )
            self.model.enemy["hp"] -= hurt_dmg

    def player_casts_sleep(self):
        """ Player tries to cast Sleep on the enemy"""
        enemy_sleep_resistance = self.model.enemy["sleepR"]
        if self.model.enemy["e_sleep"] > 0:
            self.view.main_frame.txt.insert(
                tk.END,
                f"""Player casts Sleep! But the {self.model.enemy["name"]} is already asleep!\n"""
            )
        elif self.resist(enemy_sleep_resistance):
            self.view.main_frame.txt.insert(
                tk.END,
                f"""Player casts Sleep! But the {self.model.enemy["name"]} resisted!\n"""
            )
        else:
            self.view.main_frame.txt.insert(
                tk.END,
                f"""Player casts Sleep! The {self.model.enemy["name"]} is now asleep!\n"""
            )
            self.model.enemy["e_sleep"] = 2
        return

    def player_casts_stopspell(self):
        """ Player tries to cast Stopspell on the enemy"""
        enemy_stop_resistance = self.model.enemy["stopR"]
        if self.model.enemy["e_stop"]:
            self.view.main_frame.txt.insert(
                tk.END,
                f"""Player casts Stopspell! But the {self.model.enemy["name"]}'s magic was already blocked!\n"""
            )
        elif self.resist(enemy_stop_resistance):
            self.view.main_frame.txt.insert(
                tk.END,
                f"""Player casts Stopspell! But the {self.model.enemy["name"]} resisted!\n"""
            )
        else:
            self.view.main_frame.txt.insert(
                tk.END,
                f"""Player casts Stopsell! The {self.model.enemy["name"]}'s magic is now blocked!!\n"""
            )
            self.model.enemy["e_stop"] = True




class EnemyBattle():
    """Enemy Battle Class"""

    def __init__(self, e_model):
        self.model = e_model
        self.name = e_model["name"]
        self.agi = e_model["agility"]
        self.hp = e_model["hp"]
        self.dodge_chance = e_model["dodge"]

    def dodge(self, chance):
        return random.randint(1, 64) <= chance

    def did_dodge(self):
        return self.dodge(self.dodge_chance)


