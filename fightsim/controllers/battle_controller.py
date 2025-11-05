""" Controller for the battle system """
from .battle import BattleEngine
from fightsim.presenters.battle_presenter import BattlePresenter


class BattleController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.battle = BattleEngine(self)
        self.battle_presenter = BattlePresenter()
        
    def on_attack_button(self):
        result = self.battle.player_attack()

        if result.hit:
            self.battle.enemy.take_damage(result.damage)
            message = self.battle_presenter.attack_result(result, self.battle.enemy.name)
            self.view.update_output(message)
            self.view.update_enemy_info(self.battle.enemy)
