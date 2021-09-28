import os
import sys
import tkinter as tk
from tkinter import Scrollbar
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk

# constants
MENU_OPEN = 0
MENU_RELOAD = 1
MENU_SAVE = 2
MENU_SAVE_AS = 3
MENU_EXIT = 5
MENU_HELP = 0
MENU_ABOUT = 1
APP_TITLE = "AoE2ScenarioStringEditor"
THEME_DEFAULT = "clam"
THEME_WINDOWS = "vista"
LABEL_TAB_GENERAL = "General"
LABEL_TAB_PLAYERS = "Players"
LABEL_TAB_MESSAGES = "Messages"
LABEL_TAB_TRIGGERS = "Triggers"
LABEL_TAB_RAW = "Raw"
LABEL_PLAYER = "Player "
LABEL_APPLY = "Apply"
LABEL_OPEN = "Open"
LABEL_RELOAD = "Reload"
LABEL_SAVE = "Save"
LABEL_SAVE_AS = "Save as"
LABEL_EXIT = "Exit"
LABEL_FILE = "File"
LABEL_HELP = "Help"
LABEL_ABOUT = "About"
LABEL_SCENARIO_NAME = "Internal file name:"
LABEL_FILE_EXTENSION = ".aoe2scenario"
TITLE_ERROR = "Error"
COMBOBOX_MESSAGES_CONTENT = ["Scenario Instructions", "Hints", "Victory", "Loss", "History", "Scout"]


# user interface class
class UserInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self._build_ui()

    # builds the user interface
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
        menu_bar = tk.Menu(self)

        # file menu
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.insert(MENU_OPEN, "command", label=LABEL_OPEN, accelerator="Ctrl+O")
        menu_file.insert(MENU_RELOAD, "command", label=LABEL_RELOAD, accelerator="Ctrl+R")
        menu_file.insert(MENU_SAVE, "command", label=LABEL_SAVE, accelerator="Ctrl+S")
        menu_file.insert(MENU_SAVE_AS, "command", label=LABEL_SAVE_AS, accelerator="Ctrl+Alt+S")
        menu_file.add_separator()
        menu_file.insert(MENU_EXIT, "command", label=LABEL_EXIT, command=self.quit, accelerator="Ctrl+Q")
        self.menu_file = menu_file
        menu_bar.add_cascade(label=LABEL_FILE, menu=menu_file)

        # help menu
        menu_help = tk.Menu(menu_bar, tearoff=0)
        menu_help.insert(MENU_HELP, "command", label=LABEL_HELP, accelerator="F1")
        menu_help.insert(MENU_ABOUT, "command", label=LABEL_ABOUT)
        self.menu_help = menu_help
        menu_bar.add_cascade(label=LABEL_HELP, menu=menu_help)

        self.config(menu=menu_bar)

        # tab view
        tab_container = ttk.Notebook(self)

        tab_general = ttk.Frame(tab_container)
        tab_players = ttk.Frame(tab_container)
        tab_messages = ttk.Frame(tab_container)
        tab_triggers = ttk.Frame(tab_container)
        tab_raw = ttk.Frame(tab_container)
        tab_container.add(tab_general, text=LABEL_TAB_GENERAL)
        tab_container.add(tab_players, text=LABEL_TAB_PLAYERS)
        tab_container.add(tab_messages, text=LABEL_TAB_MESSAGES)
        tab_container.add(tab_triggers, text=LABEL_TAB_TRIGGERS)
        tab_container.add(tab_raw, text=LABEL_TAB_RAW)
        tab_container.grid(row=0, column=0, padx=10, pady=10, sticky="ewns")

        # general tab widgets
        label_scenario_name = ttk.Label(tab_general, text=LABEL_SCENARIO_NAME)
        label_scenario_name.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="e")

        self.entry_file_name = ttk.Entry(tab_general, width=30)
        self.entry_file_name.grid(row=0, column=1, padx=0, pady=(10, 0), sticky="e")

        label_file_extension = ttk.Label(tab_general, text=LABEL_FILE_EXTENSION)
        label_file_extension.grid(row=0, column=2, pady=(10, 0), sticky="e")

        # player tab widgets
        self.player_labels = []
        self.player_entries = []

        for player_index in range(1, 9):
            label_player = ttk.Label(tab_players, text=(LABEL_PLAYER + str(player_index) + ":"))
            label_player.grid(row=(player_index - 1), column=0, padx=10, pady=(10, 0), sticky="e")

            self.player_labels.append(label_player)

            entry_player = ttk.Entry(tab_players, width=35)
            entry_player.grid(row=(player_index - 1), column=1, padx=0, pady=(10, 0), sticky="ew")

            self.player_entries.append(entry_player)

        # messages tab widgets
        self.combobox_message = ttk.Combobox(tab_messages, values=COMBOBOX_MESSAGES_CONTENT)
        self.combobox_message.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nw")
        self.combobox_message.current(0)

        self.textfield_message = scrolledtext.ScrolledText(tab_messages)
        self.textfield_message.grid(row=0, column=1, padx=10, pady=10, sticky="ewns")

        tab_messages.columnconfigure(1, weight=1)
        tab_messages.rowconfigure(0, weight=1)

        # triggers tab widgets
        self.listbox_triggers = tk.Listbox(tab_triggers, width=60)
        self.listbox_triggers.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="ewns")
        scrollbar_triggers = Scrollbar(tab_triggers, orient="vertical", command=self.listbox_triggers.yview)
        scrollbar_triggers.grid(row=0, column=1, pady=10, sticky="ns")
        self.listbox_triggers.config(yscrollcommand=scrollbar_triggers.set)

        self.textfield_triggers = scrolledtext.ScrolledText(tab_triggers)
        self.textfield_triggers.grid(row=0, column=2, padx=10, pady=10, sticky="ewns")
        tab_triggers.columnconfigure(0, weight=1)
        tab_triggers.columnconfigure(2, weight=1)
        tab_triggers.rowconfigure(0, weight=1)

        # raw tab widgets
        self.textfield_raw = scrolledtext.ScrolledText(tab_raw)
        self.textfield_raw.grid(row=0, column=0, padx=10, pady=10, sticky="ewns")
        tab_raw.columnconfigure(0, weight=1)
        tab_raw.rowconfigure(0, weight=1)

        self.button_apply = ttk.Button(tab_raw, text=LABEL_APPLY)
        self.button_apply.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="e")

        # separator
        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=1, column=0, sticky="ew")

        # status bar
        self.status = tk.StringVar()
        label_status_bar = ttk.Label(self, textvariable=self.status)
        label_status_bar.grid(row=2, column=0, padx=2, pady=2, sticky="w")

        # make tabs expand with the window
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    # locks the ui to prevent unwanted input
    def lock(self, lock):
        state = "normal"

        if lock:
            state = "disabled"

        self.menu_file.entryconfig(MENU_RELOAD, state=state)
        self.menu_file.entryconfig(MENU_SAVE, state=state)
        self.menu_file.entryconfig(MENU_SAVE_AS, state=state)
        self.entry_file_name.config(state=state)
        self.combobox_message.config(state=state)
        self.textfield_message.config(state=state)
        self.listbox_triggers.config(state=state)
        self.textfield_triggers.config(state=state)
        self.textfield_raw.config(state=state)
        self.button_apply.config(state=state)

        for player_entry in self.player_entries:
            player_entry.config(state=state)

    # sets the status bar text
    def set_status(self, text):
        self.status.set(text)
        self.update()

    # sets the text of a given textfield
    @staticmethod
    def set_textfield_text(textfield, text):
        textfield.delete(1.0, "end")
        textfield.insert(1.0, text)

    # shows an error dialog
    @staticmethod
    def show_error_dialog(message):
        messagebox.showerror(TITLE_ERROR, message)

    # shows an info dialog
    @staticmethod
    def show_info_dialog(title, message):
        messagebox.showinfo(title, message)

    # quits the application
    def exit(self, _event=None):
        self.quit()
