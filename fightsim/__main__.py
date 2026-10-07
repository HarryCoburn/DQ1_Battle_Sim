"""DQ1 Battle Simulator entry point."""

import logging
import logging.config
import sys
from pathlib import Path
from random import Random

from fightsim.controllers.controller import Controller
from fightsim.models.enemy import Enemy
from fightsim.models.model import Model
from fightsim.models.player import Player
from fightsim.views.view import View

LOGGING_CONFIG = Path(__file__).parent / "logging.ini"

logger = logging.getLogger("fightsim.main")

def build_app() -> Controller:
    model = Model(
        player=Player(),
        enemy=Enemy.create_dummy(),
    )
    view = View()
    rng = Random()
    controller = Controller(model, view, rng)
    view.bind_actions(controller)
    view.show_setup_screen()
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
