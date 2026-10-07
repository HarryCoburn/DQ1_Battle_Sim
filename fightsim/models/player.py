"""
Player class
"""

from dataclasses import dataclass, field
from fightsim.models.items import Item, ItemType, items
from ..common.spells import Spell
from typing import Optional
from .player_leveling import _Levelling

CRIT_CHANCE: int = 32
SLEEP_COUNT: int = 6
MAX_HERBS: int = 6

# Level at which the player learns each spell
SPELL_LEVELS: dict[Spell, int] = {
    Spell.HEAL: 3,
    Spell.HURT: 4,
    Spell.SLEEP: 7,
    Spell.STOPSPELL: 10,
    Spell.HEALMORE: 17,
    Spell.HURTMORE: 19,
}

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

    @property
    def player_magic(self) -> list[Spell]:
        """Spells the player knows at the current level."""
        return [spell for spell, level in SPELL_LEVELS.items() if self.level >= level]

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

    def add_herb(self) -> bool:
        """Adds an herb unless the player already has the maximum. Returns True if one was added."""
        if self.herb_count >= MAX_HERBS:
            return False
        self.herb_count += 1
        return True

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
