# model.py - Default model for the simulation

from typing import Optional
from fightsim.models.player import Player # For type checking
from fightsim.models.enemy import Enemy, create_enemy



class Model:
    """ Model class for the MVC pattern """
    def __init__(self, player: Optional[Player] = None, enemy: Optional[Enemy] = None):
        self.player: Player = player if player else Player()  # Add a player
        self.enemy: Optional[Enemy] = enemy if enemy else Enemy.create_dummy()

        self.clean_text: bool = False
        self.in_battle: bool = False  # Are we in battle mode or not? If not, we're in setup mode.
        self.initiative: bool = False  # Do we have initiative?
        self.crit_hit: bool = False  # Was there a critical hit?

        self.initialize_game()

    def initialize_game(self):
        """ Reset battle variables. """
        self.in_battle = False
        self.initiative = False
        self.crit_hit = False

    def __repr__(self):
        props = vars(self)
        return '\n'.join(f"{key}: {value}" for key, value in props.items())

    @staticmethod
    def find_key_by_value(d, value_to_find):
        """
        Find key by value in a dictionary. Used for item and enemy lookups.
        """
        for key, value in d.items():
            if value.name == value_to_find:
                return key
        return None

    def set_enemy(self, enemy_name):
        print(f"Entering model.set_enemy, receiving {enemy_name}")
        if enemy_name == "Select Enemy":
            self.enemy = None
        else:
            """Set the current enemy to a fresh instance by name."""
            try:
                self.enemy = create_enemy(enemy_name)
            except KeyError:
                raise ValueError(f"Unknown enemy name: {enemy_name!r}") from None

    def change_player_hp(self, delta_hp):  # TODO, what if this hits zero?
        """Change the player's HP by a delta amount."""
        self.player.current_hp += delta_hp
        if self.player.max_hp < self.player.current_hp:
            self.player.current_hp = self.player.max_hp

    def reset_after_battle(self):
        if self.enemy is not None:
            self.enemy = create_enemy(self.enemy.name)
        self.player.restore()


if __name__ == '__main__':
    model = Model()
    print(model)
