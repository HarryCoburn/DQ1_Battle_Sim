# model.py - Default model for the simulation


from fightsim.models.player import Player
from fightsim.models.enemy import enemy_instances
from fightsim.common.messages import ObserverMessages


class ModelObserved:
    """ Observer Class for MVC model"""
    def __init__(self, name):
        self._observers = {}
        self._name = name        
        self.__repr__()

    def attach(self, observer, property_name):
        """ Attach an observer to a specific property"""
        if property_name not in self._observers:
            self._observers[property_name] = []
        self._observers[property_name].append(observer)

    def notify(self, property_name, data=None):
        """ Notify all the observers about a change to a specific property"""
        for observer in self._observers.get(property_name, []):
            observer.update(property_name, self, data)

    def detach(self, observer, property_name=None):
        """Detaches an observer"""
        if property_name:
            if property_name in self._observers and observer in self._observers[property_name]:
                self._observers[property_name].remove(observer)
        else:
            for key in self._observers.keys():
                if observer in self._observers[key]:
                    self._observers[key].remove(observer)            

    def __repr__(self):
        return f"{self._name} contains observers {str(self._observers)}"
        

class Model:
    """ Model class for the MVC pattern """
    def __init__(self):        
        self.player = Player()  # Add a player
        self.enemy = None  # Default enemy to make the rollover happy. Make a dummy enemy instead?
        self.clean_text = False
        self.in_battle = False  # Are we in battle mode or not? If not, we're in setup mode.
        self.initiative = False  # Do we have initiative?
        self.crit_hit = False  # Was there a critical hit?
        self.output = []  # The data list for the output label
        self.observed = ModelObserved("Model Observers")
        self.player.set_model(self)  # Inject the model into the player for reference.

    def __repr__(self):
        props = vars(self)
        return '\n'.join("%s : %s" % prop for prop in props.items())
    
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
        if enemy_name == "Select Enemy":
            self.enemy = None
            self.observed.notify(ObserverMessages.ENEMY_CHANGE)  # Notify observers about the change
        else:
            """Set the current enemy based on a key."""
            key = self.find_key_by_value(enemy_instances, enemy_name)
            enemy_instance = enemy_instances.get(key)
            if enemy_instance:
                self.enemy = enemy_instance
                self.observed.notify(ObserverMessages.ENEMY_CHANGE)  # Notify observers about the change
            else:
                print("Selected an enemy that doesn't exist nor the default message. This should not happen!")
        
    def change_player_hp(self, delta_hp):  # TODO, what if this hits zero? Maybe set up another subscriber.
        """Change the player's HP by a delta amount."""
        self.player.curr_hp += delta_hp
        if self.player.max_hp < self.player.curr_hp:
            self.player.curr_hp = self.player.max_hp
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

    # TODO    

    def clear_output(self):
        """ Clear the output var"""
        self.output = []  # Do I Need Now?
        self.observed.notify(ObserverMessages.OUTPUT_CLEAR)

    def clear_and_set_output(self, output):
        """ Clear out the output var, then add something new. Blanks the output window """        
        self.observed.notify(ObserverMessages.OUTPUT_CLEAR)
        self.observed.notify(ObserverMessages.OUTPUT_CHANGE, output)
                

if __name__ == '__main__':
    model = Model()
    print(model)
