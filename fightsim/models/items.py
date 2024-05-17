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
    item_type: ItemType
    reduce_hurt_damage: bool = False
    reduce_fire_damage: bool = False

    def describe(self) -> str:
        return f"{self.name} (Modifier: {self.modifier})"


def create_item(item_type: ItemType, item_name: str, item_data: dict) -> Item:
    return Item(
        name=item_name,
        modifier=item_data["modifier"],
        item_type=item_type,
        reduce_hurt_damage=item_data.get("reduce_hurt_damage", False),
        reduce_fire_damage=item_data.get("reduce_fire_damage", False)
    )


item_data = {
    "weapons": {
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
    "armors": {
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
    "shields": {
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


items = {
    item_type.value: {
        name: create_item(item_type, name, data) for name, data in item_data[item_type.value + "s"].items()
    }
    for item_type in ItemType
}

weapon_names = [item.name for item in items[ItemType.WEAPON.value].values()]
armor_names = [item.name for item in items[ItemType.ARMOR.value].values()]
shield_names = [item.name for item in items[ItemType.SHIELD.value].values()]

