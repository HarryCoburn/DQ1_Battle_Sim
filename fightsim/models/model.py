# model.py - Default model for the simulation

from typing import Optional
from fightsim.common.messages import ObserverMessages
from ..common.eventmanager import EventManager
from fightsim.models.player import Player # For type checking
from fightsim.models.enemy import Enemy, create_enemy # For type checking
from fightsim.models.combat_engine import CombatEngine


class Model:
    """ Model class for the MVC pattern """
    def __init__(self, player: Optional[Player] = None, enemy: Optional[Enemy] = None, observer: EventManager = None, combat_engine: CombatEngine = None):
        self.combat_engine = combat_engine
        self.player: Player = player if player else Player()  # Add a player
        self.enemy: Optional[Enemy] = enemy if enemy else Enemy.create_dummy(combat_engine=combat_engine)
        self.observed: EventManager = observer if observer else EventManager("Generic Model Observer")    

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
        # print(f"Entering model.set_enemy, receiving {enemy_name}")
        if enemy_name == "Select Enemy":
            self.enemy = None
            self.observed.notify(ObserverMessages.ENEMY_CHANGE)  # Notify observers about the change
        else:
            # print("Searching for enemy")
            """Set the current enemy based on a key."""
            key = self.find_key_by_value(enemy_dict, enemy_name)
            #print(f"The key is {key}")
            # enemy_instance = enemy_instances.get(key)
            # print(f"The enemy_instance is is {enemy_instance}")
            if key:
                self.enemy = create_enemy(key, self.combat_engine)                
                self.observed.notify(ObserverMessages.ENEMY_CHANGE)  # Notify observers about the change
            else:
                # print("Selected an enemy that doesn't exist nor the default message. This should not happen!")
                self.enemy = None

    def buy_herb(self):
        """Handles incrementing the herb count"""
        if self.player.herb_count < 6:
            self.text("Buying an herb.")
            self.player.herb_count += 1            
            return True
        self.text("You have the maximum number of herbs.")
        return False         
   
    def text(self, output):
        """ Notify there is a message for the output window. """
        self.observed.notify(ObserverMessages.OUTPUT_CHANGE, output) 
                

if __name__ == '__main__':
    model = Model()
    print(model)
