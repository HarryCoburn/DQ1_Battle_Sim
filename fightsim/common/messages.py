from enum import Enum, auto


class ObserverMessages(Enum):
    """
    Observer Messages for sending commands
    """
    OUTPUT_CHANGE = auto()
    OUTPUT_CLEAR = auto()
    ENEMY_CHANGE = auto()
    PLAYER_HP_CHANGE = auto()
    WEAPON_CHANGE = auto()
    SHIELD_CHANGE = auto()
    ARMOR_CHANGE = auto()
    RESET_GAME = auto()


# Enemy Actions
class EnemyActions(Enum):
    """
    Actions that the Enemy class can take. Add to this to make new Enemy attacks
    """
    ATTACK = auto()
    HEAL = auto()
    HURT = auto()
    SLEEP = auto()
    STOPSPELL = auto()
    FIRE = auto()
    HEALMORE = auto()
    HURTMORE = auto()
    STRONGFIRE = auto()
