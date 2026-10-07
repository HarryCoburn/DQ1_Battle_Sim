"""
enemy_actions.py - The actions an enemy can take, and the entries of its attack pattern.
"""
from enum import Enum, auto
from typing import NamedTuple


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


class PatternEntry(NamedTuple):
    """One special action in an enemy's pattern, tried with a weight% chance."""
    action: EnemyActions
    weight: int
