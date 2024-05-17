# DQ1 Battle Simulator - App

import logging
import logging.config
from fightsim.views.view import View
from fightsim.controllers.controller import Controller
from fightsim.models.model import Model
from fightsim.models.player import player_factory
from fightsim.models.enemy import enemy_dummy_factory
from fightsim.common.eventmanager import EventManager

def create_event_manager():
    return EventManager("DQ1 Model Observer")

def create_view():
    return View()

def create_model(event_manager):
    return Model(player=player_factory(), enemy=enemy_dummy_factory(), observer=event_manager)

def create_controller(model, view, event_manager):
    return Controller(model, view, event_manager)

def main(event_manager_factory=create_event_manager,
         view_factory=create_view,
         model_factory=create_model,
         controller_factory=create_controller):
    """ Entry Point for the Application """

    
    logging.config.fileConfig('./fightsim/logging.ini')
    main_logger = logging.getLogger('main')
    
    try:
        event_manager = event_manager_factory()
        view = view_factory()
        model = model_factory(event_manager)
        controller = controller_factory(model, view, event_manager)
        
        view.set_controller(controller)
        controller.initial_update()

        main_logger.info("Starting the application GUI")
        controller.view.mainloop()
    except Exception as e:
        main_logger.error(f"Failed to start the application: {e}", exc_info=True)


if __name__ == "__main__":
    main()
