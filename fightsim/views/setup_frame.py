import tkinter as tk
from fightsim.models.items import weapon_names, armor_names, shield_names
from fightsim.models.enemy import enemy_names


def level_validate(p):
    """ Validate the input to the level spinbox to see if it's within range """
    if p == "":
        return True
    try:
        val = int(p)
        if 1 <= val <= 30:
            return True
        else:
            return False
    except ValueError:
        # non-numeric input
        return False


class SetupFrame(tk.Frame):
    """
    Frame for fight setup buttons
    """

    def __init__(self, parent, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.start_fight_button = None
        self.buy_herb_button = None
        self.controller = None
        self.level_spinbox = None
        self._level_value = tk.StringVar(value="1")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def set_controller(self, controller):
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """Create and layout widgets for setup"""

        # Simplified layout using grid
        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="e", padx=5)
        tk.Entry(self, textvariable=self.controller.name_text, width=20).grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(self, text="Level:").grid(row=1, column=0, sticky="e", padx=5)
        self.level_spinbox = tk.Spinbox(self, from_=1, to=30, increment=1, width=5,
                                        textvariable=self.controller.level_change,
                                        validate='key',
                                        validatecommand=(self.register(level_validate), '%P'))
        self.level_spinbox.grid(row=1, column=1, sticky="w", pady=5)

        tk.OptionMenu(self, self.controller.chosen_weapon, *weapon_names).grid(row=2, column=0, columnspan=2,
                                                                               sticky="ew", padx=5, pady=5)
        tk.OptionMenu(self, self.controller.chosen_armor, *armor_names).grid(row=3, column=0, columnspan=2, sticky="ew",
                                                                             padx=5, pady=5)
        tk.OptionMenu(self, self.controller.chosen_shield, *shield_names).grid(row=4, column=0, columnspan=2,
                                                                               sticky="ew", padx=5, pady=5)
        tk.OptionMenu(self, self.controller.chosen_enemy, "Select Enemy", *enemy_names).grid(row=5, column=0,
                                                                                             columnspan=2, sticky="ew",
                                                                                             padx=5, pady=5)

        self.buy_herb_button = tk.Button(self, text="Buy Herb", command=self.controller.buy_herb)
        self.buy_herb_button.grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.start_fight_button = tk.Button(self, text="FIGHT!", command=self.controller.start_battle)
        self.start_fight_button.grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=10)
