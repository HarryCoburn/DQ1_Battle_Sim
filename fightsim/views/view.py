# view.py - Holds the view for the MVC program


import tkinter as tk
import logging
from fightsim.views.setup_frame import SetupFrame
from fightsim.views.battle_frame import BattleFrame
from fightsim.views.main_frame import MainFrame
from typing import List, Optional, Dict, Union, Type


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
    chosen_magic: tk.StringVar
    spell_strings: List[str]
    curr_frame: Optional[tk.Frame]
    ctrl_container: Optional[tk.Frame]
    main_container: Optional[tk.Frame]
    setup_frame: Optional[tk.Frame]
    battle_frame: Optional[tk.Frame]
    main_frame: Optional[tk.Frame]
    controller: Optional['Controller']
    frames: Dict[Type[Union[SetupFrame, BattleFrame]], Optional[tk.Frame]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_vars()
        self.setup_frames()
        self.configure_window()

    def init_vars(self):
        self.name_text = tk.StringVar(value="Rollo")
        self.level_change = tk.StringVar(value="1")
        self.chosen_weapon = tk.StringVar(value="Unarmed")
        self.chosen_armor = tk.StringVar(value="Naked")
        self.chosen_shield = tk.StringVar(value="No Shield")
        self.chosen_enemy = tk.StringVar(value="Select Enemy")
        self.chosen_magic = tk.StringVar(value="No spells available.")
        self.spell_strings = []  # To be dynamically updated
        self.curr_frame = None
        self.controller = None

    def setup_frames(self):
        """
        Set up the frames for the application. They are:
        ctrl_container = Side container with the control buttons
        main_container = Main container with the output
        setup_frame = Pre-battle setup frame
        battle_frame = Battle setup frame
        main_frame = Main output with player, enemy, and output labels
        """
        try:
            self.ctrl_container = tk.Frame(self, height=768, width=256, bg="blue")
            self.ctrl_container.pack_propagate(False)
            self.ctrl_container.pack(side="left", fill='y')

            self.main_container = tk.Frame(self, height=768, width=768, bg="red")
            self.main_container.pack_propagate(False)
            self.main_container.pack(side="right", expand=True, fill='both')

            self.setup_frame = SetupFrame(self.ctrl_container, width=256, height=600, padx=20)
            self.setup_frame.pack(expand=True)

            self.main_frame = MainFrame(self.main_container)

            self.battle_frame = BattleFrame(self.ctrl_container)

            self.frames = {
                SetupFrame: self.setup_frame,
                BattleFrame: self.battle_frame
            }
        except Exception as e:
            logging.error(f"Error setting up frames: {e}")

    def configure_window(self):
        """ Configure main window properties """
        self.title("DQ1 Battle Simulator")
        self.geometry("820x620+50+50")
        self.resizable(width=True, height=True) # TODO See if this messes up the frames.
        self.main_frame.pack(fill='x', expand=True)

    def set_controller(self, controller):
        """ Attaches the controller to the frames """
        self.controller = controller
        self.main_frame.set_controller(controller)
        self.battle_frame.set_controller(controller)
        self.setup_frame.set_controller(controller)
        # Initialize and display frames
        self.show_frame(self.setup_frame)

    def show_frame(self, cont: Type[tk.Frame]) -> None:
        """
        Displays the given frame, hiding the current one.

        Parameters:
        cont (tk.Frame): The Tkinter frame to be displayed.

        Does not return a value but changes the visible frame in the application window.
        """
        if cont not in self.frames.values():
            logging.error(f"Attempted to show an unmanaged frame: {cont}")
            return
        if self.curr_frame is not None:
            self.curr_frame.pack_forget()
        self.curr_frame = cont
        cont.pack(fill='x', expand=True)
        logging.debug(f"Switched to frame: {cont}")

        # frame = self.frames[cont]
        # if self.curr_frame is not None:
        #     self.curr_frame.pack_forget()
        # self.curr_frame = cont
        # cont.pack(fill='x', expand=True)

    def update_magic(self):
        """
        Updates the magic menu in BattleFrame
        """
        menu = self.frames[BattleFrame].magic["menu"]
        menu.delete(0, "end")
        for string in self.spell_strings:
            menu.add_command(label=string,
                             command=lambda value=string: self.chosen_magic.set(value))

    def update_player_info(self, player_info):
        self.main_frame.update_player_label(player_info)
        self.battle_frame.update_player_magic_menu(player_info.player_magic)

    def update_enemy_info(self, enemy_info):
        self.main_frame.update_enemy_label(enemy_info)

    def update_output(self, message):
        self.main_frame.update_output(message)

    def clear_output(self):
        self.main_frame.clear_output()

