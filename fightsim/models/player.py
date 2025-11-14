"""
Player class
"""

import random
from typing import List, Optional
from dataclasses import dataclass, field
from fightsim.models.items import Item, ItemType, items
from ..common.messages import SpellFailureReason
from .player_leveling import _Levelling
from ..common.randomizer import Randomizer
from .spells import SpellType
from .combat_engine import CombatEngine

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
    herb_range: tuple = (23, 30)
    randomizer: Optional[Randomizer] = None
    combat_engine: Optional[CombatEngine] = None

    def __post_init__(self):
        self.player_magic = []
        if not 1 <= self.level <= 30:
            raise ValueError("Level must be within 1 to 30")

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
            for spell in SpellType:
                if self.level >= spell.value.level_required:
                    self.player_magic.append(spell)

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

    def attack(self, enemy):
        return self.combat_engine.resolve_player_attack(
            player_strength=self.strength,
            player_weapon=self.weapon.modifier,
            enemy_agility=enemy.agility,
            enemy_dodge_chance=enemy.dodge,
            enemy_blocks_crits=enemy.void_critical_hit,
        )

    # Herb usage

    def has_herbs(self):
        return self.herb_count >= 1

    def use_herb(self):
        """Returns the amount healed"""
        self.herb_count -= 1
        if self.current_hp >= self.max_hp:
            return HerbResult(success=False, healing=0, reason="max_hp")
        herb_hp = self.randomizer.randint(*self.herb_range)
        actual_hp_gained = min(herb_hp, self.max_hp - self.current_hp)

        return HerbResult(success=True, healing=actual_hp_gained)

    # Magic Usage

    def cast_magic(self, spell, enemy, combat_engine):
        spell_switch = {
            SpellType.HEAL: lambda: combat_engine.player_casts_heal(
                spell=spell, heal_max=(self.max_hp - self.current_hp)
            ),
            SpellType.HEALMORE: lambda: combat_engine.player_casts_heal(
                spell=spell, heal_max=(self.max_hp - self.current_hp)
            ),
            SpellType.HURT: lambda: combat_engine.player_casts_hurt(
                spell, enemy.hurt_resist
            ),
            SpellType.HURTMORE: lambda: combat_engine.player_casts_hurt(
                spell, enemy.hurt_resist
            ),
            SpellType.SLEEP: lambda: combat_engine.player_casts_sleep(
                spell, enemy.enemy_sleep_count, enemy.sleep_resist
            ),
            SpellType.STOPSPELL: combat_engine.player_casts_stopspell(
                spell, enemy.enemy_spell_stopped, enemy.enemy_stopspell_resist
            ),
        }

        magic_check = combat_engine.resolve_player_magic(
            spell, self.current_mp, self.is_spellstopped
        )
        if magic_check.success is False:
            if magic_check.reason == SpellFailureReason.PLAYER_SPELLSTOPPED:
                self.current_mp -= spell.value.mp_cost
                return magic_check
            else:  # Not enough MP
                return magic_check

        self.current_mp -= spell.value.mp_cost
        spell_function = spell_switch.get(spell, lambda: None)
        spell_function()

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
        player_flee_chance = self.agility * self.randomizer.randint(0, 254)
        enemy_block_chance = (
            enemy_agility
            * self.randomizer.randint(0, 254)
            * enemy_run_modifiers[mod_select]
        )
        return player_flee_chance > enemy_block_chance

    # Misc stats

    def resist(self, chance):
        return self.randomizer.randint(1, 16) <= chance

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


def player_factory(combat_engine):
    """
    Returns a player
    """
    return Player(
        randomizer=Randomizer(),
        combat_engine=combat_engine        
    )
