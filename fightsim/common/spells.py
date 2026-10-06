"""
spells.py - Player spell names, shared by the battle engine and the view.
"""
from enum import StrEnum


class Spell(StrEnum):
    """Player battle spells. Values match the labels shown in the magic menu."""
    HEAL = "Heal"
    HURT = "Hurt"
    SLEEP = "Sleep"
    STOPSPELL = "Stopspell"
    HEALMORE = "Healmore"
    HURTMORE = "Hurtmore"
