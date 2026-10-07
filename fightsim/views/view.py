# view.py - Holds the view for the MVC program

from __future__ import annotations
import tkinter as tk
import logging
from fightsim.views.setup_frame import SetupFrame
from fightsim.views.battle_frame import BattleFrame
from fightsim.views.main_frame import MainFrame
from typing import Optional, Dict, Union, Type, TYPE_CHECKING


if TYPE_CHECKING:
    from fightsim.controllers.controller import Controller

class View(tk.Tk):
    """
    View class for the application
    """
    controller: Controller | None = None
    name_text: tk.StringVar
    level_change: tk.StringVar
    chosen_weapon: tk.StringVar
    chosen_armor: tk.StringVar
    chosen_shield: tk.StringVar
    chosen_enemy: tk.StringVar
    curr_frame: Optional[tk.Frame]
    ctrl_container: Optional[tk.Frame]
    main_container: Optional[tk.Frame]
    _setup_frame: Optional[SetupFrame]
    _battle_frame: Optional[BattleFrame]
    _main_frame: Optional[MainFrame]
    changeable_frames: Dict[Type[Union[SetupFrame, BattleFrame]], Optional[tk.Frame]]

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

        self.curr_frame = None

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
        self._setup_frame.pack(expand=True)

        self.changeable_frames = {
            SetupFrame: self._setup_frame,
            BattleFrame: self._battle_frame
        }

    def configure_window(self):
        """ Configure main window properties """
        self.title("DQ1 Battle Simulator")
        self.geometry("820x620+50+50")
        self.resizable(width=True, height=True)
        self._main_frame.pack(fill='x', expand=True)

    def set_controller(self, controller):
        """ Attaches the controller to the frames """
        self.controller = controller
        self._main_frame.set_controller(controller)
        self._battle_frame.set_controller(controller)
        self._setup_frame.set_controller(controller)
        # Initialize and display frames
        self.show_frame(self._setup_frame)

    def show_frame(self, new_frame: Union[tk.Frame, None]) -> None:
        """
        Displays the given frame, hiding the current one.

        Parameters:
        cont (tk.Frame): The Tkinter frame to be displayed.

        Does not return a value but changes the visible frame in the application window.
        """
        if new_frame not in self.changeable_frames.values():
            logging.error(f"Attempted to show an unmanaged frame: {new_frame}")
            return
        if self.curr_frame is not None:
            self.curr_frame.pack_forget()
        self.curr_frame = new_frame
        new_frame.pack(fill='x', expand=True)
        logging.debug(f"Switched to frame: {new_frame}")

    def update_player_info(self, player_info):
        """ Refreshes the player label in _main_frame and the magic menu in _battle_frame """
        self._main_frame.update_player_label(player_info)
        self._battle_frame.update_player_magic_menu()

    def update_enemy_info(self, enemy_info):
        """ Refreshes the enemy label in _main_frame """
        self._main_frame.update_enemy_label(enemy_info)

    def update_output(self, event_type, message):
        """ Adds message to the output widget in _main_frame """
        self._main_frame.update_output(event_type, message)

    def clear_output(self):
        """ Clears the output widget in _main_frame """
        self._main_frame.clear_output()

    def update_magic_menu(self):
        self._battle_frame.update_player_magic_menu()

    def get_chosen_magic_from_menu(self):
        return self._battle_frame.magic_option_var.get()

    def show_battle_screen(self) -> None:
        self._main_frame.txt["state"] = "normal"
        self.show_frame(self._battle_frame)

    def show_setup_screen(self) -> None:
        self._main_frame.txt["state"] = "disabled"
        self.show_frame(self._setup_frame)
