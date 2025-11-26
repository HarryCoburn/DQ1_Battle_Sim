# controller.py - Core controller for the simulation

import logging
from ..models.enemy_data import enemy_name_to_key
from ..models.enemy import create_enemy


class Controller:
    """ Main controller class"""

    def __init__(self, game_state, view):
        self.logger = logging.getLogger(__name__)  # Get a module-level logger
        if not game_state or not view:
            self.logger.error("Model and View are required for Controller initialization.")
            raise ValueError("Model and View cannot be None.")

        self.game_state = game_state
        self.view = view
        self.initialize_view()
   
    def initialize_view(self):
        self.view.update_output(None, "DQ1 Battle Sim")
        self.logger.info("View initialized with welcome message.")

    def update_player_attribute(self, attribute_type, value=None):
        """ Generic method to update player attributes """
        if attribute_type == "weapon":
            self.game_state.player.equip_weapon(value)
        elif attribute_type == "armor":
            self.game_state.player.equip_armor(value)
        elif attribute_type == "shield":
            self.game_state.player.equip_shield(value)
        elif attribute_type == "level":
            self.game_state.player.level_up(value)
            self.view.battle_frame.update_player_magic_menu()
        elif attribute_type == "name":
            self.game_state.player.change_name(value)
        elif attribute_type == "herb":
            success = self.game_state.player.add_herb()
            if success:
                self.view.update_output(None, "Buying an herb.")
            else:
                self.view.update_output(None, "You have the maximum number of herbs.")

        self.view.update_player_info(self.game_state.player)        
        self.logger.info(f"Updated {attribute_type} to {value}")

    def update_enemy(self, name):
        # Handle no enemy selected
        if name == "Select Enemy":
            self.game_state.enemy = None
        # Find the enemy
        key = enemy_name_to_key(name)
        if key:
            self.game_state.enemy = create_enemy(key, self.game_state.combat_engine)
        else:
            self.game_state.enemy = None
        
        self.view.update_enemy_info(self.game_state.enemy)
        self.logger.info(f"Updated enemy to {self.game_state.enemy}")
    

    def initial_update(self):
        self.view.update_player_info(self.game_state.player)            

    def get_chosen_magic(self):
        return self.view.battle_frame.magic_option_var.get()

    def switch_battle_frame(self):
        self.view.show_frame(self.view.battle_frame)

    def clear_output(self):
        """ Clear the output var"""
        self.view.clear_output()

    def enable_main_frame_text(self):
        self.view.main_frame.txt["state"] = 'normal'
   
    
    
    
