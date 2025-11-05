# DQ1 Battle Simulator - App

import logging
import logging.config
from fightsim.views.view import View
from fightsim.controllers.controller import Controller
from fightsim.models.model import Model
from fightsim.models.player import player_factory
from fightsim.models.enemy import enemy_dummy_factory
from fightsim.common.eventmanager import EventManager
from fightsim.controllers.battle_controller import BattleController
from fightsim.presenters.battle_presenter import BattlePresenter

def create_event_manager():
    return EventManager("DQ1 Model Observer")

def create_view():
    return View()  

def create_model(event_manager):
    return Model(player=player_factory(), enemy=enemy_dummy_factory(), observer=event_manager)

def create_controller(model, view, event_manager):
    return Controller(model, view, event_manager)

def create_battle_controller(model, view):
    return BattleController(model, view)

# def create_battle_presenter():
#     return BattlePresenter()

def main(event_manager_factory=create_event_manager,
         view_factory=create_view,
         model_factory=create_model,
         controller_factory=create_controller,
        #  battle_presenter_factory=create_battle_presenter,
         battle_controller_factory=create_battle_controller):
    """ Entry Point for the Application """

    
    logging.config.fileConfig('./fightsim/logging.ini')
    main_logger = logging.getLogger('main')
    
    try:
        event_manager = event_manager_factory()
        view = view_factory()
        model = model_factory(event_manager)
        controller = controller_factory(model, view, event_manager)
        battle_controller = battle_controller_factory(model, view)
        # battle_presenter = battle_presenter_factory(view)
        
        view.set_controllers(controller, battle_controller)
        controller.initial_update()

        main_logger.info("Starting the application GUI")
        controller.view.mainloop()
    except Exception as e:
        main_logger.error(f"Failed to start the application: {e}", exc_info=True)


if __name__ == "__main__":
    main()
