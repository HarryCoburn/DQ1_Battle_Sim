"""
Player class
"""

from dataclasses import dataclass, field
from fightsim.models.items import Item, ItemType, items
from ..common.messages import ObserverMessages
from typing import List, Optional
from .player_leveling import _Levelling

CRIT_CHANCE: int = 32
SLEEP_COUNT: int = 6

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
    is_spellstopped: bool = False
    leveler: _Levelling = _Levelling()
    model: Optional = None  # Placeholder
    sleep_turns: int = 0


    @property
    def is_asleep(self) -> bool:
        return self.sleep_turns > 0

    def advance_sleep(self):
        self.sleep_turns -= 1

    def wake(self):
        self.sleep_turns = 0

    def fall_asleep(self):
        self.sleep_turns = SLEEP_COUNT

    def __post_init__(self):
        self.player_magic = []
        if not 1 <= self.level <= 30:
            raise ValueError("Level must be within 1 to 30")

    def defense(self):
        """
        Calculate and return defense value
        """
        return (self.agility // 2) + self.armor.modifier + self.shield.modifier

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

        self.strength, self.agility, self.max_hp, self.max_mp = self.leveler.adjust_stats(self.level, self.name)
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

    def take_damage(self, amount: int) -> int:
        dealt = min(amount, self.current_hp)
        self.current_hp -= dealt
        return dealt

    def heal(self, amount: int) -> int:
        healed = min(amount, self.max_hp - self.current_hp)
        self.current_hp += healed
        return healed

    def consume_herb(self):
        self.herb_count -= 1

    def consume_mp(self, cost):
        self.current_mp -= cost

    def restore(self):
        self.current_hp = self.max_hp
        self.current_mp = self.max_mp
        self.herb_count = 0
        self.wake()
        self.is_spellstopped = False


def player_factory():
    """
    Returns a player
    """
    return Player()
