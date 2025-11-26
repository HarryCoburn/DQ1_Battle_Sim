from dataclasses import dataclass, field
from .spells import SpellType
from ..common.messages import EnemyActions

@dataclass
class GameConstants:
    crit_chance: int = 32
    enemy_sleep_rounds: int = 2
    heal_ranges: dict = field(default_factory=lambda: {
        SpellType.HEAL: (10,17),
        SpellType.HEALMORE: (58, 85)
    })
    hurt_ranges: dict = field(default_factory=lambda: {
        SpellType.HURT: (5,12),
        SpellType.HURTMORE: (58, 65)
    })
    herb_range: tuple = (23,30)
    enemy_dodge_limit: int = 64
    enemy_resist_limit: int = 16
    enemy_flee_limit: int = 4
    enemy_wakeup_limit: int = 3
    enemy_hurt_ranges: dict = field(default_factory=lambda: {
        EnemyActions.HURT: ([3,10], [2,6]),
        EnemyActions.HURTMORE: ([30,45], [20,30])
    })
    enemy_breathes_fire_ranges: dict = field(default_factory=lambda: {
        EnemyActions.FIRE: ([16,23], [10,4]),
        EnemyActions.STRONGFIRE: ([65,72], [42,48])
    })
    enemy_heal_ranges: dict = field(default_factory=lambda: {
        EnemyActions.HEAL: (20, 27),
        EnemyActions.HEALMORE: (85, 100)
    })
    enemy_spellstop_limit: int = 2
