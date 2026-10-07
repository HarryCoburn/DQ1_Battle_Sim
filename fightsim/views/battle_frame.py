import tkinter as tk
from functools import partial
from fightsim.common.spells import Spell
from fightsim.views.actions import ViewActions

# Menu placeholder; not a Spell, so casting with it selected is refused
SELECT_SPELL = "Select Spell"
# Shown on the disabled menu when the player knows no spells; never offered as a choice
NO_SPELLS = "No Magic Available"


class BattleFrame(tk.Frame):
    """Frame for conducting the fight."""

    def __init__(self, parent):
        super().__init__(parent)
        self._spell_var = tk.StringVar(self)

        self.attack_btn = tk.Button(self, text="Attack")
        self.attack_btn.grid(row=0, column=0, padx=5, pady=5)
        self.herb_btn = tk.Button(self, text="Use Herb")
        self.herb_btn.grid(row=1, column=0, padx=5, pady=5)
        self.run_btn = tk.Button(self, text="Run")
        self.run_btn.grid(row=2, column=0, padx=5, pady=5)
        self.cast_btn = tk.Button(self, text="Cast")
        self.cast_btn.grid(row=3, column=0, padx=5, pady=5)

        self.magic_menu = tk.OptionMenu(self, self._spell_var, "")
        self.magic_menu.grid(row=3, column=1, padx=5, pady=5)
        self.update_magic_menu([])

    def bind_actions(self, actions: ViewActions):
        """ Sets the command each battle button calls """
        self.attack_btn.config(command=actions.attack)
        self.herb_btn.config(command=actions.use_herb)
        self.run_btn.config(command=actions.flee)
        self.cast_btn.config(command=lambda: actions.cast_spell(self._spell_var.get()))

    def update_magic_menu(self, spells: list[Spell]):
        """ Rebuilds the magic menu from the player's known spells, disabling casting if there are none. """
        menu = self.magic_menu['menu']
        menu.delete(0, 'end')

        if not spells:
            self._spell_var.set(NO_SPELLS)
            self.magic_menu.config(state="disabled")
            self.cast_btn.config(state="disabled")
            return

        self.magic_menu.config(state="normal")
        self.cast_btn.config(state="normal")
        labels = [SELECT_SPELL, *spells]
        # Keep the current selection if it's still available
        if self._spell_var.get() not in labels:
            self._spell_var.set(SELECT_SPELL)
        for label in labels:
            menu.add_command(label=label, command=partial(self._spell_var.set, label))
