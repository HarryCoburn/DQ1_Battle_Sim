"""
setup_frame.py - Pre-battle controls: name, level, equipment, herbs and enemy choice.
"""
from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from typing import TYPE_CHECKING

from fightsim.models.items import weapon_names, armor_names, shield_names
from fightsim.models.enemy import enemy_names
from fightsim.models.player_leveling import MIN_LEVEL, MAX_LEVEL
from fightsim.views.actions import ViewActions

if TYPE_CHECKING:
    from fightsim.models.player import Player


def _bind_menu(option_menu: tk.OptionMenu, variable: tk.StringVar, callback: Callable[[str], None]) -> None:
    """Makes each entry of option_menu set variable and then call callback with its label."""
    menu = option_menu["menu"]
    for index in range(menu.index("end") + 1):
        label = menu.entrycget(index, "label")

        def choose(value: str = label) -> None:
            variable.set(value)
            callback(value)

        menu.entryconfigure(index, command=choose)


class SetupFrame(tk.Frame):
    """
    Frame for fight setup buttons
    """

    def __init__(self, parent, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.player_level = MIN_LEVEL
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.weapon_var = tk.StringVar()
        self.armor_var = tk.StringVar()
        self.shield_var = tk.StringVar()
        self.level_var = tk.IntVar(value=MIN_LEVEL)
        self.name_var = tk.StringVar()
        self.enemy_var = tk.StringVar(value="Select Enemy")
        self.create_widgets()

    def create_widgets(self):
        """Create and layout widgets for setup"""
        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="e", padx=5)
        tk.Entry(self, textvariable=self.name_var, width=20).grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(self, text="Level:").grid(row=1, column=0, sticky="e", padx=5)
        self.level_spinbox = tk.Spinbox(self, from_=MIN_LEVEL, to=MAX_LEVEL, increment=1, width=5,
                                        textvariable=self.level_var,
                                        wrap=True,
                                        validate='key',
                                        validatecommand=(self.register(self.level_validate), '%P'))
        self.level_spinbox.grid(row=1, column=1, sticky="w", pady=5)
        self.level_spinbox.bind("<FocusOut>", lambda event: self.refill_level())

        self.weapon_menu = tk.OptionMenu(self, self.weapon_var, *weapon_names)
        self.weapon_menu.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.armor_menu = tk.OptionMenu(self, self.armor_var, *armor_names)
        self.armor_menu.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.shield_menu = tk.OptionMenu(self, self.shield_var, *shield_names)
        self.shield_menu.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.enemy_menu = tk.OptionMenu(self, self.enemy_var, *enemy_names)
        self.enemy_menu.grid(row=5, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.buy_herb_button = tk.Button(self, text="Buy Herb")
        self.buy_herb_button.grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.start_fight_button = tk.Button(self, text="FIGHT!", state="disabled")
        self.start_fight_button.grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

    def show_player(self, player: Player) -> None:
        """
        Fills the controls from the player. Call before bind_actions(), so filling them
        doesn't send the values straight back as changes.
        """
        self.name_var.set(player.name)
        self.level_var.set(player.level)
        self.weapon_var.set(player.weapon.name)
        self.armor_var.set(player.armor.name)
        self.shield_var.set(player.shield.name)
        self.player_level = player.level

    def bind_actions(self, actions: ViewActions):
        """ Connects every setup control to the action it calls """
        _bind_menu(self.weapon_menu, self.weapon_var, actions.equip_weapon)
        _bind_menu(self.armor_menu, self.armor_var, actions.equip_armor)
        _bind_menu(self.shield_menu, self.shield_var, actions.equip_shield)
        _bind_menu(self.enemy_menu, self.enemy_var, lambda name: self._enemy_chosen(actions, name))
        self.buy_herb_button.config(command=actions.buy_herb)
        self.start_fight_button.config(command=actions.start_battle)
        self.level_var.trace_add("write", lambda name, index, mode: self._level_changed(actions))
        self.name_var.trace_add("write", lambda name, index, mode: actions.change_name(self.name_var.get()))

    def _level_changed(self, actions: ViewActions) -> None:
        """Pass the level on, skipping edits that leave the box empty."""
        try:
            level = self.level_var.get()
        except tk.TclError:
            return
        actions.set_level(level)

    def _enemy_chosen(self, actions: ViewActions, name: str) -> None:
        """Pass the chosen enemy on and allow the fight to start."""
        actions.select_enemy(name)
        self.start_fight_button.config(state="normal")

    def refill_level(self) -> None:
        """Put the player's current level back in the box if it was left empty."""
        if self.level_spinbox.get() == "":
            self.level_var.set(self.player_level)

    def set_player_level(self, level: int) -> None:
        """Remember the player's current level for refilling the level box."""
        self.player_level = level

    @staticmethod
    def level_validate(p: str) -> bool:
        """ Allows an empty box or a whole number within the level range """
        return p == "" or (p.isdigit() and MIN_LEVEL <= int(p) <= MAX_LEVEL)
