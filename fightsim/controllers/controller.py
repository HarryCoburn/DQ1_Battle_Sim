# controller.py - Core controller for the simulation

from fightsim.common.messages import ObserverMessages
from .battle import Battle
import logging
from ..common.decorators import handle_errors
from ..common.attribute_type import AttributeType
from ..common.spells import Spell

# Module-level logger
logger = logging.getLogger(__name__)

class ObserverManager:
    def __init__(self, observer):
        self.observer = observer


    def attach_observers(self, controller, messages):
        for message in messages:
            self.observer.attach(controller, message)
            logger.debug(f"Attached controller to model with message: {message}")

class PlayerManager:
    def __init__(self, model, view):
        self.model = model
        self.view = view


    def update_player_attribute(self, attribute_type, value=None):
        print(value)
        """ Generic method to update player attributes """
        update_methods = {
            AttributeType.WEAPON: self.model.player.equip_weapon,
            AttributeType.ARMOR: self.model.player.equip_armor,
            AttributeType.SHIELD: self.model.player.equip_shield,
            AttributeType.LEVEL: self.model.player.level_up,
            AttributeType.NAME: self.model.player.change_name,
            AttributeType.HERB: self.model.buy_herb
        }

        if attribute_type in update_methods:
            if attribute_type == AttributeType.HERB:
                update_methods[attribute_type]()
            else:
                update_methods[attribute_type](value)
            self.update_player_info()
            logger.info(f"Updated {attribute_type} to {value}")
        else:
            logger.warning(f"Unknown attribute type: {attribute_type}")


    def update_player_info(self):
        """Updates the view with current player information from the model."""
        self.view.update_player_info(self.model.player)
        logger.info("Player info updated in the view.")

class Controller:
    """ Main controller class"""

    def __init__(self, model, view, observer, rng):
        if not model or not view:
            logger.error("Model and View are required for Controller initialization.")
            raise ValueError("Model and View cannot be None.")

        self.model = model
        self.view = view
        self.rng = rng
        self.observer_manager = ObserverManager(observer)
        self.player_manager = PlayerManager(model, view)
        self.observer = observer
        self.battle: Battle | None = None
        self.messages = [
            ObserverMessages.OUTPUT_CHANGE,
            ObserverMessages.OUTPUT_CLEAR,
            ObserverMessages.UPDATE_PLAYER_MAGIC
        ]

        self.setup_observers()
        self.initialize_view()

    def run(self) -> None:
        self.view.mainloop()

    def setup_observers(self):
        """ Attach the controller as an observer to model events """
        self.observer_manager.attach_observers(self, self.messages)

    def initialize_view(self):
        self.model.text("DQ1 Battle Sim")
        logger.info("View initialized with welcome message.")

    def initial_update(self):
        self.player_manager.update_player_info()


    def update(self, property_name, data=None):
        if property_name == ObserverMessages.OUTPUT_CHANGE:
            self.view.update_output(property_name, data)
        if property_name == ObserverMessages.OUTPUT_CLEAR:
            self.view.clear_output()
        if property_name == ObserverMessages.UPDATE_PLAYER_MAGIC:
            self.view.battle_frame.update_player_magic_menu()

    def update_enemy_info(self, value = None):
        if value is not None:
            self.model.set_enemy(value)
        self.view.update_enemy_info(self.model.enemy)
        logger.info(f"Updated enemy to {value}")

    def get_chosen_magic(self):
        return self.view.battle_frame.magic_option_var.get()

    def switch_battle_frame(self):
        self.view.show_frame(self.view.battle_frame)

    def clear_output(self):
        """ Clear the output var"""
        self.observer.notify(ObserverMessages.OUTPUT_CLEAR)

    def enable_main_frame_text(self):
        self.view.main_frame.txt["state"] = 'normal'

    def _active_battle(self) -> Battle:
        if self.battle is None:
            raise RuntimeError("Battle action called with no battle in progress")
        return self.battle

    def prepare_battle(self):
        self.player_manager.update_player_info()
        self.switch_battle_frame()
        self.clear_output()

    def start_battle(self) -> None:
        self.battle = Battle(
            player=self.model.player,
            enemy=self.model.enemy,
            log=self.model.text,
            rng=self.rng,
            on_end=self.end_battle,
        )
        self.prepare_battle()
        self.enable_main_frame_text()
        self.battle.start_fight()

    def end_battle(self):
        """Cleans up after the battle is done and resets the simulator"""
        self.model.enemy.current_hp = self.model.enemy.max_hp
        self.model.player.current_hp = self.model.player.max_hp
        self.model.player.current_mp = self.model.player.max_mp
        self.model.player.herb_count = 0
        self.view.main_frame.txt["state"] = "disabled"
        self.update_enemy_info()
        self.player_manager.update_player_info()
        self.view.show_frame(self.view.setup_frame)

    def attack(self) -> None:
        self._active_battle().take_turn(self.battle.player_attack)
        self.refresh()

    def use_herb(self) -> None:
        self._active_battle().take_turn(self.battle.use_herb)
        self.refresh()

    def flee(self) -> None:
        self._active_battle().take_turn(self.battle.player_flees)
        self.refresh()

    def cast_spell(self) -> None:
        label = self.get_chosen_magic()
        if label not in Spell:
            self.model.text("You must select a spell first.\n")
            return
        self._active_battle().take_turn(lambda: self._active_battle().player_cast_magic(Spell(label)))
        self.refresh()

    def refresh(self) -> None:
        self.view.update_player_info(self.model.player)
        self.view.update_enemy_info(self.model.enemy)
