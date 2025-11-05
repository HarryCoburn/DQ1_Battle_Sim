# view.py - Holds the view for the MVC program

from __future__ import annotations
import tkinter as tk
import logging
from fightsim.views.setup_frame import SetupFrame
from fightsim.views.battle_frame import BattleFrame
from fightsim.views.main_frame import MainFrame
from fightsim.controllers.controller import Controller
from fightsim.controllers.battle_controller import BattleController
from typing import Optional, Dict, Union, Type


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
    curr_frame: Optional[tk.Frame]
    ctrl_container: Optional[tk.Frame]
    main_container: Optional[tk.Frame]
    setup_frame: Optional[SetupFrame]
    battle_frame: Optional[BattleFrame]
    main_frame: Optional[MainFrame]
    controller: Optional['Controller'] = None
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
        setup_frame = Pre-battle setup frame
        battle_frame = Battle setup frame
        main_frame = Main output with player, enemy, and output labels
        """

        self.curr_frame = None

        self.ctrl_container = tk.Frame(self, height=768, width=256, bg="blue")
        # self.ctrl_container.pack_propagate(False)
        self.ctrl_container.pack(side="left", fill='y')

        self.main_container = tk.Frame(self, height=768, width=768, bg="red")
        self.main_container.pack_propagate(False)
        self.main_container.pack(side="right", expand=True, fill='both')

        # Fixed frame in the application
        self.main_frame = MainFrame(self.main_container)

        # Changeable frames in the application
        self.battle_frame = BattleFrame(self.ctrl_container)

        self.setup_frame = SetupFrame(self.ctrl_container, width=240, height=600, padx=20)
        self.setup_frame.pack(expand=True)

        self.changeable_frames = {
            SetupFrame: self.setup_frame,
            BattleFrame: self.battle_frame
        }

    def configure_window(self):
        """ Configure main window properties """
        self.title("DQ1 Battle Simulator")
        self.geometry("820x620+50+50")
        self.resizable(width=True, height=True)
        self.main_frame.pack(fill='x', expand=True)

    def set_controllers(self, controller, battle_controller):
        """ Attaches the controller to the frames """
        self.controller = controller
        self.main_frame.set_controller(controller)
        self.battle_frame.set_controller(battle_controller)
        self.setup_frame.set_controllers(controller, battle_controller)
        # Initialize and display frames
        self.show_frame(self.setup_frame)

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
        """ Refreshes the player label in main_frame and the magic menu in battle_frame """
        self.main_frame.update_player_label(player_info)
        self.battle_frame.update_player_magic_menu()

    def update_enemy_info(self, enemy_info):
        """ Refreshes the enemy label in main_frame """
        self.main_frame.update_enemy_label(enemy_info)

    def update_output(self, event_type, message):
        """ Adds message to the output widget in main_frame """
        self.main_frame.update_output(event_type, message)

    def clear_output(self):
        """ Clears the output widget in main_frame """
        self.main_frame.clear_output()
