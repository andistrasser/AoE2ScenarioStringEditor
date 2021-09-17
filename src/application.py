import os
import sys
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk

# constants
APP_TITLE = "AoE2ScenarioStringEditor"
THEME_DEFAULT = "clam"
THEME_WINDOWS = "vista"
LABEL_TAB_GENERAL = "General"
LABEL_TAB_PLAYERS = "Players"
LABEL_TAB_MESSAGES = "Messages"
LABEL_TAB_TRIGGERS = "Triggers"
LABEL_TAB_RAW = "Raw Content"
LABEL_SAVE = "Save"
LABEL_PLAYER = "Player "
LABEL_APPLY = "Apply"


# application class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self._build_ui()

    # creates a window and places widgets on it
    def _build_ui(self):
        self.geometry("720x470")
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

        # menu bar
        self.menu_bar = tk.Menu(self)

        # file menu
        menu_file = tk.Menu(self.menu_bar, tearoff=0)
        menu_file.add_command(label="Open", accelerator="Ctrl+O")
        menu_file.add_command(label="Save", accelerator="Ctrl+S")
        menu_file.add_command(label="Save as", accelerator="Shift+Ctrl+S")
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit, accelerator="Ctrl+Q")
        self.menu_bar.add_cascade(label="File", underline=0, menu=menu_file)

        # help menu
        menu_help = tk.Menu(self.menu_bar, tearoff=0)
        menu_help.add_command(label="Help", accelerator="F1")
        menu_help.add_command(label="About")
        self.menu_bar.add_cascade(label="Help", underline=0, menu=menu_help)

        self.config(menu=self.menu_bar)

        # tab view
        self.tab_view = ttk.Notebook(self)

        self.tab_general = ttk.Frame(self.tab_view)
        self.tab_players = ttk.Frame(self.tab_view)
        self.tab_messages = ttk.Frame(self.tab_view)
        self.tab_triggers = ttk.Frame(self.tab_view)
        self.tab_raw = ttk.Frame(self.tab_view)
        self.tab_view.add(self.tab_general, text=LABEL_TAB_GENERAL)
        self.tab_view.add(self.tab_players, text=LABEL_TAB_PLAYERS)
        self.tab_view.add(self.tab_messages, text=LABEL_TAB_MESSAGES)
        self.tab_view.add(self.tab_triggers, text=LABEL_TAB_TRIGGERS)
        self.tab_view.add(self.tab_raw, text=LABEL_TAB_RAW)
        self.tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="ewns")

        # player tab content
        self.player_labels = []
        self.player_entries = []

        for player_index in range(1, 9):
            label_player = ttk.Label(self.tab_players, text=(LABEL_PLAYER + str(player_index) + ":"))
            label_player.grid(row=(player_index - 1), column=0, padx=10, pady=(10, 0), sticky="e")

            self.player_labels.append(label_player)

            entry_player = ttk.Entry(self.tab_players, width=35)
            entry_player.grid(row=(player_index - 1), column=1, padx=0, pady=(10, 0), sticky="ew")

            self.player_entries.append(entry_player)

        self.textfield_raw = scrolledtext.ScrolledText(self.tab_raw)
        self.textfield_raw.grid(row=0, column=0, padx=10, pady=10, sticky="ewns")
        self.tab_raw.columnconfigure(0, weight=1)
        self.tab_raw.rowconfigure(0, weight=1)

        self.button_apply = ttk.Button(self.tab_raw, text=LABEL_APPLY)
        self.button_apply.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="e")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
