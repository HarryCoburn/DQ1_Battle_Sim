# controller.py - Core controller for the simulation

from fightsim.models.model import ModelObserved
from fightsim.common.messages import ObserverMessages


class Controller:
    """ Main controller class"""

    def __init__(self, model, view):
        self.model = model
        self.view = view

        # self.output = model.output
        # self.output.attach(self)
        # self.output.output = "DQ1 Battle Sim"

        self.model.observed.attach(self, ObserverMessages.ENEMY_CHANGE)
        self.model.observed.attach(self, ObserverMessages.WEAPON_CHANGE)
        self.model.observed.attach(self, ObserverMessages.ARMOR_CHANGE)
        self.model.observed.attach(self, ObserverMessages.SHIELD_CHANGE)
        self.model.observed.attach(self, ObserverMessages.OUTPUT_CHANGE)
        self.model.observed.attach(self, ObserverMessages.OUTPUT_CLEAR)

        self.view.name_text.trace('w', self.update_name)
        self.view.level_change.trace('w', self.update_level)
        self.view.chosen_weapon.trace('w', self.update_weapon)
        self.view.chosen_armor.trace('w', self.update_armor)
        self.view.chosen_shield.trace('w', self.update_shield)
        self.view.chosen_enemy.trace('w', self.update_enemy)
        self.spell_strings = []

    def initial_update(self):
        self.view.update_player_info(self.model.player)
        # self.battle = battle.Battle(self.model, self.view)
        # self.view.frames[View.SetupFrame].buy_herb_button.bind("<Button-1>", self.herb_inc)
        # self.view.frames[self.view.frames.SetupFrame].start_fight_button.bind("<Button-1>", self.start_battle)
        # self.view.frames[self.view.BattleFrame].show_model_btn.bind("<Button-1>", self.update_text)
        # self.battle.fight_over.trace('w', self.end_battle)

    def update_armor(self, *_):
        # called when armor dropdown changes
        selected_armor = self.view.chosen_armor.get()
        self.model.player.equip_armor(selected_armor)

    def update_weapon(self, *_):
        # called when armor dropdown changes
        selected_weapon = self.view.chosen_weapon.get()
        self.model.player.equip_weapon(selected_weapon)

    def update_shield(self, *_):
        # called when armor dropdown changes
        selected_shield = self.view.chosen_shield.get()
        self.model.player.equip_shield(selected_shield)

    def update_enemy(self, *_):
        # called when enemy dropdown changes
        selected_enemy = self.view.chosen_enemy.get()
        self.model.set_enemy(selected_enemy)

    def update_frame(self, *args):
        ''' Tells view.ctrl_frame to change the frame'''
        self.view.ctrl_frame.show_frame(args[0])

    def start_battle(self, *_):
        """ Performs the handoff to battle.py for battle control"""
        if self.model.enemy is None:
            pass
        else:
            self.battle.setup_battle()

    def chosen_magic(self, *args):
        pass

    def end_battle(self, *_):
        """Cleans up after the battle is done and resets the simulator"""
        self.model.enemy = None
        self.model.enemy["hp"] = self.model.player["maxhp"]
        self.model.player["mp"] = self.model.player["maxmp"]
        self.model.player["herb_count"] = 0
        self.view.main_frame.txt["state"] = "disabled"
        self.update_enemy()
        self.update_player_info()
        self.view.show_frame(self.view.frames.SetupFrame)

    def update(self, property_name, model, data=None):
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
            self.view.update_output(data)
        if property_name == ObserverMessages.OUTPUT_CLEAR:
            self.view.clear_output()

    def update_text(self, text, *_):
        '''
        Updates the main text box with output. When text is None, outputs the model and other
        debugging information
        '''
        # pp = pprint.PrettyPrinter()
        # p_model = pp.pformat(self.model)

        # self.view.clear_output()

        for line in text.output:
            self.view.append_output(line)

    def update_name(self, *_):
        ''' Updates the player name and triggers stat recalculations '''
        self.model.player.name = self.view.name_text.get()
        self.model.player.level_up()
        self.update_player_info()

    def update_player_info(self, *_):
        '''Tells the view to update the player label'''
        self.view.update_player_info(self.model.player)

    def update_level(self, *_):
        """Updates stats when level spinbox changes"""
        if self.view.level_change.get() == "":
            pass
        else:
            self.model.player.level = int(self.view.level_change.get())
            self.model.player.level_up()
            self.update_player_info()


    def buy_herb(self, *_):
        if self.model.buy_herb():
            self.view.update_player_info(self.model.player)
        # else:
        # self.view.show_message("Maximum herb count reached.")

    @property
    def name_text(self):
        return self.view.name_text

    @property
    def level_change(self):
        return self.view.level_change

    @property
    def chosen_weapon(self):
        return self.view.chosen_weapon

    @property
    def chosen_armor(self):
        return self.view.chosen_armor

    @property
    def chosen_shield(self):
        return self.view.chosen_shield

    @property
    def chosen_enemy(self):
        return self.view.chosen_enemy
