'''
    view.py - Holds the view for the MVC program
'''

import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import inspect
from .items import weapon_names, armor_names, shield_names
from .enemy import enemy_names

class View(tk.Tk):
    '''
    View class for the application
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Using super() for a cleaner call to the parent class constructor


        # Initialize View Variables
        self.init_variables()

        # Configure main window
        self.configure_window()

        # Create and lay out containers
        self.setup_containers()        

    def init_variables(self):
        self.name_text = tk.StringVar(value="Rollo")        
        self.level_change = tk.StringVar(value="1")
        self.chosen_weapon = tk.StringVar(value="Unarmed")        
        self.chosen_armor = tk.StringVar(value="Naked")                
        self.chosen_shield = tk.StringVar(value="No Shield")        
        self.chosen_enemy = tk.StringVar(value= "Select Enemy")        
        self.chosen_magic = tk.StringVar(value="No spells available.")        
        self.spell_strings = [] # To be dynamically updated
        self.curr_frame = None
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller
        # Initialize and display frames
        self.init_frames()
    
    def configure_window(self):
        """ Configure main window properties """
        self.title("DQ1 Battle Simulator")
        self.geometry("1224x620+50+50")        

    def setup_containers(self):
        ''' Setup the main containers for control and main area'''

        # Define
        self.ctrl_container = tk.Frame(self, height=768, width=256, bg="blue")
        self.main_container = tk.Frame(self, height=768, width=768, bg="red")

        # Pack it
        self.ctrl_container.pack(side="left", fill="both", expand=True)
        self.main_container.pack(side="right", fill="both", expand=True)

        # Grid it
        self.ctrl_container.grid_rowconfigure(0, weight=1)
        self.ctrl_container.grid_columnconfigure(0, weight=1)
        self.ctrl_container.grid_propagate(False)

        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

    def init_frames(self):
        # Set up the main frame.
        self.main_frame = MainFrame(self.main_container, self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.frames = {
            SetupFrame: SetupFrame(self.ctrl_container),
            BattleFrame: BattleFrame(self.ctrl_container)
        }
        for frame in self.frames.values():
            frame.set_controller(self.controller)


        #Display initial frame
        self.show_frame(SetupFrame)

        

    def show_frame(self, cont):
        '''
        Switches one frame for another. Assumes frames are overlapping.
        '''
        frame = self.frames[cont]
        if self.curr_frame is not None:
            self.curr_frame.grid_remove()
        self.curr_frame=frame        
        frame.grid(row=0, column=0)        


    def update_magic(self):
        '''
        Updates the magic menu in BattleFrame
        '''
        menu = self.frames[BattleFrame].magic["menu"]
        menu.delete(0, "end")
        for string in self.spell_strings:
            menu.add_command(label=string,
                             command=lambda value=string: self.chosen_magic.set(value))

    def update_player_label(self, pinfo):
        '''
        Updates the player label
        '''
        print("Trying to update the label.")
        self.main_frame.player_label["text"] = inspect.cleandoc(f'''\
            Name: {pinfo.name}
            Level: {pinfo.level}
            HP: {pinfo.curr_hp}/{pinfo.max_hp}
            MP: {pinfo.curr_mp}

            Weapon: {pinfo.weapon.name}
            Armor: {pinfo.armor.name}
            Shield: {pinfo.shield.name}

            Strength: {pinfo.strength}
            Agility: {pinfo.agility}

            Herbs remaining: {pinfo.herb_count}

            Asleep?: {pinfo.is_asleep}
            Spells stopped?: {pinfo.is_spellstopped}
        ''')
        self.spell_strings = pinfo.player_magic

    def update_einfo(self, einfo):
        '''
        Updates enemy label
        '''
        print(einfo)
        self.main_frame.enemy_label["text"] = inspect.cleandoc(f'''\
            Name: {einfo.name}
            HP: {einfo.current_hp}

            Strength: {einfo.strength}
            Agility: {einfo.agility}
        ''')

    def update_output(self, message):        
        '''Appends output to the main output window'''
        self.main_frame.txt.configure(state='normal')  # Enable text widget for editing
        self.main_frame.txt.insert(tk.END, message + "\n")  # Append new message
        self.main_frame.txt.configure(state='disabled')  # Disable text widget to prevent editing
        self.main_frame.txt.see(tk.END)  # Auto-scroll to the end        

    def clear_output(self):
        '''Erases all output in the main output'''
        self.main_frame.txt["state"] = 'normal'
        self.main_frame.txt.delete(1.0, tk.END)

class SetupFrame(tk.Frame):
    '''
    Frame for fight setup buttons
    '''
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None
        self._level_value = tk.StringVar(value=1)        
         
    def set_controller(self, controller):
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):        
        '''Create and layout widgets for setup'''
        # Simplified layout using grid
        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="e", padx=5)
        tk.Entry(self, textvariable=self.controller.name_text, width=20).grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(self, text="Level:").grid(row=1, column=0, sticky="e", padx=5)
        tk.Spinbox(self, from_=1, to=30, width=5, textvariable=self.controller.level_change, validate='all', validatecommand=(self.register(self.level_validate), '%P')).grid(row=1, column=1, sticky="w", pady=5)

        tk.OptionMenu(self, self.controller.chosen_weapon, *weapon_names).grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        tk.OptionMenu(self, self.controller.chosen_armor, *armor_names).grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)        
        tk.OptionMenu(self, self.controller.chosen_shield, *shield_names).grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        tk.OptionMenu(self, self.controller.chosen_enemy, "Select Enemy", *enemy_names).grid(row=5, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.buy_herb_button = tk.Button(self, text="Buy Herb", command=self.controller.buy_herb)
        self.buy_herb_button.grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.start_fight_button = tk.Button(self, text="FIGHT!", command=self.controller.start_fight)
        self.start_fight_button.grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

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

class BattleFrame(tk.Frame):   
    '''Optimized frame for conducting the fight.'''
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        '''Create and layout widgets for battle.'''
        self.attack_btn = tk.Button(self, text="Attack", command=self.attack)
        self.attack_btn.grid(row=0, column=0, padx=5, pady=5)
        self.herb_btn = tk.Button(self, text="Use Herb", command=self.use_herb)
        self.herb_btn.grid(row=1, column=0, padx=5, pady=5)
        self.run_btn = tk.Button(self, text="Run", command=self.run)
        self.run_btn.grid(row=2, column=0, padx=5, pady=5)
        self.cast_btn = tk.Button(self, text="Cast", command=self.cast_spell)
        self.cast_btn.grid(row=3, column=0, padx=5, pady=5)
        # Note: Update the OptionMenu for magic dynamically based on available spells
        self.magic_option_var = tk.StringVar(self)
        self.magic_option_var.set("No Spells Available") # Initial placeholder.
        self.magic_menu = tk.OptionMenu(self, self.magic_option_var, "No spells available")
        self.magic_menu.grid(row=3, column=1, padx=5, pady=5)
        # self.magic = tk.OptionMenu(self, self.controller.chosen_magic, *self.controller.spell_strings).grid(row=3, column=1, padx=5, pady=5)
        self.show_model_btn = tk.Button(self, text="Show Model", command=self.show_model)
        self.show_model_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def attack(self):
        '''Placeholder for attack action.'''
        print("Attacked.")

    def use_herb(self):
        '''Placeholder for using a herb.'''
        print("Herb used.")

    def run(self):
        '''Placeholder for run action.'''
        print("Attempted to run.")

    def cast_spell(self):
        '''Placeholder for casting a spell.'''
        print("Spell cast.")

    def show_model(self):
        '''Placeholder for showing model stats.'''
        print("Model stats shown.")

    def update_magic_menu(self, spell_list):
        #reset menu
        self.magic_menu['menu'].delete(0, 'end')

class MainFrame(tk.Frame):
    '''
    Main frame of the program. Holds output
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='purple')
        self.controller = controller

        # Player Label
        self.player_label = tk.Label(
            master=self,            
            borderwidth=1,
            relief="solid",
            anchor=tk.NW,
            font=('consolas','12'),            
            )
        self.player_label.grid(column=0, row=0, sticky="n", padx=10, ipadx=3)


        #Enemey label
        self.enemy_label = tk.Label(
            master=self,            
            borderwidth=1,
            relief="solid",
            anchor=tk.NW,
            font=('consolas','12'),
            text="Enemy not selected.",            
            )
        self.enemy_label.grid(column=1, row=0, sticky="n", padx=10, ipadx=3)

        #Output window
        self.txt = scrolledtext.ScrolledText(
            master=self,
            undo=True,
            font=('consolas','12'),
            width=40,            
            wrap=tk.WORD
            )
        self.txt.grid(column=2, row=0, padx=10, ipadx=3)
        self.txt.configure(state="disabled")
