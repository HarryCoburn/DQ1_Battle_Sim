import tkinter as tk
from functools import partial


class BattleFrame(tk.Frame):
    """Optimized frame for conducting the fight."""

    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None
        self.attack_btn = None
        self.herb_btn = None
        self.run_btn = None
        self.cast_btn = None
        self.magic_option_var = tk.StringVar(self)
        self.magic_menu = None
        self.player_magic = []

    def set_controller(self, controller):
        """ Sets controller as the controller for BattleFrame and continues setup of BattleFrame """
        self.controller = controller
        self.set_magic_menu()
        self.create_widgets()

    def set_magic_menu(self):
        """ Initializes self.player_magic and links it correctly with the controller. """
        self.player_magic = self.controller.model.player.player_magic
        if not self.player_magic:
            self.player_magic = ["No Magic Available"]
        self.magic_option_var.set(self.player_magic[0])

    def create_widgets(self):
        """Create and layout widgets for battle."""
        self.attack_btn = tk.Button(self, text="Attack", command=self.controller.on_attack_button)
        self.attack_btn.grid(row=0, column=0, padx=5, pady=5)
        self.herb_btn = tk.Button(self, text="Use Herb", command=self.controller.on_herb_button)
        self.herb_btn.grid(row=1, column=0, padx=5, pady=5)
        self.run_btn = tk.Button(self, text="Run", command=self.controller.on_flee_button)
        self.run_btn.grid(row=2, column=0, padx=5, pady=5)
        self.cast_btn = tk.Button(self, text="Cast", command=self.controller.on_cast_magic_button)
        self.cast_btn.grid(row=3, column=0, padx=5, pady=5)

        self.magic_menu = tk.OptionMenu(self, self.magic_option_var, *self.player_magic)
        self.magic_menu.grid(row=3, column=1, padx=5, pady=5)

    def update_player_magic_menu(self):
        """ Update the options available in the magic menu based on current player magic abilities. """
        menu = self.magic_menu['menu']
        menu.delete(0, 'end')

        # Ensure there's a default list of magic spells
        player_magic = self.controller.model.player.player_magic or ["No Magic Available"]
        self.magic_option_var.set(player_magic[0])

        for magic in player_magic:
            menu.add_command(label=magic.value.name, command=partial(self.set_magic_option, magic))

    def set_magic_option(self, magic):
        """ Set the current magic option in the OptionMenu. """
        self.magic_option_var.set(magic)
