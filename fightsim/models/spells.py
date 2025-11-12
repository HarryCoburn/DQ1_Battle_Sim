from dataclasses import dataclass
from enum import Enum

@dataclass
class SpellData:
    name: str
    mp_cost: int
    level_required: int

class SpellType(Enum):
    # Spell name, MP requirement, Level requirement
    HEAL = SpellData("Heal", 4, 3)
    HEALMORE = SpellData("Healmore", 10, 17)
    HURT = SpellData("Hurt", 2, 4)
    HURTMORE = SpellData("Hurtmore", 5, 19)
    SLEEP = SpellData("Sleep", 2, 7)
    STOPSPELL = SpellData("Stopspell", 2, 10)