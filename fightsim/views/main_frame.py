import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import inspect


class MainFrame(tk.Frame):
    """
    Main frame of the program. Holds output
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.configure(bg='purple')
        self.parent = parent
        self.controller = None

        top_spacer = tk.Frame(self, height=12, bg='purple')
        top_spacer.pack(fill='both', expand=True)

        # Container for labels to align them nicely centered vertically
        label_container = tk.Frame(self, bg='purple')
        label_container.pack(fill='x')  # Horizontal packing within the frame, not expanded

        # Player Label
        self.player_label = tk.Label(
            master=label_container,
            borderwidth=1,
            relief="solid",
            anchor="center",
            font=('consolas', '12'),
            padx=20,
            text="Player: Not selected"
        )
        self.player_label.pack(side='left', fill='both', padx=10)  # Pack to the left, filling horizontally

        # Enemy Label
        self.enemy_label = tk.Label(
            master=label_container,
            borderwidth=1,
            relief="solid",
            anchor="center",
            font=('consolas', '12'),
            padx=20,
            width=28,
            height=16,
            text="Enemy not selected.",
        )
        self.enemy_label.pack(side='left', fill='none', padx=10)  # Pack next to the player label

        # Bottom spacer
        bottom_spacer = tk.Frame(self, height=1, bg='purple')
        bottom_spacer.pack(fill='both', expand=True)

        # Output window
        self.txt = scrolledtext.ScrolledText(
            master=self,
            undo=True,
            font=('consolas', '12'),
            width=40,
            wrap=tk.WORD
        )
        self.txt.pack(fill='both', expand=True, padx=10, pady=10)  # Fill both horizontally and vertically
        self.txt.configure(state="disabled")

    def set_controller(self, controller):
        self.controller = controller

    def update_player_label(self, player_info):
        """
        Updates the player label
        """
        print("Trying to update the label.")
        self.player_label["text"] = inspect.cleandoc(f"""\
              Name: {player_info.name}
              Level: {player_info.level}
              HP: {player_info.current_hp}/{player_info.max_hp}
              MP: {player_info.current_mp}

              Weapon: {player_info.weapon.name}
              Armor: {player_info.armor.name}
              Shield: {player_info.shield.name}

              Strength: {player_info.strength}
              Agility: {player_info.agility}

              Herbs remaining: {player_info.herb_count}

              Asleep?: {player_info.is_asleep}
              Spells stopped?: {player_info.is_spellstopped}
          """)

    def update_enemy_label(self, enemy_info):
        if enemy_info is None:
            self.enemy_label["text"] = "Enemy not selected."
        else:
            """
            Updates enemy label
            """
            self.enemy_label["text"] = inspect.cleandoc(f"""\
                Name: {enemy_info.name}
                HP: {enemy_info.current_hp}
    
                Strength: {enemy_info.strength}
                Agility: {enemy_info.agility}
            """)

    def update_output(self, _, message):
        """Appends output to the main output window"""
        self.txt.configure(state='normal')  # Enable text widget for editing
        self.txt.insert(tk.END, message + "\n")  # Append new message
        self.txt.configure(state='disabled')  # Disable text widget to prevent editing
        self.txt.see(tk.END)  # Auto-scroll to the end

    def clear_output(self):
        """Erases all output in the main output"""
        self.txt["state"] = 'normal'
        self.txt.delete(1.0, tk.END)
