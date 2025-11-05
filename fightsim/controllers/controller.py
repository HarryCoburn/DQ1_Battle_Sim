# controller.py - Core controller for the simulation

from fightsim.common.messages import ObserverMessages
from ..models.battle import BattleEngine
import logging
from ..common.decorators import handle_errors


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
        self.battle = BattleEngine(self)

        self.setup_observers()
        self.initialize_view()

    def setup_observers(self):
        """ Attach the controller as an observer to model events """
        messages = [
            ObserverMessages.OUTPUT_CHANGE,
            ObserverMessages.OUTPUT_CLEAR,
            ObserverMessages.UPDATE_PLAYER_MAGIC
        ]
        for message in messages:
            self.observer.attach(self, message)
            self.logger.debug(f"Attached controller to model with message: {message}")

    def initialize_view(self):
        self.model.text("DQ1 Battle Sim")
        self.logger.info("View initialized with welcome message.")

    def update_player_attribute(self, attribute_type, value=None):
        """ Generic method to update player attributes """
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
        elif attribute_type == "herb":
            self.model.buy_herb()
        self.view.update_player_info(self.model.player)        
        self.logger.info(f"Updated {attribute_type} to {value}")


    def update_enemy(self, value):
        self.model.set_enemy(value)
        self.view.update_enemy_info(self.model.enemy)
        self.logger.info(f"Updated enemy to {value}")

    def initial_update(self):
        self.view.update_player_info(self.model.player)        

    def update(self, property_name, data=None):
        if property_name == ObserverMessages.OUTPUT_CHANGE:
            self.view.update_output(property_name, data)
        if property_name == ObserverMessages.OUTPUT_CLEAR:
            self.view.clear_output()
        if property_name == ObserverMessages.UPDATE_PLAYER_MAGIC:
            self.view.battle_frame.update_player_magic_menu()

    # def update_player_info(self):
    #     """Updates the view with current player information from the model."""
    #     self.view.update_player_info(self.model.player)
    #     self.logger.info("Player info updated in the view.")

    # def update_enemy_info(self):
    #     self.view.update_enemy_info(self.model.enemy)

    def get_chosen_magic(self):
        return self.view.battle_frame.magic_option_var.get()

    def switch_battle_frame(self):
        self.view.show_frame(self.view.battle_frame)

    def clear_output(self):
        """ Clear the output var"""
        self.observer.notify(ObserverMessages.OUTPUT_CLEAR)

    def enable_main_frame_text(self):
        self.view.main_frame.txt["state"] = 'normal'
   
    
    
    
