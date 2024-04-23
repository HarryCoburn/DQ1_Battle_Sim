# controller.py - Core controller for the simulation

from fightsim.common.messages import ObserverMessages
from .battle import Battle
import logging


class Controller:
    """ Main controller class"""

    def __init__(self, model, view, observer):
        self.logger = logging.getLogger(__name__)  # Get a module-level logger
        if not model or not view:
            self.logger.error("Model and View are required for Controller initialization.")
            raise ValueError("Model and View cannot be None.")

        self.model = model
        self.view = view
        self.observer = observer
        self.battle = Battle(self)
        self.spell_strings = []

        self.setup_observers()
        self.initialize_view()

    def setup_observers(self):
        """ Attach the controller as an observer to model events """
        messages = [
            ObserverMessages.ENEMY_CHANGE,
            ObserverMessages.WEAPON_CHANGE,
            ObserverMessages.ARMOR_CHANGE,
            ObserverMessages.SHIELD_CHANGE,
            ObserverMessages.OUTPUT_CHANGE,
            ObserverMessages.OUTPUT_CLEAR
        ]
        for message in messages:
            self.observer.attach(self, message)
            self.logger.debug(f"Attached controller to model with message: {message}")

    def initialize_view(self):
        self.model.text("DQ1 Battle Sim")
        self.logger.info("View initialized with welcome message.")

    def initial_update(self):
        self.view.update_player_info(self.model.player)
        self.battle.fight_over.trace('w', self.end_battle)

    def update_player_attribute(self, attribute_type, value):
        """ Generic method to update player attributes """
        try:
            if attribute_type == "weapon":
                self.model.player.equip_weapon(value)
            elif attribute_type == "armor":
                self.model.player.equip_armor(value)
            elif attribute_type == "shield":
                self.model.player.equip_shield(value)
            elif attribute_type == "level":
                self.model.player.level_up(value)
            elif attribute_type == "name":
                self.model.player.change_name(value)
            self.view.update_player_info(self.model.player)
            self.logger.info(f"Updated {attribute_type} to {value}")
        except Exception as e:
            self.logger.error(f"Failed to update {attribute_type}: {e}")

    def update_enemy(self, value):
        try:
            self.model.set_enemy(value)
            self.view.update_enemy_info(self.model.enemy)
            self.logger.info(f"Updated enemy to {value}")
        except Exception as e:
            self.logger.error(f"Failed to update enemy to {value}: {e}")

    def update_frame(self, *args):
        """ Tells view.ctrl_frame to change the frame"""
        self.view.ctrl_frame.show_frame(args[0])

    def start_battle(self, *_):
        print(f"Entering start_battle, enemy is {self.model.enemy}")
        """ Performs the handoff to battle.py for battle control"""
        if self.model.enemy is None:
            pass
        else:
            self.battle.setup_battle()

    def chosen_magic(self, *args):
        pass

    def end_battle(self, *_):
        """Cleans up after the battle is done and resets the simulator"""

        self.model.enemy.curr_hp = self.model.enemy.max_hp
        self.model.player.curr_hp = self.model.player.max_hp
        self.model.player.curr_mp = self.model.player.max_mp
        self.model.player.herb_count = 0
        self.view.main_frame.txt["state"] = "disabled"
        self.view.update_enemy_info(self.model.enemy)
        self.update_player_info()
        self.view.show_frame(self.view.setup_frame)

    def update(self, property_name, data=None):
        print(f"Received property_name {property_name}")
        # React to notifications from the model
        if property_name == ObserverMessages.SHIELD_CHANGE:
            self.view.update_player_info(self.model.player)
        if property_name == ObserverMessages.WEAPON_CHANGE:
            self.view.update_player_info(self.model.player)
        if property_name == ObserverMessages.ARMOR_CHANGE:
            self.view.update_player_info(self.model.player)
        if property_name == ObserverMessages.ENEMY_CHANGE:
            self.view.update_enemy_info(self.model.enemy)
        if property_name == ObserverMessages.OUTPUT_CHANGE:
            print(f"In update, data is {data}")
            self.view.update_output(property_name, data)
        if property_name == ObserverMessages.OUTPUT_CLEAR:
            self.view.clear_output()

    def update_text(self, text, *_):
        """
        Updates the main text box with output. When text is None, outputs the model and other
        debugging information
        """
        for line in text.output:
            self.view.append_output(line)

    def update_player_info(self, *_):
        """Tells the view to update the player label"""
        self.view.update_player_info(self.model.player)

    def update_enemy_info(self, *_):
        self.view.update_enemy_info(self.model.enemy)

    def buy_herb(self, *_):
        if self.model.buy_herb():
            self.view.update_player_info(self.model.player)
        # else:
        # self.view.show_message("Maximum herb count reached.")
