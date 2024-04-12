# view.py - Holds the view for the MVC program


import tkinter as tk
from fightsim.views.setup_frame import SetupFrame
from fightsim.views.battle_frame import BattleFrame
from fightsim.views.main_frame import MainFrame


class View(tk.Tk):
    """
    View class for the application
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Using super() for a cleaner call to the parent class constructor

        # Initialize View Variables
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

        # Configure main window
        self.configure_window()

    def set_controller(self, controller):
        self.controller = controller
        self.main_frame.set_controller(controller)
        self.battle_frame.set_controller(controller)
        self.setup_frame.set_controller(controller)
        # Initialize and display frames
        self.show_frame(SetupFrame)

    def configure_window(self):
        """ Configure main window properties """
        self.title("DQ1 Battle Simulator")
        self.geometry("820x620+50+50")
        self.resizable(width=False, height=False)
        self.main_frame.pack(fill='x', expand=True)

    def show_frame(self, cont):
        """
        Switches one frame for another. Assumes frames are overlapping.
        """
        frame = self.frames[cont]
        if self.curr_frame is not None:
            self.curr_frame.pack_forget()
        self.curr_frame = frame
        frame.pack(fill='x', expand=True)

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

    def update_enemy_info(self, enemy_info):
        self.main_frame.update_enemy_label(enemy_info)

    def update_output(self, message):
        self.main_frame.update_output(message)

    def clear_output(self):
        self.main_frame.clear_output()

