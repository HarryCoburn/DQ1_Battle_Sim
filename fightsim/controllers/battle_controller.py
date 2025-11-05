""" Controller for the battle system """
from .battle import BattleEngine
from fightsim.presenters.battle_presenter import BattlePresenter


class BattleController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.player = self.model.player
        self.enemy = self.model.enemy
        self.battle = BattleEngine(self)
        self.battle_presenter = BattlePresenter(view)

    def start_battle(self, *_):
        print(f"Entering start_battle, enemy is {self.model.enemy}")        
        if self.model.enemy is None:
            pass
        else:
            self.setup_battle()

    def setup_battle(self):
        self.view.update_player_info(self.model.player)
        self.view.show_frame(self.view.battle_frame)
        # self.observer.notify(ObserverMessages.OUTPUT_CLEAR)
        self.player = self.model.player
        self.enemy = self.model.enemy
        self.battle_presenter.start_fight_msg(None, self.model.enemy.name)
        self.battle.start_fight()
        
    def on_attack_button(self):
        result = self.battle.player_attack()

        if result.hit:
            self.battle.enemy.take_damage(result.damage)
            message = self.battle_presenter.attack_result(result, self.battle.enemy.name)
            self.view.update_output(None, message)
            self.view.update_enemy_info(self.battle.enemy)
