# controller.py - Core controller for the simulation

from fightsim.common.messages import ObserverMessages
from .battle import Battle
import logging
from ..common.decorators import handle_errors
from ..common.attribute_type import AttributeType
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

class EnemyManager:
    def __init__(self, model, view):
        self.model = model
        self.view = view


    def update_enemy_info(self, value = None):
        if value is not None:
            self.model.set_enemy(value)
        self.view.update_enemy_info(self.model.enemy)
        logger.info(f"Updated enemy to {value}")


class Controller:
    """ Main controller class"""

    def __init__(self, model, view, observer, rng):
        self.logger = logging.getLogger(__name__)  # Get a module-level logger
        if not model or not view:
            logger.error("Model and View are required for Controller initialization.")
            raise ValueError("Model and View cannot be None.")

        self.model = model
        self.view = view
        self.rng = rng
        self.observer_manager = ObserverManager(observer)
        self.player_manager = PlayerManager(model, view)
        self.enemy_manager = EnemyManager(model, view)
        self.observer = observer
        self.battle = None
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

    def get_chosen_magic(self):
        return self.view.battle_frame.magic_option_var.get()

    def switch_battle_frame(self):
        self.view.show_frame(self.view.battle_frame)

    def clear_output(self):
        """ Clear the output var"""
        self.observer.notify(ObserverMessages.OUTPUT_CLEAR)

    def enable_main_frame_text(self):
        self.view.main_frame.txt["state"] = 'normal'

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
        self.enemy_manager.update_enemy_info()
        self.player_manager.update_player_info()
        self.view.show_frame(self.view.setup_frame)


    def player_surprised(self):
        self.model.text(f"""The {self.model.enemy.name} surprises you! They attack first!\n""")

    def player_wins(self):
        self.model.text(f"""You have defeated the {self.model.enemy.name}!\n""")

    def fleeing(self, succeed):
        self.model.text(f"You attempt to run away...\n")
        if succeed:
            self.model.text(f"You successfully flee!\n")
        else:
            self.model.text(f"""...but the {self.model.enemy.name} blocks you from running away!\n""")

    def attack(self) -> None:
        self.battle.take_turn(self.battle.player_attack)
        self.refresh()

    def use_herb(self) -> None:
        self.battle.take_turn(self.battle.use_herb)
        self.refresh()

    def flee(self) -> None:
        self.battle.take_turn(self.battle.player_flees)
        self.refresh()

    def cast_spell(self) -> None:
        spell = self.get_chosen_magic()
        self.battle.take_turn(lambda: self.battle.player_cast_magic(spell))
        self.refresh()

    def refresh(self) -> None:
        self.view.update_player_info(self.model.player)
        self.view.update_enemy_info(self.model.enemy)
