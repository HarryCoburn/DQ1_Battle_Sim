"""
items.py - Weapons, armor and shields, and their stats.
"""
from dataclasses import dataclass
from enum import Enum


class ItemType(Enum):
    WEAPON = "weapon"
    SHIELD = "shield"
    ARMOR = "armor"


@dataclass
class Item:
    name: str
    modifier: int
    reduce_hurt_damage: bool = False
    reduce_fire_damage: bool = False


ITEM_DATA = {
    ItemType.WEAPON: {
        "Unarmed": {
            "modifier": 0
        },
        "Bamboo Pole": {
            "modifier": 2
        },
        "Club": {
            "modifier": 4
        },
        "Copper Sword": {
            "modifier": 10
        },
        "Hand Axe": {
            "modifier": 15
        },
        "Broad Sword": {
            "modifier": 20
        },
        "Flame Sword": {
            "modifier": 28
        },
        "Edrick's Sword": {
            "modifier": 40
        }
    },
    ItemType.ARMOR: {
        "Naked": {
            "modifier": 0
        },
        "Clothes": {
            "modifier": 2
        },
        "Leather Armor": {
            "modifier": 4
        },
        "Chain Mail": {
            "modifier": 10
        },
        "Half Plate": {
            "modifier": 16
        },
        "Full Plate": {
            "modifier": 24
        },
        "Magic Armor": {
            "modifier": 2,
            "reduce_hurt_damage": True
        },
        "Edrick's Armor": {
            "modifier": 2,
            "reduce_hurt_damage": True,
            "reduce_fire_damage": True
        }
    },
    ItemType.SHIELD: {
        "No Shield": {
            "modifier": 0
        },
        "Small Shield": {
            "modifier": 4
        },
        "Large Shield": {
            "modifier": 10
        },
        "Silver Shield": {
            "modifier": 25
        }
    }
}


items: dict[ItemType, dict[str, Item]] = {
    item_type: {name: Item(name=name, **data) for name, data in by_name.items()}
    for item_type, by_name in ITEM_DATA.items()
}

weapon_names = list(items[ItemType.WEAPON])
armor_names = list(items[ItemType.ARMOR])
shield_names = list(items[ItemType.SHIELD])

