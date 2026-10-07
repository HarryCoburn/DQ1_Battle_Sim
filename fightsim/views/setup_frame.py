import tkinter as tk
from fightsim.models.items import weapon_names, armor_names, shield_names
from fightsim.models.enemy import enemy_names
from fightsim.views.actions import ViewActions
from typing import Optional

class SetupFrame(tk.Frame):
    """
    Frame for fight setup buttons
    """

    def __init__(self, parent, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.actions: Optional[ViewActions] = None
        self.player_level = 1
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.weapon_var = tk.StringVar(value="Unarmed")
        self.armor_var = tk.StringVar(value="Naked")
        self.shield_var = tk.StringVar(value="No Shield")
        self.level_var = tk.IntVar(value=1)
        self.name_var = tk.StringVar(value="Rollo")
        self.enemy_var = tk.StringVar(value="Select Enemy")
        self.create_widgets()
        self.set_traces()

    def bind_actions(self, actions: ViewActions):
        """ Sets the actions the setup controls call """
        self.actions = actions

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
        self.level_spinbox.bind("<FocusOut>", lambda event: self.refill_level())

        self.weapon_menu = tk.OptionMenu(self, self.weapon_var, *weapon_names,
                                         command=lambda value: self.actions.equip_weapon(value))
        self.weapon_menu.grid(row=2,
                              column=0,
                              columnspan=2,
                              sticky="ew",
                              padx=5,
                              pady=5)

        self.armor_menu = tk.OptionMenu(self, self.armor_var, *armor_names,
                                        command=lambda value: self.actions.equip_armor(value))
        self.armor_menu.grid(row=3,
                             column=0,
                             columnspan=2,
                             sticky="ew",
                             padx=5,
                             pady=5)
        self.shield_menu = tk.OptionMenu(self, self.shield_var, *shield_names,
                                         command=lambda value: self.actions.equip_shield(value))
        self.shield_menu.grid(row=4,
                              column=0,
                              columnspan=2,
                              sticky="ew",
                              padx=5,
                              pady=5)
        self.enemy_menu = tk.OptionMenu(self, self.enemy_var, *enemy_names,
                                        command=self.on_enemy_selected)
        self.enemy_menu.grid(row=5, column=0,
                             columnspan=2, sticky="ew",
                             padx=5, pady=5)

        self.buy_herb_button = tk.Button(self, text="Buy Herb",
                                         command=lambda: self.actions.buy_herb())
        self.buy_herb_button.grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.start_fight_button = tk.Button(self, text="FIGHT!", command=lambda: self.actions.start_battle(),
                                            state="disabled")
        self.start_fight_button.grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

    def set_traces(self):
        self.level_var.trace("w", lambda name, index, mode: self.on_level_changed())
        self.name_var.trace("w", lambda name, index, mode: self.actions.change_name(self.name_var.get()))

    def on_level_changed(self) -> None:
        """Pass the level on, skipping edits that leave the box empty."""
        try:
            level = self.level_var.get()
        except tk.TclError:
            return
        self.actions.set_level(level)

    def refill_level(self) -> None:
        """Put the player's current level back in the box if it was left empty."""
        if self.level_spinbox.get() == "":
            self.level_var.set(self.player_level)

    def set_player_level(self, level: int) -> None:
        """Remember the player's current level for refilling the level box."""
        self.player_level = level

    def on_enemy_selected(self, name:str) -> None:
        """Pass the chosen enemy on and allow the fight to start."""
        self.actions.select_enemy(name)
        self.start_fight_button.config(state="normal")

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
