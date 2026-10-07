"""
controller.py - Connects the view's actions to the model and runs battles.
"""
import logging
import random

from fightsim.controllers.battle import Battle
from fightsim.common.spells import Spell
from fightsim.models.model import Model
from fightsim.views.view import View

# Module-level logger
logger = logging.getLogger(__name__)

class Controller:
    """ Main controller class"""

    def __init__(self, model: Model, view: View, rng: random.Random):
        self.model = model
        self.view = view
        self.rng = rng
        self.battle: Battle | None = None

    def run(self) -> None:
        self.view.mainloop()

    def initial_update(self) -> None:
        """Shows the welcome message and the starting player and enemy."""
        self.view.append_output("DQ1 Battle Sim")
        self._refresh()

    def _refresh(self) -> None:
        """Redraws the player and enemy information from the model."""
        self.view.update_player_info(self.model.player)
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
        self._refresh()
        self.view.show_battle_screen()
        self.view.clear_output()
        self.battle.start_fight()

    def end_battle(self):
        """Cleans up after the battle is done and resets the simulator"""
        self.battle = None
        self.model.reset_after_battle()
        self._refresh()
        self.view.show_setup_screen()

    def attack(self) -> None:
        self._active_battle().take_turn(self._active_battle().player_attack)
        self._refresh()

    def use_herb(self) -> None:
        self._active_battle().take_turn(self._active_battle().use_herb)
        self._refresh()

    def flee(self) -> None:
        self._active_battle().take_turn(self._active_battle().player_flees)
        self._refresh()

    def cast_spell(self, label: str) -> None:
        if label not in Spell:
            self.view.append_output("You must select a spell first.")
            return
        self._active_battle().take_turn(lambda: self._active_battle().player_cast_magic(Spell(label)))
        self._refresh()

    # Setup actions

    def change_name(self, name: str) -> None:
        self.model.player.change_name(name)
        self._refresh()

    def set_level(self, level: int) -> None:
        self.model.player.set_level(level)
        self._refresh()

    def equip_weapon(self, name: str) -> None:
        self.model.player.equip_weapon(name)
        self._refresh()

    def equip_armor(self, name: str) -> None:
        self.model.player.equip_armor(name)
        self._refresh()

    def equip_shield(self, name: str) -> None:
        self.model.player.equip_shield(name)
        self._refresh()

    def buy_herb(self) -> None:
        if self.model.player.add_herb():
            self.view.append_output("Buying an herb.")
        else:
            self.view.append_output("You have the maximum number of herbs.")
        self._refresh()

    def select_enemy(self, name: str) -> None:
        self.model.set_enemy(name)
        self._refresh()
        logger.info("Selected enemy %s", name)
