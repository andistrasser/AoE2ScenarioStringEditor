import os
import sys
import tkinter as tk
from tkinter import ttk

# constants
APP_TITLE = "AoE2ScenarioStringEditor"
THEME_DEFAULT = "clam"
THEME_WINDOWS = "vista"
LABEL_TAB_PLAYERS = "Players"
LABEL_TAB_MESSAGES = "Messages"
LABEL_TAB_TRIGGERS = "Triggers"
LABEL_SAVE = "Save"


# application class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self._build_ui()

    # creates a window and places widgets on it
    def _build_ui(self):
        self.geometry("720x450")
        self.title(APP_TITLE)
        self.style = ttk.Style(self)

        # set the app icon add change theme if executed on a windows systems
        if THEME_WINDOWS in self.style.theme_names():
            self.style.theme_use(THEME_WINDOWS)

            icon = "icon.ico"

            if not hasattr(sys, "frozen"):
                icon = os.path.join(os.path.dirname(__file__), icon)
            else:
                icon = os.path.join(sys.prefix, icon)

            self.iconbitmap(default=icon)
        else:
            self.style.theme_use(THEME_DEFAULT)

        self.tab_view = ttk.Notebook(self)

        self.tab_players = ttk.Frame(self.tab_view)
        self.tab_messages = ttk.Frame(self.tab_view)
        self.tab_triggers = ttk.Frame(self.tab_view)
        self.tab_view.add(self.tab_players, text=LABEL_TAB_PLAYERS)
        self.tab_view.add(self.tab_messages, text=LABEL_TAB_MESSAGES)
        self.tab_view.add(self.tab_triggers, text=LABEL_TAB_TRIGGERS)
        self.tab_view.pack(expand=1, fill="both")
        self.tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="ewns")

        self.button_save = ttk.Button(self, text=LABEL_SAVE)
        self.button_save.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.columnconfigure(0, weight=3)
        self.rowconfigure(0, weight=3)
