"""DQ1 Battle Simulator entry point."""

import logging
import logging.config
import sys
from pathlib import Path
from random import Random

from fightsim.common.eventmanager import EventManager
from fightsim.controllers.controller import Controller
from fightsim.models.enemy import enemy_dummy_factory
from fightsim.models.model import Model
from fightsim.models.player import player_factory
from fightsim.views.view import View

LOGGING_CONFIG = Path(__file__).parent / "logging.ini"

logger = logging.getLogger("fightsim.main")

def build_app() -> Controller:
    event_manager = EventManager("DQ1 Model Observer")
    model = Model(
        player=player_factory(),
        enemy=enemy_dummy_factory(),
        observer=event_manager,
    )
    view = View()
    rng = Random()
    controller = Controller(model, view, event_manager, rng)
    view.set_controller(controller)
    controller.initial_update()
    return controller


def main() -> int:
    logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)
    try:
        controller = build_app()
    except Exception:
        logger.exception("Failed to start the application")
        return 1

    logger.info("Starting the application GUI")
    controller.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
