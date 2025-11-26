# model.py - Default model for the simulation

from dataclasses import dataclass
from typing import Optional
from fightsim.models.player import Player
from fightsim.models.enemy import Enemy
from fightsim.models.combat_engine import CombatEngine

@dataclass
class GameState:
    """ Shared state container for game """
    player: Player
    enemy: Optional[Enemy] = None
    combat_engine: CombatEngine
    