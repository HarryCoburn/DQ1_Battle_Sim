"""
battle.py - Battle code for DQ1 sim. Holds both player and enemy code.
"""

import random
from collections.abc import Callable
import tkinter as tk
from ..common.messages import EnemyActions
from ..common.randomizer import Randomizer



class Battle:
    """
    Main battle controller
    """

    def __init__(self, player, enemy, log, rng: random.Random, on_end):

        self.player = player
        self.enemy = enemy
        self.rng = rng
        self.log = log
        self.on_end = on_end
        self.herb_range = (23, 30)
        self.over = False

    # Core Fight Routines



    def start_fight(self):
        """Starts the battle loop"""
        self.log(f"""You are fighting the {self.enemy.name}!\n""")

        surprise_check = self.does_enemy_surprise()
        if surprise_check:
            self.log(f"The {self.enemy.name} surprises you!\n")
            self.advance()
        # Now we wait for the UI to call turn_engine

    def take_turn(self, action: Callable[[], bool]) -> None:
        if self.over or not action():
            return
        self.advance()

    def advance(self) -> None:
        """Resolve everything until the player needs to choose again."""
        while not self.over:
            if self.enemy.is_defeated():
                self.log(f"You have defeated the {self.enemy.name}!\n")
                return self.finish()
            self.enemy_turn()
            if self.over:
                return
            if self.player.is_defeated():
                self.log(f"You have been defeated by the {self.enemy.name}!\n")
                return self.finish()
            if not self.player.check_sleep():
                return
            # Player is asleep: Loop so enemy attacks again.

    def finish(self) -> None:
        self.over = True
        self.on_end()

    def does_enemy_surprise(self):
        """ Determine if the enemy surprises the player based on agility and randomness. """
        player_roll = self.player.agility * self.rng.randint(0,254)
        enemy_roll = self.enemy.agility * self.rng.randint(0,254) * 0.25
        return player_roll < enemy_roll

    # Player Actions

    # Player Attack

    def did_player_critical_hit(self):
        return self.player.did_crit() and self.enemy.void_critical_hit is False

    def calculate_player_critical_hit_damage(self):
        low, high = self.player.crit_range(self.player.attack_num())
        return self.rng.randint(low, high)

    def calculate_player_attack_damage(self, critical_hit):
        if critical_hit:
            return self.calculate_player_critical_hit_damage()
        return self.calculate_player_normal_hit_damage()

    def calculate_player_normal_hit_damage(self):
        low, high = self.player.damage_range(self.player.attack_num(), self.enemy.agility)
        return self.rng.randint(low, high)

    def player_attack(self) -> bool:
        crit = self.did_player_critical_hit()
        dodge = self.enemy.did_dodge()
        damage = self.calculate_player_attack_damage(crit)
        self.player.attack_msg(crit, dodge, damage, self.enemy.name)
        if crit or not dodge:
            self.enemy.take_damage(damage)
        return True

    # Player uses an herb
    def use_herb(self) -> bool:
        """ Handle herb consumption by the player """
        if self.player.herb_count <= 0:
            self.log("You have no herbs!")
            return False

        self.player.herb_count -= 1
        if self.player.current_hp >= self.player.max_hp:
            self.log("You eat a herb, but your hit points are already at maximum!\n")
            return True

        heal_amt = self.calculate_player_herb_heal_amount()
        self.player.current_hp += heal_amt
        self.log(f"""You eat a herb and regain {heal_amt} hit points!\n""")
        return True

    def calculate_player_herb_heal_amount(self):
        """ Calculates the amount of health an herb will restore. """
        heal_amt = Randomizer.randint(*self.herb_range)
        return min(heal_amt, self.player.max_hp - self.player.current_hp)

    # Player Flees

    def is_flee_successful(self):
        """ Return True if the player flees successfully """
        enemy_run_modifiers = [0.25, 0.375, 0.75, 1]
        player_flee_chance = self.player.agility * self.rng.randint(0, 254)
        enemy_block_chance = self.enemy.agility * self.rng.randint(0, 254) * enemy_run_modifiers[self.enemy.run]
        return player_flee_chance > enemy_block_chance

    def player_flees(self) -> bool:
        """Player attempts to flee battle."""
        self.log("You attempt to run away...\n")
        if self.is_flee_successful():
            self.log("You successfully flee!\n")
            self.finish()
        else:
            self.log(f"...but the {self.enemy.name} blocks you from running away!\n")
        return True

    # Player Magic

    def player_cast_magic(self, spell) -> bool:

        if spell in ["Select Spell", "No Magic Available"]:
            self.log(
                "You must select a valid spell first." if spell == "Select Spell" else "Your level is too low to cast magic.")
            return False

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

        cost = spell_cost.get(spell, 0)
        if cost == 0:
            raise ValueError(f"No cost defined for spell {spell!r}")

        if self.player.current_mp < cost:
            self.log(f"Player tries to cast {spell}, but doesn't have enough MP!\n")
            return True # Intended. Casting without enough MP wastes turn.

        self.player.current_mp -= cost
        if self.player.is_spellstopped:
            self.log(f"""Player casts {spell}, but their magic has been sealed!\n""")
            return True

        # Execute the spell function
        spell_function = spell_switch.get(spell, lambda: None)
        spell_function()
        return True

    def player_heal(self, more):
        heal_ranges = {
            "Heal": [10, 17],
            "Healmore": [85,100]
        }
        spell_name = "Healmore" if more else "Heal"
        heal_range = heal_ranges[spell_name]

        heal_total = self.calc_heal(heal_range)
        if heal_total == 0:
            self.log(f"""Player casts {spell_name}, but their hit points were already at maximum!\n""")
        else:
            self.player.current_hp += heal_total
            self.log(f"""Player casts {spell_name}! Player is healed {str(heal_total)} hit points!\n""")

    def calc_heal(self, heal_range):
        heal_max = self.player.max_hp - self.player.current_hp
        heal_amount = self.rng.randint(*heal_range)
        return min(heal_max, heal_amount)

    def player_hurt(self, more):
        """ Handles player casting of Hurt and Hurtmore"""
        hurt_ranges = {
            "Hurt": [5, 12],
            "Hurtmore": [58, 65]
        }
        spell_name = "Hurtmore" if more else "Hurt"
        hurt_range = hurt_ranges[spell_name]
        enemy_hurt_resistance = self.enemy.hurt_resist

        hurt_total = self.calc_hurt(hurt_range)

        if self.resist(enemy_hurt_resistance):
            self.log(f"""Player casts {spell_name}, but the enemy resisted!\n""")
        else:
            self.enemy.take_damage(hurt_total)
            self.log(f"""Player casts {spell_name}! {self.enemy.name} is hurt by {str(hurt_total)} hit points!\n""")

    @staticmethod
    def calc_hurt(hurt_range):
        return Randomizer.randint(*hurt_range)

    def player_casts_sleep(self):
        """ Player tries to cast Sleep on the enemy"""
        enemy_sleep_resistance = self.enemy.sleep_resist
        if self.enemy.enemy_sleep_count > 0:
            self.log(f"""Player casts Sleep! But the {self.enemy.name} is already asleep!\n""")
        elif self.resist(enemy_sleep_resistance):
            self.log(f"""Player casts Sleep! But the {self.enemy.name} resisted!\n""")
        else:
            self.log(f"""Player casts Sleep! The {self.enemy.name} is now asleep!\n""")
            self.enemy.enemy_sleep_count = 2

    def player_casts_stopspell(self):
        """ Player tries to cast Stopspell on the enemy"""
        enemy_stop_resistance = self.enemy.stopspell_resist
        if self.enemy.enemy_spell_stopped:
            self.log(f"""Player casts Stopspell! But the {self.enemy.name}'s magic was already blocked!\n""")
        elif self.resist(enemy_stop_resistance):
            self.log(f"""Player casts Stopspell! But the {self.enemy.name} resisted!\n""")
        else:
            self.log(f"""Player casts Stopspell! The {self.enemy.name}'s magic is now blocked!!\n""")
            self.enemy.enemy_spell_stopped = True



    # Enemy Actions
    #
    def enemy_turn(self):
        """ Handles the Enemy's turn """

        if self.enemy.enemy_sleep_count > 0 and self.enemy.is_asleep():
            self.log(f"The {self.enemy.name} is asleep.\n")
            return
        if self.should_enemy_flee():
            self.enemy_flees()
            return
        self.perform_enemy_action()

    def should_enemy_flee(self):
        return self.player.strength > self.enemy.strength * 2 and self.rng.randint(1, 4) == 4

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
        raise NotImplementedError("Enemy tried to attack with something not programmed yet!!\n")

    def enemy_flees(self):
        """ Enemy runs away. End the combat"""
        self.log(f"The {self.enemy.name} flees from your superior strength!\n")
        self.finish()

    def enemy_choose_attack(self):
        atk_list = self.enemy.pattern
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
                if action == EnemyActions.SLEEP and not self.player.is_asleep:
                    choice = action
                    break
                if action == EnemyActions.STOPSPELL and not self.player.is_spellstopped:
                    choice = action
                    break

        return choice or EnemyActions.ATTACK

    @staticmethod
    def resist(chance):
        return Randomizer.randint(1, 16) <= chance

    def enemy_attack(self):
        """Enemy attacks normally"""
        self.log(f"\nEnemy turn\n")
        enemy_damage_dealt = self.enemy.attack(self.player.defense())
        self.player.current_hp -= enemy_damage_dealt

        self.log(f"{self.enemy.name} attacks! {self.enemy.name} hits you for {enemy_damage_dealt} damage.\n")


    def enemy_casts_hurt(self, more):
        """ Enemy handling of hurt and hurtmore"""
        spell_name = "Hurtmore" if more else "Hurt"
        if self.enemy.is_spell_stopped(spell_name):
            self.log(f"""The {self.enemy.name} casts {spell_name}, but their spell has been blocked!\n""")
            return

        hurt_high = [3, 10]
        hurt_low = [2, 6]
        hurtmore_high = [30, 45]
        hurtmore_low = [20, 30]

        mag_def = self.player.reduce_hurt_damage
        hurt_dmg = 0

        if mag_def and more:
            hurt_dmg = random.randint(hurtmore_low[0], hurtmore_low[1])
        elif mag_def and not more:
            hurt_dmg = random.randint(hurt_low[0], hurt_low[1])
        elif more:
            hurt_dmg = random.randint(hurtmore_high[0], hurtmore_high[1])
        else:
            hurt_dmg = random.randint(hurt_high[0], hurt_high[1])

        self.player.current_hp -= hurt_dmg
        self.log(f"""The {self.enemy.name} casts {spell_name}! {self.player.name} is hurt for {hurt_dmg} damage!\n""")


    def enemy_casts_heal(self, more):
        """ Enemy handling of heal and healmore"""
        spell_name = "Healmore" if more else "Heal"
        if self.enemy.enemy_spell_stopped:
            self.log(f"""The {self.enemy.name} casts {spell_name}, but their spell has been blocked!\n""")
            return

        heal_range = [20, 27]
        healmore_range = [85, 100]

        heal_max = self.enemy.max_hp - self.enemy.current_hp

        heal_rand = random.randint(healmore_range[0], healmore_range[1]) if more else random.randint(heal_range[0],
                                                                                                     heal_range[1])

        heal_amt = heal_rand if heal_rand < heal_max else heal_max

        self.enemy.current_hp += heal_amt
        self.log(f"""The {self.enemy.name} casts {spell_name}! {self.enemy.name} is healed {heal_amt} hit points!\n""")


    def enemy_casts_sleep(self):
        """Enemy attempts to cast sleep"""
        spell_name = "Sleep"
        if self.enemy.enemy_spell_stopped:
            self.log(f"""The {self.enemy.name} casts {spell_name}, but their spell has been blocked!\n""")
        else:
            self.player.is_asleep = True
            self.log(f"""The {self.enemy.name} casts {spell_name}. You fall asleep!!\n""")

    def enemy_casts_stopspell(self):
        """ Enemy attempts to cast stopspell. 50% chance of failure"""
        spell_name = "Stopspell"
        if self.enemy.enemy_spell_stopped:
            self.log(f"The {self.enemy.name} casts {spell_name}, but their spell has been blocked!\n")
        elif random.randint(1, 2) == 2:
            self.player.is_spellstopped = True
            self.log(f"""The {self.enemy.name} casts {spell_name}! Your magic has been blocked!\n""")
        else:
            self.log(f"""The {self.enemy.name} casts {spell_name}, but the spell fails!\n""")

    def enemy_breathes_fire(self, more):
        """ Enemy handling of breath attacks"""
        # Stopspell does not affect breath attacks.
        spell_name = "strong flames at you!" if more else "fire"

        fire_high = [16, 23]
        fire_low = [10, 14]
        strongfire_high = [65, 72]
        strongfire_low = [42, 48]

        fire_def = self.player.reduce_fire_damage
        fire_dmg = 0

        if fire_def and more:
            fire_dmg = random.randint(strongfire_low[0], strongfire_low[1])
        elif fire_def and not more:
            fire_dmg = random.randint(fire_low[0], fire_low[1])
        elif more:
            fire_dmg = random.randint(strongfire_high[0], strongfire_high[1])
        else:
            fire_dmg = random.randint(fire_high[0], fire_high[1])

        self.player.current_hp -= fire_dmg
        self.log(f"""The {self.enemy.name} breathes {spell_name}! {self.player.name} is hurt for {fire_dmg} damage!\n""")
