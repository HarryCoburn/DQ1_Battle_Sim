"""
Player class
"""

import random
from typing import List, Optional
from dataclasses import dataclass, field
from fightsim.models.items import Item, ItemType, items
from ..common.messages import ObserverMessages, SpellFailureReason
from .player_leveling import _Levelling
from ..common.randomizer import Randomizer

CRIT_CHANCE: int = 32
SLEEP_COUNT: int = 6


@dataclass
class AttackResult:
    crit: bool
    dodge: bool
    damage: int
    hit: bool

@dataclass
class HerbResult:
    success: bool
    healing: int
    reason: str = ""

@dataclass
class SpellResult:
    spell_name: str
    success: bool
    amount: int = 0
    reason: Optional[SpellFailureReason] = None

@dataclass
class Player:
    name: str = "Rollo"
    level: int = 1
    strength: int = 4
    agility: int = 4
    current_hp: int = 15
    max_hp: int = 15
    current_mp: int = 0
    max_mp: int = 0
    weapon: Item = field(
        default_factory=lambda: items[ItemType.WEAPON.value]["Unarmed"]
    )
    armor: Item = field(default_factory=lambda: items[ItemType.ARMOR.value]["Naked"])
    shield: Item = field(
        default_factory=lambda: items[ItemType.SHIELD.value]["No Shield"]
    )
    player_magic: List[str] = field(default_factory=list)
    herb_count: int = 0
    reduce_hurt_damage: bool = False
    reduce_fire_damage: bool = False
    is_asleep: bool = False
    is_spellstopped: bool = False
    sleep_count: int = SLEEP_COUNT
    leveler: _Levelling = _Levelling()
    model: Optional = None  # Placeholder
    herb_range: tuple = (23, 30)

    def __post_init__(self):
        self.player_magic = []
        if not 1 <= self.level <= 30:
            raise ValueError("Level must be within 1 to 30")

    def set_model(self, model):
        """
        Injects model dependence into Player.
        """
        self.model = model

    # Changing Player stats

    def change_name(self, name):
        """
        Sets the new name and then recalculates the stats of the player based on the new name value.
        """
        self.name = name
        self.recalculate_stats()

    def level_up(self, value):
        """
        Sets the new level and then recalculates the stats of the player based on the new level value.
        """
        self.level = value
        self.recalculate_stats()

    def recalculate_stats(self):

        self.strength, self.agility, self.max_hp, self.max_hp = (
            self.leveler.adjust_stats(self.level, self.name)
        )
        self.current_hp = self.max_hp
        self.current_mp = self.max_mp
        self.build_p_magic_list()

    def build_p_magic_list(self):
        """
        Create a list of available spells based on level
        """
        self.player_magic = []
        if self.level >= 3:
            self.player_magic.append("Select Spell")
            self.player_magic.append("Heal")
        if self.level >= 4:
            self.player_magic.append("Hurt")
        if self.level >= 7:
            self.player_magic.append("Sleep")
        if self.level >= 10:
            self.player_magic.append("Stopspell")
        if self.level >= 17:
            self.player_magic.append("Healmore")
        if self.level >= 19:
            self.player_magic.append("Hurtmore")
        self.model.observed.notify(ObserverMessages.UPDATE_PLAYER_MAGIC)

    def equip_weapon(self, weapon_name: str):
        """
        Sets a new weapon on the player. Keeps the same weapon if it is not found.
        """
        self.weapon = items[ItemType.WEAPON.value].get(weapon_name, self.weapon)

    def equip_armor(self, armor_name: str):
        """
        Sets a new armor on the player. Keeps the same armor if it is not found.
        """
        self.armor = items[ItemType.ARMOR.value].get(armor_name, self.armor)
        self.reduce_hurt_damage = self.armor.reduce_hurt_damage
        self.reduce_fire_damage = self.armor.reduce_fire_damage

    def equip_shield(self, shield_name: str):
        """
        Sets a new shield on the player. Keeps the same shield if it is not found.
        """
        self.shield = items[ItemType.SHIELD.value].get(shield_name, self.shield)

    def raise_hp(self, hp_gain):
        self.current_hp += hp_gain

    def lower_hp(self, hp_gain):
        self.current_hp -= hp_gain

    # Attack damage calcuations

    def calculate_attack_damage(self, critical_hit, enemy_agility):
        if critical_hit:
            low, high = self.crit_range(self.attack_num())
        else:
            low, high = self.damage_range(self.attack_num(), enemy_agility)
        return Randomizer.randint(low, high)

    def attack_num(self):
        """
        Calculate and return attack number
        """
        return self.strength + self.weapon.modifier

    @staticmethod
    def damage_range(attack, agility):
        """
        Returns a possible damage range for a normal attack as a tuple in the form (min, max)
        min must be at least 0, max can be no lower than 1
        """
        return max(((attack - agility // 2) // 4), 0), max(
            ((attack - agility // 2) // 2), 1
        )

    @staticmethod
    def crit_range(attack):
        """
        Returns a possible critical damage range for a normal attack as a tuple in the form (min, max)
        min must be at least 0, max can be no lower than 1
        """
        return max((attack // 2), 0), max(attack, 1)

    def attack(self, enemy):
        crit = self.did_crit() and enemy.void_critical_hit is False
        dodge = enemy.did_dodge()
        damage = self.calculate_attack_damage(crit, enemy.agility)

        return AttackResult(
            crit=crit, dodge=dodge, damage=damage, hit=not (dodge and not crit)
        )

    @staticmethod
    def did_crit():
        """
        Returns if the player had a critical hit or not.
        """
        return random.randint(1, CRIT_CHANCE) == 1

    # Herb usage

    def has_herbs(self):
        return self.herb_count >= 1

    def use_herb(self):
        """Returns the amount healed"""
        self.herb_count -= 1        
        if self.current_hp >= self.max_hp:
            return HerbResult(
                success=False, healing=0, reason="max_hp"
            )
        herb_hp = Randomizer.randint(*self.herb_range)
        actual_hp_gained = min(herb_hp, self.max_hp - self.current_hp)
        #self.current_hp += actual_hp_gained
        return HerbResult(
            success=True, healing=actual_hp_gained
        )
    
    # Magic Usage

    def cast_magic(self, spell, enemy):
        spell_switch = {
            "Heal": lambda: self.player_heal(False),
            "Healmore": lambda: self.player_heal(True),
            "Hurt": lambda: self.player_hurt(False, enemy),
            "Hurtmore": lambda: self.player_hurt(True, enemy),
            "Sleep": self.player_casts_sleep(enemy),
            "Stopspell": self.player_casts_stopspell(enemy),
        }

        spell_cost = {
            "Heal": 4,
            "Healmore": 10,
            "Hurt": 2,
            "Hurtmore": 5,
            "Sleep": 2,
            "Stopspell": 2,
        }

        cost = spell_cost.get(spell, 0)
        if self.current_mp < cost:
            return SpellResult(
                spell_name=spell, success=False, amount=0, reason=SpellFailureReason.NOT_ENOUGH_MP
            )
        self.current_mp -= cost  # always burn the MP even if spellstopped
        if self.is_spellstopped:
            return SpellResult(
                spell_name=spell, success=False, amount=0, reason=SpellFailureReason.PLAYER_SPELLSTOPPED
            )
        spell_function = spell_switch.get(spell, lambda: None)
        spell_function()

    # Heal

    def player_heal(self, more):
        heal_ranges = {"Heal": [10, 17], "Healmore": [85, 100]}
        spell_name = "Healmore" if more else "Heal"

        heal_range = heal_ranges[spell_name]
        heal_total = self.calc_heal(heal_range)
        if heal_total == 0:
            return SpellResult(spell_name=spell_name, success=False, amount=0, reason=SpellFailureReason.HEALED_AT_MAX_HP)
        else:
            self.current_hp += heal_total
            return heal_total

    def calc_heal(self, heal_range):
        heal_max = self.max_hp - self.current_hp
        heal_amount = Randomizer.randint(*heal_range)
        return min(heal_max, heal_amount)

    # Hurt

    def player_hurt(self, more, enemy):
        hurt_ranges = {"Hurt": [5, 12], "Hurtmore": [58, 65]}
        spell_name = "Hurtmore" if more else "Hurt"
        hurt_range = hurt_ranges[spell_name]
        enemy_hurt_resistance = enemy.hurt_resist
        if self.resist(enemy_hurt_resistance):
            return SpellResult(spell_name=spell_name, success=False, amount=0, reason=SpellFailureReason.ENEMY_RESISTED_HURT)

        hurt_total = self.calc_hurt(hurt_range)
        enemy.take_damage(hurt_total)
        return hurt_total

    def calc_hurt(self, hurt_range):
        return Randomizer.randint(*hurt_range)    

    # Sleep

    def player_casts_sleep(self, enemy):
        enemy_sleep_resistance = enemy.sleep_resist
        if enemy.enemy_sleep_count > 0:  # enemy already asleep
            return SpellResult(spell_name="Sleep", success=False, reason=SpellFailureReason.ENEMY_ALREADY_ASLEEP)
        if self.resist(enemy_sleep_resistance):  # enemy resists sleep
            return SpellResult(spell_name="Sleep", success=False, reason=SpellFailureReason.ENEMY_RESISTED_SLEEP)
        enemy.enemy_sleep_count = 2
        return "success"  # dummy string

    # Stopspell

    def player_casts_stopspell(self, enemy):
        enemy_stop_resistance = enemy.stopspell_resist
        if enemy.enemy_spell_stopped:
            return "enemy_already_spellstopped"
        if self.resist(enemy_stop_resistance):
            return "enemy_resists_spellstop"
        enemy.enemy_spell_stopped = True
        return "success"  # dummy string

    # Handle player's sleep status

    def handle_sleep(self):
        """
        Returns the status of the player's sleep
        """
        if not self.is_asleep:
            return False
        else:
            self.sleep_count -= 1
            if random.randint(1, 2) == 2 or self.sleep_count <= 0:
                self.is_asleep = False
                self.sleep_count = 6
                return "awake"
            else:
                return True
            
    # Handle fleeing

    def is_flee_successful(self, enemy_agility, mod_select):
        """Return True if the player flees successfully"""
        enemy_run_modifiers = [0.25, 0.375, 0.75, 1]
        player_flee_chance = self.agility * Randomizer.randint(0, 254)
        enemy_block_chance = (
            enemy_agility * Randomizer.randint(0, 254) * enemy_run_modifiers[mod_select]
        )
        return player_flee_chance > enemy_block_chance

    # Misc stats

    def resist(self, chance):
        return Randomizer.randint(1, 16) <= chance
    
    def defense(self):
        """
        Calculate and return defense value
        """
        return (self.agility + self.armor.modifier + self.shield.modifier) // 2

    def is_defeated(self):
        """
        Returns if the player is defeated
        """
        return self.current_hp <= 0

def player_factory():
    """
    Returns a player
    """
    return Player()
