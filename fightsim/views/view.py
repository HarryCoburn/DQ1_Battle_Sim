"""
view.py - The main window: the output area plus the setup and battle controls.
"""
from __future__ import annotations

import logging
import tkinter as tk
from typing import TYPE_CHECKING

from fightsim.views.setup_frame import SetupFrame
from fightsim.views.battle_frame import BattleFrame
from fightsim.views.main_frame import MainFrame
from fightsim.views.actions import ViewActions

if TYPE_CHECKING:
    from fightsim.models.enemy import Enemy
    from fightsim.models.player import Player

logger = logging.getLogger(__name__)

class View(tk.Tk):
    """
    View class for the application
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Side container with the control buttons, and main container with the output.
        # The window geometry sets the overall size; the controls take what they need.
        self.ctrl_container = tk.Frame(self)
        self.ctrl_container.pack(side="left", fill='y')

        self.main_container = tk.Frame(self)
        self.main_container.pack_propagate(False)
        self.main_container.pack(side="right", expand=True, fill='both')

        # Fixed frame: player, enemy and output labels
        self._main_frame = MainFrame(self.main_container)
        self._main_frame.pack(fill='x', expand=True)

        # Changeable control frames; one is shown at a time
        self._battle_frame = BattleFrame(self.ctrl_container)
        self._setup_frame = SetupFrame(self.ctrl_container, width=240, height=600, padx=20)
        self._curr_frame: tk.Frame | None = None

        self.configure_window()
        self.bind("<FocusOut>", lambda event: self.after_idle(self._close_menus_if_unfocused), add="+")

    def _close_menus_if_unfocused(self) -> None:
        """
        Closes any open dropdown once the app has lost focus to another window.
        Tk closes dropdowns on an outside click through a pointer grab, which fails under
        XWayland, so an open dropdown would otherwise float above other applications.
        """
        try:
            if self.focus_get() is not None:
                return
        except KeyError:  # focus is on a Tk-internal widget, so still inside the app
            return
        for menu in self._menus(self):
            if menu.winfo_ismapped():
                self.tk.call("tk::MenuUnpost", menu)

    def _menus(self, widget: tk.Misc):
        for child in widget.winfo_children():
            if isinstance(child, tk.Menu):
                yield child
            yield from self._menus(child)

    def report_callback_exception(self, exc, val, tb):
        """ Logs errors raised in button and other Tk callbacks instead of printing them to stderr """
        logger.error("Unhandled exception in Tk callback", exc_info=(exc, val, tb))

    def configure_window(self):
        """ Configure main window properties """
        self.title("DQ1 Battle Simulator")
        self.geometry("820x620+50+50")
        self.resizable(width=True, height=True)

    def show_player(self, player: Player) -> None:
        """ Fills the setup controls from the player; call before bind_actions() """
        self._setup_frame.show_player(player)

    def bind_actions(self, actions: ViewActions):
        """ Gives the frames the actions their controls call """
        self._battle_frame.bind_actions(actions)
        self._setup_frame.bind_actions(actions)

    def show_setup_screen(self) -> None:
        """ Shows the pre-battle setup controls """
        self._swap_controls(self._setup_frame)

    def show_battle_screen(self) -> None:
        """ Shows the battle controls """
        self._swap_controls(self._battle_frame)

    def _swap_controls(self, new_frame: tk.Frame) -> None:
        """ Hides the current control frame and packs new_frame in its place """
        if self._curr_frame is not None:
            self._curr_frame.pack_forget()
        self._curr_frame = new_frame
        new_frame.pack(fill='x', expand=True)
        logger.debug("Switched to frame: %s", new_frame)

    def update_player_info(self, player: Player) -> None:
        """ Refreshes the player label in _main_frame, the magic menu in _battle_frame and the level in _setup_frame """
        self._main_frame.update_player_label(player)
        self._battle_frame.update_magic_menu(player.player_magic)
        self._setup_frame.set_player_level(player.level)

    def update_enemy_info(self, enemy: Enemy | None) -> None:
        """ Refreshes the enemy label in _main_frame """
        self._main_frame.update_enemy_label(enemy)

    def append_output(self, message: str) -> None:
        """ Adds message to the output widget in _main_frame """
        self._main_frame.append_output(message)

    def clear_output(self) -> None:
        """ Clears the output widget in _main_frame """
        self._main_frame.clear_output()
