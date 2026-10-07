# view.py - Holds the view for the MVC program

from __future__ import annotations
import tkinter as tk
import logging
from fightsim.views.setup_frame import SetupFrame
from fightsim.views.battle_frame import BattleFrame
from fightsim.views.main_frame import MainFrame
from fightsim.views.actions import ViewActions
from typing import Optional

logger = logging.getLogger(__name__)

class View(tk.Tk):
    """
    View class for the application
    """
    name_text: tk.StringVar
    level_change: tk.StringVar
    chosen_weapon: tk.StringVar
    chosen_armor: tk.StringVar
    chosen_shield: tk.StringVar
    chosen_enemy: tk.StringVar
    _curr_frame: Optional[tk.Frame]
    ctrl_container: Optional[tk.Frame]
    main_container: Optional[tk.Frame]
    _setup_frame: Optional[SetupFrame]
    _battle_frame: Optional[BattleFrame]
    _main_frame: Optional[MainFrame]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_frames()
        self.configure_window()

    def setup_frames(self):
        """
        Set up the frames for the application. They are:
        ctrl_container = Side container with the control buttons
        main_container = Main container with the output
        _setup_frame = Pre-battle setup frame
        _battle_frame = Battle setup frame
        _main_frame = Main output with player, enemy, and output labels
        """

        self._curr_frame = None

        self.ctrl_container = tk.Frame(self, height=768, width=256, bg="blue")
        # self.ctrl_container.pack_propagate(False)
        self.ctrl_container.pack(side="left", fill='y')

        self.main_container = tk.Frame(self, height=768, width=768, bg="red")
        self.main_container.pack_propagate(False)
        self.main_container.pack(side="right", expand=True, fill='both')

        # Fixed frame in the application
        self._main_frame = MainFrame(self.main_container)

        # Changeable frames in the application
        self._battle_frame = BattleFrame(self.ctrl_container)

        self._setup_frame = SetupFrame(self.ctrl_container, width=240, height=600, padx=20)

    def report_callback_exception(self, exc, val, tb):
        """ Logs errors raised in button and other Tk callbacks instead of printing them to stderr """
        logger.error("Unhandled exception in Tk callback", exc_info=(exc, val, tb))

    def configure_window(self):
        """ Configure main window properties """
        self.title("DQ1 Battle Simulator")
        self.geometry("820x620+50+50")
        self.resizable(width=True, height=True)
        self._main_frame.pack(fill='x', expand=True)

    def bind_actions(self, actions: ViewActions):
        """ Gives the frames the actions their controls call """
        self._battle_frame.bind_actions(actions)
        self._setup_frame.bind_actions(actions)
        self.show_setup_screen()

    def show_setup_screen(self) -> None:
        """ Shows the pre-battle setup controls """
        self._swap_controls(self._setup_frame)

    def show_battle_screen(self) -> None:
        """ Shows the battle controls """
        self._swap_controls(self._battle_frame)

    def _swap_controls(self, new_frame: tk.Frame) -> None:
        """ Hides the current control frame and packs new_frame in its place """
        if self._curr_frame is not None:
            self._curr_frame.pack_forget()
        self._curr_frame = new_frame
        new_frame.pack(fill='x', expand=True)
        logging.debug(f"Switched to frame: {new_frame}")

    def update_player_info(self, player_info):
        """ Refreshes the player label in _main_frame, the magic menu in _battle_frame and the level in _setup_frame """
        self._main_frame.update_player_label(player_info)
        self._battle_frame.update_magic_menu(player_info.player_magic)
        self._setup_frame.set_player_level(player_info.level)

    def update_enemy_info(self, enemy_info):
        """ Refreshes the enemy label in _main_frame """
        self._main_frame.update_enemy_label(enemy_info)

    def append_output(self, message):
        """ Adds message to the output widget in _main_frame """
        self._main_frame.append_output(message)

    def clear_output(self):
        """ Clears the output widget in _main_frame """
        self._main_frame.clear_output()
