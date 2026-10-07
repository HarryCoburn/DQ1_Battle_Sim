"""
model.py - The current player and enemy.
"""
from fightsim.models.player import Player
from fightsim.models.enemy import Enemy, create_enemy


class Model:
    """ Model class for the MVC pattern """
    def __init__(self, player: Player | None = None, enemy: Enemy | None = None):
        self.player: Player = player if player is not None else Player()
        self.enemy: Enemy | None = enemy  # None until one is chosen

    def __repr__(self):
        props = vars(self)
        return '\n'.join(f"{key}: {value}" for key, value in props.items())

    def set_enemy(self, enemy_name: str | None):
        """Set the current enemy to a fresh instance by name, or clear it with None."""
        if enemy_name is None:
            self.enemy = None
            return
        try:
            self.enemy = create_enemy(enemy_name)
        except KeyError:
            raise ValueError(f"Unknown enemy name: {enemy_name!r}") from None

    def reset_after_battle(self):
        if self.enemy is not None:
            self.enemy = create_enemy(self.enemy.name)
        self.player.restore()
