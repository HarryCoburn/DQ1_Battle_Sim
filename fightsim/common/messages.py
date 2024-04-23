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

    def description(self):
        descriptions = {
            # TODO
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
            EnemyActions.HURT: "Enemy casts the Hurt spell.",
            EnemyActions.SLEEP: "Enemy casts the Sleep spell.",
            EnemyActions.STOPSPELL: "Enemy casts the Stopspell spell.",
            EnemyActions.FIRE: "Enemy uses a fiery breath attack.",
            EnemyActions.HEALMORE: "Enemy casts the Healmore spell.",
            EnemyActions.HURTMORE: "Enemy casts the Hurtmore spell.",
            EnemyActions.STRONGFIRE: "Enemy uses a strong fiery breath attack."
        }
        return descriptions.get(self, "No description available.")
