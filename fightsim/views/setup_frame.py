import tkinter as tk
from fightsim.models.items import weapon_names, armor_names, shield_names
from fightsim.models.enemy import enemy_names


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
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.weapon_var = tk.StringVar(value="Unarmed")
        self.armor_var = tk.StringVar(value="Naked")
        self.shield_var = tk.StringVar(value="No Shield")
        self.level_var = tk.IntVar(value=1)
        self.name_var = tk.StringVar(value="Rollo")
        self.enemy_var = tk.StringVar(value="Select Enemy")
        self.weapon_menu = None
        self.armor_menu = None
        self.shield_menu = None
        self.enemy_menu = None

    def set_controller(self, controller):
        self.controller = controller
        self.create_widgets()
        self.set_traces()

    def create_widgets(self):
        """Create and layout widgets for setup"""

        # Simplified layout using grid
        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="e", padx=5)
        tk.Entry(self, textvariable=self.name_var, width=20).grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(self, text="Level:").grid(row=1, column=0, sticky="e", padx=5)
        self.level_spinbox = tk.Spinbox(self, from_=1, to=30, increment=1, width=5,
                                        textvariable=self.level_var,
                                        wrap=True,
                                        validate='key',
                                        validatecommand=(self.register(self.level_validate), '%P'))
        self.level_spinbox.grid(row=1, column=1, sticky="w", pady=5)

        self.weapon_menu = tk.OptionMenu(self, self.weapon_var, *weapon_names,
                                         command=lambda value: self.controller.update_player_attribute("weapon", value))
        self.weapon_menu.grid(row=2,
                              column=0,
                              columnspan=2,
                              sticky="ew",
                              padx=5,
                              pady=5)

        self.armor_menu = tk.OptionMenu(self, self.armor_var, *armor_names,
                                        command=lambda value: self.controller.update_player_attribute("armor", value))
        self.armor_menu.grid(row=3,
                             column=0,
                             columnspan=2,
                             sticky="ew",
                             padx=5,
                             pady=5)
        self.shield_menu = tk.OptionMenu(self, self.shield_var, *shield_names,
                                         command=lambda value: self.controller.update_player_attribute("shield", value))
        self.shield_menu.grid(row=4,
                              column=0,
                              columnspan=2,
                              sticky="ew",
                              padx=5,
                              pady=5)
        self.enemy_menu = tk.OptionMenu(self, self.enemy_var, "Select Enemy", *enemy_names,
                                        command=lambda value: self.controller.update_enemy(value))
        self.enemy_menu.grid(row=5, column=0,
                             columnspan=2, sticky="ew",
                             padx=5, pady=5)

        self.buy_herb_button = tk.Button(self, text="Buy Herb",
                                         command=lambda: self.controller.update_player_attribute("herb"))
        self.buy_herb_button.grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.start_fight_button = tk.Button(self, text="FIGHT!", command=self.controller.start_battle)
        self.start_fight_button.grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

    def set_traces(self):
        self.level_var.trace("w",
                             lambda name, index, mode,
                                    value=self.level_var: self.controller.update_player_attribute("level", value.get()))
        self.name_var.trace("w", lambda name, index, mode, value=self.name_var: self.controller.update_player_attribute(
            "name", value.get()))

    @staticmethod
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
