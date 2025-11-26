from enum import Enum, auto
from dataclasses import dataclass

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
    