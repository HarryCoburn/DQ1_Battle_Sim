import tkinter as tk
import tkinter.scrolledtext as scrolledtext


class MainFrame(tk.Frame):
    """
    Main frame of the program. Holds output
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.configure(bg='purple')

        # Player Label
        self.player_label = tk.Label(
            master=self,
            borderwidth=1,
            relief="solid",
            anchor=tk.NW,
            font=('consolas', '12'),
        )
        self.player_label.grid(column=0, row=0, sticky="n", padx=10, ipadx=3)

        # Enemy label
        self.enemy_label = tk.Label(
            master=self,
            borderwidth=1,
            relief="solid",
            anchor=tk.NW,
            font=('consolas', '12'),
            text="Enemy not selected.",
        )
        self.enemy_label.grid(column=1, row=0, sticky="n", padx=10, ipadx=3)

        # Output window
        self.txt = scrolledtext.ScrolledText(
            master=self,
            undo=True,
            font=('consolas', '12'),
            width=40,
            wrap=tk.WORD
        )
        self.txt.grid(column=2, row=0, padx=10, ipadx=3)
        self.txt.configure(state="disabled")

    def set_controller(self, controller):
        self.controller = controller
