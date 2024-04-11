import tkinter as tk
from fightsim.models.items import weapon_names, armor_names, shield_names
from fightsim.models.enemy import enemy_names


class SetupFrame(tk.Frame):
    """
    Frame for fight setup buttons
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._level_value = tk.StringVar(value="1")


    def set_controller(self, controller):
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """Create and layout widgets for setup"""

        # Simplified layout using grid
        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="e", padx=5)
        tk.Entry(self, textvariable=self.controller.name_text, width=20).grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(self, text="Level:").grid(row=1, column=0, sticky="e", padx=5)
        tk.Spinbox(self, from_=1, to=30, width=5, textvariable=self.controller.level_change, validate='all',
                   validatecommand=(self.register(self.level_validate), '%P')).grid(row=1, column=1, sticky="w", pady=5)

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
        # self.start_fight_button = tk.Button(self, text="FIGHT!", command=self.controller.start_fight)
        self.buy_herb_button.grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        # self.start_fight_button.grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

    def on_validate(self, P):
        if P.isdigit() and 1 <= int(P) <= 30:
            return True
        return False

    def level_validate(self, new_value):
        if self.on_validate(new_value):
            self._level_value.set(new_value)
            self.controller.level_change.set(new_value)
        else:
            self.level_spinbox.delete(0, tk.END)
            self.level_spinbox.insert(0, 1)
