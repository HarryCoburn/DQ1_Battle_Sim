from dataclasses import dataclass


@dataclass
class Item:
    name: str
    modifier: int

    def describe(self) -> str:
        return f"{self.name} (Modifier: {self.modifier}"


@dataclass
class Weapon(Item):
    pass


@dataclass
class Shield(Item):
    pass


@dataclass
class Armor(Item):
    reduce_hurt_damage: bool = False
    reduce_fire_damage: bool = False


weapon_dict = {
    "unarmed": {
        "name": "Unarmed",
        "modifier": 0
    },
    "bamboo_pole": {
        "name": "Bamboo Pole",
        "modifier": 2
    },
    "club": {
        "name": "Club",
        "modifier": 4
    },
    "copper_sword": {
        "name": "Copper Sword",
        "modifier": 10
    },
    "hand_axe": {
        "name": "Hand Axe",
        "modifier": 15
    },
    "broad_sword": {
        "name": "Broad Sword",
        "modifier": 20
    },
    "flame_sword": {
        "name": "Flame Sword",
        "modifier": 28
    },
    "edricks-sword": {
        "name": "Edrick's Sword",
        "modifier": 40
    }
}

armor_dict = {
    "naked": {
        "name": "Naked",
        "modifier": 0
    },
    "clothes": {
        "name": "Clothes",
        "modifier": 2
    },
    "leather_armor": {
        "name": "Leather Armor",
        "modifier": 4
    },
    "chain_mail": {
        "name": "Chain Mail",
        "modifier": 10
    },
    "half_plate": {
        "name": "Half Plate",
        "modifier": 16
    },
    "full_plate": {
        "name": "Full Plate",
        "modifier": 24
    },
    "magic_armor": {
        "name": "Magic Armor",
        "modifier": 2,
        "reduce_hurt_damage": True
    },
    "edricks_armor": {
        "name": "Edrick's Armor",
        "modifier": 2,
        "reduce_hurt_damage": True,
        "reduce_fire_damage": True
    }
}

shield_dict = {
    "no_shield": {
        "name": "No Shield",
        "modifier": 0
    },
    "small_shield": {
        "name": "Small Shield",
        "modifier": 4
    },
    "large_shield": {
        "name": "Large Shield",
        "modifier": 10
    },
    "silver_shield": {
        "name": "Silver Shield",
        "modifier": 25
    }
}

weapon_instances = {k: Weapon(**v) for k, v in weapon_dict.items()}
armor_instances = {k: Armor(**v) for k, v in armor_dict.items()}
shield_instances = {k: Shield(**v) for k, v in shield_dict.items()}

weapon_names = [weapon.name for weapon in weapon_instances.values()]
armor_names = [armor.name for armor in armor_instances.values()]
shield_names = [shield.name for shield in shield_instances.values()]
