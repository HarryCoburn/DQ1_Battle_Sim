""" Controller for the battle system """

from fightsim.presenters.battle_presenter import BattlePresenter
from ..common.randomizer import Randomizer
from ..common.messages import EnemyActions
from ..models.spells import SpellResult, SpellType

class BattleController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.player = self.model.player
        self.enemy = self.model.enemy
        
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
        self.battle_presenter.start_fight_msg(None, self.enemy.name) #test name here
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
        sleep_check = self.player.handle_sleep()  # TODO: expand on this. If the player is asleep, switch to the enemy's turn.
        if sleep_check is True:
            self.battle_presenter.player_is_sleeping()            
            self.enemy_turn()
        if sleep_check == "awake":
            self.battle_presenter.player_woke_up()
        # Stopspell does not lift once the player is under that status.

    def on_attack_button(self):
        result = self.player.attack(self.enemy)

        if result.hit:
            self.enemy.take_damage(result.damage)
            self.battle_presenter.attack_result(result, self.enemy.name)            
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
            if result.success is False and result.reason == "max_hp": # Used herb with full HP, no healing
                self.battle_presenter.eat_herb_at_full_hp()
            else:
                self.player.raise_hp(result.healing)
                self.battle_presenter.eat_herb(None, result.healing)
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
        if result.success is False:
            self.battle_presenter.player_spell_failed(result, self.enemy.name)
        
        # From here, spells are successful
        if spell in [SpellType.HEAL, SpellType.HEALMORE]:
            self.battle_presenter.player_casts_heal(spell, result.amount)
            self.player.raise_hp(result.amount)
        
        if spell in ["Hurt", "Hurtmore"]:
            self.battle_presenter.player_casts_hurt(spell, self.enemy.name, result)
            
        if spell == "Sleep":
            self.battle_presenter.enemy_now_asleep(self.enemy.name)
            
        if spell == "Stopspell":
            self.battle_presenter.enemy_now_spell_stopped(self.enemy.name)
        
        self.is_enemy_defeated()

    # Enemy Turn and Actions

    def enemy_turn(self):
        # First, handle if the enemy's sleep status
        if self.enemy.enemy_sleep_count > 0:
            sleep_status = self.enemy.is_asleep()
            if sleep_status is True:
                if self.enemy.enemy_sleep_count == 2:
                    self.battle_presenter.enemy_is_sleeping(self.enemy.name)
                else:
                    self.battle_presenter.enemy_is_still_sleeping(self.enemy.name)
                self.player_turn()
            elif sleep_status == "enemy_woke_up":
                self.battle_presenter.enemy_woke_up(self.enemy.name)
        # Now see if the enemy flees
        if self.enemy.does_flee(self.player.strength):
            self.battle_presenter.enemy_flees(self.enemy.name)
            self.end_fight() #    self.fight_over.set(True)
        
        # Perform an action and get its result
        result = self.enemy.perform_enemy_action(self.player)
        
        if result[0] == EnemyActions.ATTACK:
            self.battle_presenter.enemy_attacks(self.enemy.name, str(result[1]))            
        
        if result[0] in [EnemyActions.HURT, EnemyActions.HURTMORE]:
            if self.enemy.enemy_spell_stopped:
                self.battle_presenter.enemy_casts_while_spellstopped(self.enemy.name, result[0])
            else:
                self.battle_presenter.enemy_casts_hurt(self.enemy.name, result, self.player.name)
        
        if result[0] in [EnemyActions.FIRE, EnemyActions.STRONGFIRE]:
            self.battle_presenter.enemy_breathes_fire(self.enemy.name, result, self.player.name)

        if result[0] in [EnemyActions.HEAL, EnemyActions.HEALMORE]:
            if self.enemy.enemy_spell_stopped:
                self.battle_presenter.enemy_casts_while_spellstopped(self.enemy.name, result[0])
            else:
                self.battle_presenter.enemy_casts_heal(self.enemy.name, result)

        if result[0] == EnemyActions.SLEEP:
            if self.enemy.enemy_spell_stopped:
                self.battle_presenter.enemy_casts_while_spellstopped(self.enemy.name, result[0])
            else:
                self.battle_presenter.enemy_casts_sleep(self.enemy.name)

        if result[0] == EnemyActions.STOPSPELL:
            if self.enemy.enemy_spell_stopped:
                self.battle_presenter.enemy_casts_while_spellstopped(self.enemy.name, result[0])
            else:
                self.battle_presenter.enemy_casts_stopspell(self.enemy.name, result[1])


        self.is_player_defeated()    


    # Battle Ending and Turn Switching

    def is_enemy_defeated(self):
        """ Checks if the enemy is defeated. Ends fight if true. Starts enemy turn if false. """
        self.view.update_enemy_info(self.enemy)
        if self.enemy.is_defeated():
            self.battle_presenter.player_wins(None, self.enemy.name)
            self.end_fight()
        else:
            self.enemy_turn()

    def is_player_defeated(self):
        self.view.update_player_info(self.player)
        if self.player.is_defeated():
            self.battle_presenter.enemy_wins(self.enemy.name)
            self.end_fight()
        else:
            self.player_turn()
        

    def end_fight(self):
        self.enemy.current_hp = self.enemy.max_hp
        self.player.current_hp = self.player.max_hp
        self.player.current_mp = self.player.max_mp
        self.player.herb_count = 0
        self.view.main_frame.txt["state"] = "disabled"
        self.view.update_player_info(self.player)
        self.view.update_enemy_info(self.enemy)
        self.view.show_frame(self.view.setup_frame)
