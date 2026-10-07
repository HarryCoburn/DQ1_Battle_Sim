import tkinter as tk
from functools import partial
from typing import Optional
from fightsim.views.actions import ViewActions

# Menu placeholders; neither is a Spell, so casting with one selected is refused
SELECT_SPELL = "Select Spell"
NO_MAGIC = "No Magic Available"


class BattleFrame(tk.Frame):
    """Optimized frame for conducting the fight."""

    def __init__(self, parent):
        super().__init__(parent)
        self.actions: Optional[ViewActions] = None
        self.magic_option_var = tk.StringVar(self)
        self.create_widgets()

    def bind_actions(self, actions: ViewActions):
        """ Sets the actions the battle buttons call """
        self.actions = actions

    def create_widgets(self):
        """Create and layout widgets for battle."""
        self.attack_btn = tk.Button(self, text="Attack", command=lambda: self.actions.attack())
        self.attack_btn.grid(row=0, column=0, padx=5, pady=5)
        self.herb_btn = tk.Button(self, text="Use Herb", command=lambda: self.actions.use_herb())
        self.herb_btn.grid(row=1, column=0, padx=5, pady=5)
        self.run_btn = tk.Button(self, text="Run", command=lambda: self.actions.flee())
        self.run_btn.grid(row=2, column=0, padx=5, pady=5)
        self.cast_btn = tk.Button(self, text="Cast",
                                  command=lambda: self.actions.cast_spell(self.magic_option_var.get()))
        self.cast_btn.grid(row=3, column=0, padx=5, pady=5)

        self.magic_menu = tk.OptionMenu(self, self.magic_option_var, NO_MAGIC)
        self.magic_menu.grid(row=3, column=1, padx=5, pady=5)
        self.magic_option_var.set(NO_MAGIC)

    def update_magic_menu(self, spells):
        """ Update the options available in the magic menu from the player's known spells. """
        menu = self.magic_menu['menu']
        menu.delete(0, 'end')

        labels = [SELECT_SPELL, *spells] if spells else [NO_MAGIC]
        # Keep the current selection if it's still available
        if self.magic_option_var.get() not in labels:
            self.magic_option_var.set(labels[0])

        for magic in labels:
            menu.add_command(label=magic, command=partial(self.set_magic_option, magic))

    def set_magic_option(self, magic):
        """ Set the current magic option in the OptionMenu. """
        self.magic_option_var.set(magic)
