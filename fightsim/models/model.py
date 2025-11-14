# model.py - Default model for the simulation

from typing import Optional
from fightsim.common.messages import ObserverMessages
from ..common.eventmanager import EventManager
from fightsim.models.player import Player # For type checking
from fightsim.models.enemy import Enemy, enemy_instances # For type checking
from fightsim.models.combat_engine import CombatEngine


class Model:
    """ Model class for the MVC pattern """
    def __init__(self, player: Optional[Player] = None, enemy: Optional[Enemy] = None, observer: EventManager = None, combat_engine: CombatEngine = None):
        self.combat_engine = combat_engine
        self.player: Player = player if player else Player()  # Add a player
        self.enemy: Optional[Enemy] = enemy if enemy else Enemy.create_dummy()
        self.observed: EventManager = observer if observer else EventManager("Generic Model Observer")
        

        self.clean_text: bool = False
        self.in_battle: bool = False  # Are we in battle mode or not? If not, we're in setup mode.
        self.initiative: bool = False  # Do we have initiative?
        self.crit_hit: bool = False  # Was there a critical hit?

        self.initialize_game()

    def initialize_game(self):
        """ Inject the model into player, reset battle variables, and notify the observer. """
        self.player.set_model(self)
        self.in_battle = False
        self.initiative = False
        self.crit_hit = False
        self.observed.notify(ObserverMessages.RESET_GAME)

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
            self.observed.notify(ObserverMessages.ENEMY_CHANGE)  # Notify observers about the change
        else:
            print("Searching for enemy")
            """Set the current enemy based on a key."""
            key = self.find_key_by_value(enemy_instances, enemy_name)
            print(f"The key is {key}")
            enemy_instance = enemy_instances.get(key)
            print(f"The enemy_instance is is {enemy_instance}")
            if enemy_instance:
                self.enemy = enemy_instance
                self.enemy.set_model(self)
                self.observed.notify(ObserverMessages.ENEMY_CHANGE)  # Notify observers about the change
            else:
                print("Selected an enemy that doesn't exist nor the default message. This should not happen!")
                self.enemy = None
        
    def change_player_hp(self, delta_hp):  # TODO, what if this hits zero? Maybe set up another subscriber.
        """Change the player's HP by a delta amount."""
        self.player.current_hp += delta_hp
        if self.player.max_hp < self.player.current_hp:
            self.player.current_hp = self.player.max_hp
        self.observed.notify(ObserverMessages.PLAYER_HP_CHANGE)  # Notify observers about the specific change

    def buy_herb(self):
        """Handles incrementing the herb count"""
        if self.player.herb_count < 6:
            self.text("Buying an herb.")
            self.player.herb_count += 1            
            return True
        self.text("You have the maximum number of herbs.")
        return False     

    def notify_armor_change(self):
        """ Notify there's been a change in armor """
        self.observed.notify(ObserverMessages.ARMOR_CHANGE)
    
    def notify_weapon_change(self):
        """ Notify there's been a change in weapon """
        self.observed.notify(ObserverMessages.WEAPON_CHANGE)

    def notify_shield_change(self):
        """ Notify there's been a change in shield """
        self.observed.notify(ObserverMessages.SHIELD_CHANGE)
   
    def text(self, output):
        """ Notify there is a message for the output window. """
        self.observed.notify(ObserverMessages.OUTPUT_CHANGE, output)

    def clear_output(self):
        """ Clear the output var"""
        self.observed.notify(ObserverMessages.OUTPUT_CLEAR)

    def clear_and_set_output(self, output):
        """ Clear out the output var, then add something new. Blanks the output window """        
        self.observed.notify(ObserverMessages.OUTPUT_CLEAR)
        self.observed.notify(ObserverMessages.OUTPUT_CHANGE, output)
                

if __name__ == '__main__':
    model = Model()
    print(model)
