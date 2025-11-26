# DQ1 Battle Simulator - App

import logging
import logging.config
from fightsim.views.view import View
from fightsim.controllers.controller import Controller
from fightsim.models.game_state import GameState
from fightsim.models.player import player_factory
from fightsim.models.enemy import enemy_dummy_factory

from fightsim.controllers.battle_controller import BattleController
from fightsim.models.combat_engine import CombatEngine
from fightsim.common.randomizer import Randomizer
from fightsim.models.game_constants import GameConstants

def create_view():
    return View()  

def create_game_state(combat_engine):
    return GameState(player=player_factory(combat_engine), enemy=enemy_dummy_factory(combat_engine))

def create_controller(game_state, view):
    return Controller(game_state, view)

def create_battle_controller(game_state, view):
    return BattleController(game_state, view)

def create_combat_engine():
    return CombatEngine(Randomizer(), GameConstants())

def main(view_factory=create_view,
        game_state_factory=create_game_state,
        controller_factory=create_controller,        
        battle_controller_factory=create_battle_controller,
        combat_engine_factory=create_combat_engine
        ):
        
    """ Entry Point for the Application """

    
    logging.config.fileConfig('./fightsim/logging.ini')
    main_logger = logging.getLogger('main')
    
    try:       
        combat_engine = combat_engine_factory()
        view = view_factory()        
        game_state = game_state_factory(combat_engine)
        controller = controller_factory(game_state, view)
        battle_controller = battle_controller_factory(game_state, view)
        view.set_controllers(controller, battle_controller)
        controller.initial_update()

        main_logger.info("Starting the application GUI")
        controller.view.mainloop()
    except Exception as e:
        main_logger.error(f"Failed to start the application: {e}", exc_info=True)


if __name__ == "__main__":
    main()
