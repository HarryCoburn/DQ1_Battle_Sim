"""
Player class
"""

import random
from typing import List, Optional
from dataclasses import dataclass, field
from fightsim.models.items import Item, ItemType, items
from ..common.messages import ObserverMessages
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
class Player:
    name: str = "Rollo"
    level: int = 1
    strength: int = 4
    agility: int = 4
    current_hp: int = 15
    max_hp: int = 15
    current_mp: int = 0
    max_mp: int = 0
    weapon: Item = field(default_factory=lambda: items[ItemType.WEAPON.value]["Unarmed"])
    armor: Item = field(default_factory=lambda: items[ItemType.ARMOR.value]["Naked"])
    shield: Item = field(default_factory=lambda: items[ItemType.SHIELD.value]["No Shield"])
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

    def defense(self):
        """
        Calculate and return defense value
        """
        return (self.agility + self.armor.modifier + self.shield.modifier) // 2

    def attack_num(self):
        """
        Calculate and return attack number
        """
        return self.strength + self.weapon.modifier

    def set_model(self, model):
        """
        Injects model dependence into Player.
        """
        self.model = model

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

        self.strength, self.agility, self.max_hp, self.max_hp = self.leveler.adjust_stats(self.level, self.name)
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
        
    def calculate_attack_damage(self, critical_hit, enemy_agility):
        if critical_hit:
            low, high = self.crit_range(self.attack_num())
        else:
            low, high = self.damage_range(self.attack_num(), enemy_agility)    
        return Randomizer.randint(low, high)
    # 
    def attack(self, enemy):
        crit = self.did_crit() and enemy.void_critical_hit is False
        dodge = enemy.did_dodge()
        damage = self.calculate_attack_damage(crit, enemy.agility)

        return AttackResult(
            crit = crit,
            dodge = dodge,
            damage = damage,
            hit = not (dodge and not crit)
        )

    @staticmethod
    def did_crit():
        """
        Returns if the player had a critical hit or not.
        """
        return random.randint(1, CRIT_CHANCE) == 1

    @staticmethod
    def damage_range(attack, agility):
        """
        Returns a possible damage range for a normal attack as a tuple in the form (min, max)
        min must be at least 0, max can be no lower than 1
        """
        return max(((attack - agility // 2) // 4), 0), max(((attack - agility // 2) // 2), 1)
    
    @staticmethod
    def crit_range(attack):
        """
        Returns a possible critical damage range for a normal attack as a tuple in the form (min, max)
        min must be at least 0, max can be no lower than 1
        """
        return max((attack // 2), 0), max(attack, 1)

    def is_defeated(self):
        """
        Returns if the player is defeated
        """
        return self.current_hp <= 0

    def check_sleep(self):
        """
        Returns if the player is asleep or not.
        """
        if not self.is_asleep:
            return False
        else:
            self.sleep_count -= 1
            if random.randint(1, 2) == 2 or self.sleep_count <= 0:
                self.is_asleep = False
                self.sleep_count = 6
                self.model.text(f"You wake up!\n")
                return False
            else:
                self.model.text(f"You're still asleep...'\n")
                return True

    def attack_msg(self, did_crit, did_dodge, damage_dealt, enemy_name):
        """
        Display attack messages for the player.
        """
        if did_crit:
            self.model.text(f"\nYou attack with an excellent attack!!\n")
        else:
            self.model.text(f"\nYou attack!\n")

        if did_dodge and not did_crit:
            self.model.text(f"But the {enemy_name} dodged your attack!\n")
        else:
            self.model.text(f"You hit {enemy_name} for {damage_dealt} points of damage!\n")

    def has_herbs(self):
        return self.herb_count >=1
    
    def use_herb(self):
        """ Returns the amount healed """
        self.herb_count -= 1
        if self.current_hp >= self.max_hp:
            return 0       
        herb_hp = Randomizer.randint(*self.herb_range)
        actual_hp_gained = min(herb_hp, self.max_hp - self.current_hp)
        self.current_hp += actual_hp_gained
        return actual_hp_gained
    
    def is_flee_successful(self, enemy_agility, mod_select):
        """ Return True if the player flees successfully """
        enemy_run_modifiers = [0.25, 0.375, 0.75, 1]
        player_flee_chance = self.agility * Randomizer.randint(0, 254)
        enemy_block_chance = enemy_agility * Randomizer.randint(0, 254) * enemy_run_modifiers[mod_select]
        return player_flee_chance > enemy_block_chance



def player_factory():
    """
    Returns a player
    """
    return Player()
