""" Controller for the battle system """
from ..models.battle import BattleEngine
from fightsim.presenters.battle_presenter import BattlePresenter
from ..common.randomizer import Randomizer


class BattleController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.player = self.model.player
        self.enemy = self.model.enemy
        self.battle = BattleEngine(self)
        self.battle_presenter = BattlePresenter(view)

    # Battle Setup

    def start_battle(self, *_):
        """ Sanity check to ensure the player has selected an enemy """
        print(f"Entering start_battle, enemy is {self.model.enemy}")        
        if self.model.enemy is None:
            pass
        else:
            self.setup_battle()

    def setup_battle(self):
        """ All of the initial battle setup before the battle menu appears """        
        self.view.update_player_info(self.model.player)
        self.view.show_frame(self.view.battle_frame)
        # self.observer.notify(ObserverMessages.OUTPUT_CLEAR)
        self.player = self.model.player
        self.enemy = self.model.enemy
        self.battle_presenter.start_fight_msg(None, self.model.enemy.name)
        self.start_fight()

    def start_fight(self):
        # Check for surprise at the very start of battle.
        enemy_surprises = self.does_enemy_surprise()
        if enemy_surprises:
            self.battle_presenter.player_surprised(None, self.enemy.name)
            self.enemy_turn()
        else:
            self.player_turn()

    def does_enemy_surprise(self):
        """ Determine if the enemy surprises the player based on agility and randomness. """
        player_roll = Randomizer.agility_roll(self.player.agility)
        enemy_roll = Randomizer.agility_roll(self.enemy.agility, surprise_factor=0.25)
        return player_roll < enemy_roll
    
    # Player Turns and Actions

    def player_turn(self):
        """Runs at the start of player turn. Checks for sleep status and updates it, then waits for user to
        enter a command."""
        if self.player.check_sleep():  # If the player is asleep, switch to the enemy's turn.
            self.enemy_turn()

    def on_attack_button(self):
        result = self.player.attack(self.enemy)

        if result.hit:
            self.battle.enemy.take_damage(result.damage)
            self.battle_presenter.attack_result(result, self.battle.enemy.name)            
            self.view.update_enemy_info(self.enemy)
            self.is_enemy_defeated()
        else:
            self.enemy_turn()

    def on_herb_button(self):
        if self.player.has_herbs() is False:
            self.battle_presenter.no_herbs()
            return # Player does not lose turn if they try to use an herb when they have none.
        else:
            result = self.player.use_herb()
            if result == 0: # Used herb with full HP, no healing
                self.battle_presenter.eat_herb_at_full_hp()
            else:
                self.battle_presenter.eat_herb(None, result)
        self.is_enemy_defeated()

    def on_flee_button(self):
        result = self.player.is_flee_successful(self.enemy.agility, self.enemy.run)
        self.battle_presenter.fleeing(result, self.enemy.name)
        if result is True:            
            self.end_fight()
        else:
            self.enemy_turn()

    def on_cast_magic_button(self):
        spell = self.view.battle_frame.magic_option_var.get()    

        # First make sure a spell is selected
        if spell in ["Select Spell", "No Magic Available"]:
            self.battle_presenter.no_spell_selected(spell)
            return
        
        result = self.player.cast_magic(spell, self.enemy)
        if result == "not_enough_mp":
            self.battle_presenter.not_enough_mp(spell)
        
        if result == "player_spellstopped":
            self.battle_presenter.player_spellstopped(spell)
        
        if result == "heal_when_at_max_hp":
            self.battle_presenter.player_casts_heal_when_full(spell)
        
        if result == "resist_hurt":
            self.battle_presenter.enemy_resists_hurt(spell)
        
        if result == "enemy_already_asleep":
            self.battle_presenter.enemy_already_asleep(self.enemy.name)
        
        if result == "enemy_resists_sleep":
            self.battle_presenter.enemy_resists_sleep(self.enemy.name)
        
        if result == "enemy_already_spellstopped":
            self.battle_presenter.enemy_already_stopped(self.enemy.name)
        
        if result == "enemy_resists_spellstop":
            self.battle_presenter.enemy_resists_stopped(self.enemy.name)
        
        # From here, spells are successful
        if spell in ["Heal", "Healmore"]:
            self.battle_presenter.player_casts_heal(spell, result)
        
        if spell in ["Hurt", "Hurtmore"]:
            self.battle_presenter.player_casts_hurt(spell, self.enemy.name, result)
            
        if spell == "Sleep":
            self.battle_presenter.enemy_now_asleep(self.enemy.name)
            
        if spell == "Stopspell":
            self.battle_presenter.enemy_now_spell_stopped(self.enemy.name)
        
        self.is_enemy_defeated()


        
        


    

    # Battle Ending and Turn Switching

    def is_enemy_defeated(self):
        """ Checks if the enemy is defeated. Ends fight if true. Starts enemy turn if false. """
        if self.enemy.is_defeated():
            self.battle_presenter.player_wins(None, self.enemy.name)
            self.end_fight()
        else:
            self.enemy_turn()
