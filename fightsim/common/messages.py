from enum import Enum, auto
from dataclasses import dataclass

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
    UPDATE_PLAYER_MAGIC = auto()

    def description(self):
        descriptions = {
            ObserverMessages.OUTPUT_CLEAR: "Clears the output window.",
            ObserverMessages.OUTPUT_CHANGE: "Appends new data to the output window.",
            ObserverMessages.ENEMY_CHANGE: "The enemy has changed",
            ObserverMessages.PLAYER_HP_CHANGE: "The player's Hit Points have changed.",
            ObserverMessages.WEAPON_CHANGE: "The player's weapon has changed.",
            ObserverMessages.SHIELD_CHANGE: "The player's shield has changed.",
            ObserverMessages.ARMOR_CHANGE: "The player's armor has changed.",
            ObserverMessages.RESET_GAME: "Resets the game.",
            ObserverMessages.UPDATE_PLAYER_MAGIC: "Updates the player magic menu"
        }
        return descriptions.get(self, "No description available.")


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

    def description(self):
        descriptions = {
            EnemyActions.ATTACK: "Enemy performs a basic attack.",
            EnemyActions.HEAL: "Enemy casts the Heal spell.",
            EnemyActions.HURT: "Hurt",
            EnemyActions.SLEEP: "Enemy casts the Sleep spell.",
            EnemyActions.STOPSPELL: "Enemy casts the Stopspell spell.",
            EnemyActions.FIRE: "Enemy uses a fiery breath attack.",
            EnemyActions.HEALMORE: "Enemy casts the Healmore spell.",
            EnemyActions.HURTMORE: "Hurtmore",
            EnemyActions.STRONGFIRE: "Enemy uses a strong fiery breath attack."
        }
        return descriptions.get(self, "No description available.")

class SpellFailureReason(Enum):
    NOT_ENOUGH_MP = auto()
    PLAYER_SPELLSTOPPED = auto()
    HEALED_AT_MAX_HP = auto()
    ENEMY_RESISTED_HURT = auto()
    ENEMY_ALREADY_ASLEEP = auto()
    ENEMY_RESISTED_SLEEP = auto()
    ENEMY_ALREADY_SPELLSTOPPED = auto()
    ENEMY_RESISTED_SPELLSTOP = auto()
    ENEMY_SPELLSTOPPED = auto()

class HerbFailureReason(Enum):
    NO_HERBS = auto()
    MAX_HP = auto()

@dataclass
class HerbResult:
    success: bool
    healing: int
    reason: str = ""

class SleepReason(Enum):
    NOT_ASLEEP = auto()
    FIRST_ROUND_ENEMY_ASLEEP = auto()
    ENEMY_WAKES_UP = auto()
    ENEMY_ASLEEP = auto()
    