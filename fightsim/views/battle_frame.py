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
        self.magic_option_var = tk.StringVar(self)
        self.magic_menu = None

    def set_controller(self, controller):
        self.controller = controller
        self.player_magic = self.controller.model.player.player_magic
        if not self.player_magic:
            self.player_magic = ["No Magic Available"]
        self.magic_option_var.set(self.player_magic[0])
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

        self.magic_menu = tk.OptionMenu(self, self.magic_option_var, *self.player_magic)
        self.magic_menu.grid(row=3, column=1, padx=5, pady=5)



    def update_player_magic_menu(self):
        player_magic = self.controller.model.player.player_magic

        # Clear current entries
        self.magic_menu['menu'].delete(0, 'end')

        if not player_magic:  # If the list is empty, provide a default 'No Magic' option
            self.magic_option_var.set("No Magic Available")
            self.magic_menu['menu'].add_command(label="No Magic Available",
                                                command=lambda: self.magic_option_var.set("No Magic Available"))
        else:
            # Set the default value to the first item in the list
            self.magic_option_var.set(player_magic[0])
            # Add new options to the menu
            for magic in player_magic:
                self.magic_menu['menu'].add_command(label=magic, command=tk._setit(self.magic_option_var, magic))


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
