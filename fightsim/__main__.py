# DQ1 Battle Simulator - App

import logging
from fightsim.views.view import View
from fightsim.controllers.controller import Controller
from fightsim.models.model import Model
from fightsim.models.player import player_factory
from fightsim.models.enemy import enemy_dummy_factory
from fightsim.common.eventmanager import EventManager


def main():
    """ Entry Point for the Application """

    # Logging Setup
    main_logger = logging.getLogger('main')
    main_logger.setLevel(logging.INFO)

    # Handler Setup
    main_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main_handler.setFormatter(formatter)
    main_logger.addHandler(main_handler)

    try:
        observer = EventManager("DQ1 Model Observer")
        view = View()
        model = Model(player=player_factory(), enemy=enemy_dummy_factory(), observer=observer)
        controller = Controller(model, view, observer)

        view.set_controller(controller)
        controller.initial_update()

        main_logger.info("Starting the application GUI")
        controller.view.mainloop()
    except Exception as e:
        main_logger.error(f"Failed to start the application: {e}", exc_info=True)


if __name__ == "__main__":
    main()
