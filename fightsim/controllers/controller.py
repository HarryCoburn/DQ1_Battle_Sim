# controller.py - Core controller for the simulation

import logging

from fightsim.controllers.battle import Battle
from fightsim.common.spells import Spell
from fightsim.models.model import Model
from fightsim.views.view import View

# Module-level logger
logger = logging.getLogger(__name__)

class Controller:
    """ Main controller class"""

    def __init__(self, model: Model, view: View, rng):
        self.model = model
        self.view = view
        self.rng = rng
        self.battle: Battle | None = None

        self.initialize_view()

    def run(self) -> None:
        self.view.mainloop()

    def initialize_view(self):
        self.view.append_output("DQ1 Battle Sim")
        logger.info("View initialized with welcome message.")

    def initial_update(self):
        self.update_player_info()

    def update_enemy_info(self):
        self.view.update_enemy_info(self.model.enemy)

    def _active_battle(self) -> Battle:
        if self.battle is None:
            raise RuntimeError("Battle action called with no battle in progress")
        return self.battle

    def start_battle(self) -> None:
        self.battle = Battle(
            player=self.model.player,
            enemy=self.model.enemy,
            log=self.view.append_output,
            rng=self.rng,
            on_end=self.end_battle,
        )
        self.update_player_info()
        self.view.show_battle_screen()
        self.view.clear_output()
        self.battle.start_fight()

    def end_battle(self):
        """Cleans up after the battle is done and resets the simulator"""
        self.model.reset_after_battle()
        self.update_enemy_info()
        self.update_player_info()
        self.view.show_setup_screen()

    def attack(self) -> None:
        self._active_battle().take_turn(self._active_battle().player_attack)
        self.refresh()

    def use_herb(self) -> None:
        self._active_battle().take_turn(self._active_battle().use_herb)
        self.refresh()

    def flee(self) -> None:
        self._active_battle().take_turn(self._active_battle().player_flees)
        self.refresh()

    def cast_spell(self, label: str) -> None:
        if label not in Spell:
            self.view.append_output("You must select a spell first.")
            return
        self._active_battle().take_turn(lambda: self._active_battle().player_cast_magic(Spell(label)))
        self.refresh()

    def refresh(self) -> None:
        self.view.update_player_info(self.model.player)
        self.view.update_enemy_info(self.model.enemy)

    def update_player_info(self):
        """Updates the view with current player information from the model."""
        self.view.update_player_info(self.model.player)
        logger.info("Player info updated in the view.")

    # Setup actions

    def change_name(self, name: str) -> None:
        self.model.player.change_name(name)
        self.update_player_info()

    def set_level(self, level: int) -> None:
        self.model.player.level_up(level)
        self.update_player_info()

    def equip_weapon(self, name: str) -> None:
        self.model.player.equip_weapon(name)
        self.update_player_info()

    def equip_armor(self, name: str) -> None:
        self.model.player.equip_armor(name)
        self.update_player_info()

    def equip_shield(self, name: str) -> None:
        self.model.player.equip_shield(name)
        self.update_player_info()

    def buy_herb(self) -> None:
        if self.model.player.add_herb():
            self.view.append_output("Buying an herb.")
        else:
            self.view.append_output("You have the maximum number of herbs.")
        self.update_player_info()

    def select_enemy(self, name: str) -> None:
        self.model.set_enemy(name)
        self.update_enemy_info()
        logger.info("Selected enemy %s", name)
