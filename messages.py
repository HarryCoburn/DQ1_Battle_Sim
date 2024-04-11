from enum import Enum, auto

class ObserverMessages(Enum):
    OUTPUT_CHANGE = auto()
    OUTPUT_CLEAR = auto()
    ENEMY_CHANGE = auto()
    PLAYER_HP_CHANGE = auto()
    ARMOR_CHANGE = auto()
    WEAPON_CHANGE = auto()
    SHIELD_CHANGE = auto()
