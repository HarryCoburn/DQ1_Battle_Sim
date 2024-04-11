'''
    view.py - Holds the view for the MVC program
'''

import tkinter as tk
import inspect
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
        self.main_container = tk.Frame(self, height=768, width=768, bg="red")
        self.main_frame = MainFrame(self.main_container)
        self.setup_frame = SetupFrame(self.ctrl_container)
        self.battle_frame = BattleFrame(self.ctrl_container)

        self.frames = {
            SetupFrame: self.setup_frame,
            BattleFrame: self.battle_frame
        }

        # Configure main window
        self.configure_window()

        # Create and lay out containers
        self.setup_containers()

    def set_controller(self, controller):
        self.controller = controller
        self.main_frame.set_controller(controller)
        self.battle_frame.set_controller(controller)
        self.setup_frame.set_controller(controller)
        # Initialize and display frames
        self.init_frames()

    def configure_window(self):
        """ Configure main window properties """
        self.title("DQ1 Battle Simulator")
        self.geometry("1224x620+50+50")

    def setup_containers(self):
        """ Set up the main containers for control and main area"""

        # Pack it
        self.ctrl_container.pack(side="left", fill="both", expand=True)
        self.main_container.pack(side="right", fill="both", expand=True)

        # Grid it
        self.ctrl_container.grid_rowconfigure(0, weight=1)
        self.ctrl_container.grid_columnconfigure(0, weight=1)
        self.ctrl_container.grid_propagate(False)

        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

    def init_frames(self):
        # Set up the main frame.

        self.main_frame.grid(row=0, column=0, sticky="nsew")

        for frame in self.frames.values():
            frame.set_controller(self.controller)

        # Display initial frame
        self.show_frame(SetupFrame)

    def show_frame(self, cont):
        """
        Switches one frame for another. Assumes frames are overlapping.
        """
        frame = self.frames[cont]
        if self.curr_frame is not None:
            self.curr_frame.grid_remove()
        self.curr_frame = frame
        frame.grid(row=0, column=0)

    def update_magic(self):
        """
        Updates the magic menu in BattleFrame
        """
        menu = self.frames[BattleFrame].magic["menu"]
        menu.delete(0, "end")
        for string in self.spell_strings:
            menu.add_command(label=string,
                             command=lambda value=string: self.chosen_magic.set(value))

    def update_player_label(self, pinfo):
        """
        Updates the player label
        """
        print("Trying to update the label.")
        self.main_frame.player_label["text"] = inspect.cleandoc(f'''\
            Name: {pinfo.name}
            Level: {pinfo.level}
            HP: {pinfo.curr_hp}/{pinfo.max_hp}
            MP: {pinfo.curr_mp}

            Weapon: {pinfo.weapon.name}
            Armor: {pinfo.armor.name}
            Shield: {pinfo.shield.name}

            Strength: {pinfo.strength}
            Agility: {pinfo.agility}

            Herbs remaining: {pinfo.herb_count}

            Asleep?: {pinfo.is_asleep}
            Spells stopped?: {pinfo.is_spellstopped}
        ''')
        self.spell_strings = pinfo.player_magic

    def update_enemy_info(self, enemy_info):
        """
        Updates enemy label
        """
        print(enemy_info)
        self.main_frame.enemy_label["text"] = inspect.cleandoc(f'''\
            Name: {enemy_info.name}
            HP: {enemy_info.current_hp}

            Strength: {enemy_info.strength}
            Agility: {enemy_info.agility}
        ''')

    def update_output(self, message):
        """Appends output to the main output window"""
        self.main_frame.txt.configure(state='normal')  # Enable text widget for editing
        self.main_frame.txt.insert(tk.END, message + "\n")  # Append new message
        self.main_frame.txt.configure(state='disabled')  # Disable text widget to prevent editing
        self.main_frame.txt.see(tk.END)  # Auto-scroll to the end        

    def clear_output(self):
        """Erases all output in the main output"""
        self.main_frame.txt["state"] = 'normal'
        self.main_frame.txt.delete(1.0, tk.END)

