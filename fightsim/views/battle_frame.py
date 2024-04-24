import tkinter as tk


class BattleFrame(tk.Frame):
    """Optimized frame for conducting the fight."""

    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None
        self.attack_btn = None
        self.herb_btn = None
        self.run_btn = None
        self.cast_btn = None
        self.magic_option_var = None
        self.magic_menu = None
        self.magic = None
        self.show_model_btn = None

    def set_controller(self, controller):
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """Create and layout widgets for battle."""
        self.attack_btn = tk.Button(self, text="Attack", command=self.controller.battle.player_attack)
        self.attack_btn.grid(row=0, column=0, padx=5, pady=5)
        self.herb_btn = tk.Button(self, text="Use Herb", command=self.controller.battle.use_herb)
        self.herb_btn.grid(row=1, column=0, padx=5, pady=5)
        self.run_btn = tk.Button(self, text="Run", command=self.controller.battle.player_flees)
        self.run_btn.grid(row=2, column=0, padx=5, pady=5)
        self.cast_btn = tk.Button(self, text="Cast", command=self.controller.battle.player_cast_magic)
        self.cast_btn.grid(row=3, column=0, padx=5, pady=5)

        # Note: Update the OptionMenu for magic dynamically based on available spells
        self.magic_option_var = tk.StringVar(self)
        self.magic_option_var.set("No Spells Available")  # Initial placeholder.
        self.magic_menu = tk.OptionMenu(self, self.magic_option_var, "No spells available")
        self.magic_menu.grid(row=3, column=1, padx=5, pady=5)

        # self.magic = tk.OptionMenu(self, self.controller.chosen_magic, *self.controller.spell_strings)
        # self.magic.grid(row=3, column=1, padx=5, pady=5)

        # May cut
        # self.show_model_btn = tk.Button(self, text="Show Model", command=self.show_model)
        # self.show_model_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def update_player_magic_menu(self, player_magic):
        self.magic_menu["menu"].delete(0, "end")
        for spell in player_magic:
            self.magic_menu["menu"].add_command(label=spell,
                                                command=lambda value=spell: self.magic_option_var.set(value))

    def attack(self):
        """Placeholder for attack action."""
        print("Attacked.")

    def use_herb(self):
        """Placeholder for using a herb."""
        print("Herb used.")

    def run(self):
        """Placeholder for run action."""
        print("Attempted to run.")

    def cast_spell(self):
        """Placeholder for casting a spell."""
        print("Spell cast.")

    def show_model(self):
        """Placeholder for showing model stats."""
        print("Model stats shown.")

    def update_magic_menu(self, spell_list):
        # reset menu
        self.magic_menu['menu'].delete(0, 'end')
