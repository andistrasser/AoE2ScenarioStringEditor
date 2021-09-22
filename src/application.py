import os
import sys
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter.filedialog import askopenfilename

import trigger_item as ti
from scenario_handler import ScenarioHandler
from trigger_item import TriggerItem

# constants
EFFECT_56 = 56
EFFECT_91 = 91
NO_EFFECT = -1
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
LABEL_SCENARIO_NAME = "Scenario name:"
STATUS_NO_SCENARIO_LOADED = "no scenario file loaded at the moment"
STATUS_LOADING = "loading "
STATUS_LOADING_SUCCESSFUL = " loaded successfully"
STATUS_LOADING_FAILED = " could not be loaded"
COMBOBOX_MESSAGES_CONTENT = ["Scenario Instructions", "Hints", "Victory", "Loss", "History", "Scout"]
FILETYPES = [("AoE2DE scenario file", "*.aoe2scenario")]


# application class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self._init()
        self._build_ui()

    # initialize variables
    def _init(self):
        self.file = ""
        self.status = tk.StringVar()
        self.status.set(STATUS_NO_SCENARIO_LOADED)
        self.player_count = 0
        self.content_players = []
        self.content_messages = []
        self.content_triggers = []

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
        menu_file.add_command(label=LABEL_OPEN, accelerator="Ctrl+O", command=self._open_file)
        menu_file.add_command(label=LABEL_RELOAD, accelerator="Ctrl+R")
        menu_file.add_command(label=LABEL_SAVE, accelerator="Ctrl+S")
        menu_file.add_command(label=LABEL_SAVE_AS, accelerator="Shift+Ctrl+S")
        menu_file.add_separator()
        menu_file.add_command(label=LABEL_EXIT, command=self.quit, accelerator="Ctrl+Q")
        self.menu_bar.add_cascade(label=LABEL_FILE, underline=0, menu=menu_file)

        # help menu
        menu_help = tk.Menu(self.menu_bar, tearoff=0)
        menu_help.add_command(label=LABEL_HELP, accelerator="F1")
        menu_help.add_command(label=LABEL_ABOUT)
        self.menu_bar.add_cascade(label=LABEL_HELP, underline=0, menu=menu_help)

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

        # general tab content
        self.label_scenario_name = ttk.Label(self.tab_general, text=LABEL_SCENARIO_NAME)
        self.label_scenario_name.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="e")

        self.entry_scenario_name = ttk.Entry(self.tab_general, width=35)
        self.entry_scenario_name.grid(row=0, column=1, padx=0, pady=(10, 0), sticky="ew")

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

        # messages tab content
        self.combobox_message = ttk.Combobox(self.tab_messages, values=COMBOBOX_MESSAGES_CONTENT)
        self.combobox_message.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nw")
        self.combobox_message.current(0)

        self.textfield_message = scrolledtext.ScrolledText(self.tab_messages)
        self.textfield_message.grid(row=0, column=1, padx=10, pady=10, sticky="ewns")

        self.tab_messages.columnconfigure(1, weight=1)
        self.tab_messages.rowconfigure(0, weight=1)

        # triggers tab content
        self.listbox_triggers = tk.Listbox(self.tab_triggers, width=60)
        self.listbox_triggers.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="ewns")
        # self.listbox_triggers.insert(1, "[D] Refugees Spawn (one time) - E#0: Display Instructions")
        # self.listbox_triggers.insert(2, "[D] First Group in East - E#0: Display Instructions")

        self.textfield_triggers = scrolledtext.ScrolledText(self.tab_triggers)
        self.textfield_triggers.grid(row=0, column=1, padx=10, pady=10, sticky="ewns")
        self.tab_triggers.columnconfigure(0, weight=1)
        self.tab_triggers.columnconfigure(1, weight=1)
        self.tab_triggers.rowconfigure(0, weight=1)

        # raw tab content
        self.textfield_raw = scrolledtext.ScrolledText(self.tab_raw)
        self.textfield_raw.grid(row=0, column=0, padx=10, pady=10, sticky="ewns")
        self.tab_raw.columnconfigure(0, weight=1)
        self.tab_raw.rowconfigure(0, weight=1)

        self.button_apply = ttk.Button(self.tab_raw, text=LABEL_APPLY)
        self.button_apply.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="e")

        # status bar
        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=1, column=0, sticky="ew")
        self.label_status_bar = ttk.Label(self, textvariable=self.status)
        self.label_status_bar.grid(row=2, column=0, padx=2, pady=2, sticky="w")

        # make tabs expand with the window
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def _set_status(self, text):
        self.status.set(text)
        self.update()

    def _open_file(self):
        self.file_path = askopenfilename(filetypes=FILETYPES)
        self.scenario_handler = ScenarioHandler(self.file_path)

        if len(self.file_path) == 0:
            return

        file_name = os.path.basename(self.file_path)

        try:
            self._set_status(STATUS_LOADING + file_name)
            self.scenario = self.scenario_handler.load_scenario()
            self._load_content_from_scenario()
            self._load_content_into_ui()
            self._set_status(file_name + STATUS_LOADING_SUCCESSFUL)
        except:
            self._set_status(file_name + STATUS_LOADING_FAILED)

    def _load_content_from_scenario(self):
        # file header section
        file_header_section = self.scenario.sections["FileHeader"]

        self.player_count = file_header_section.player_count

        # data header section
        data_header_section = self.scenario.sections["DataHeader"]

        for index in range(0, 8):
            player_name = str(data_header_section.player_names[index])

            self.content_players.append(player_name.replace("\x00", ""))

        # messages section
        messages_section = self.scenario.sections["Messages"]

        self.content_messages.append(messages_section.ascii_instructions)
        self.content_messages.append(messages_section.ascii_hints)
        self.content_messages.append(messages_section.ascii_victory)
        self.content_messages.append(messages_section.ascii_loss)
        self.content_messages.append(messages_section.ascii_history)
        self.content_messages.append(messages_section.ascii_scouts)

        # triggers
        trigger_manager = self.scenario.trigger_manager

        for trigger in trigger_manager.triggers:
            if trigger.display_as_objective:
                if trigger.description != "":
                    trigger_text_long = TriggerItem(ti.TYPE_OBJECTIVE_LONG, trigger.name, trigger.description,
                                                    trigger_manager.triggers.index(trigger), NO_EFFECT)
                    self.content_triggers.append(trigger_text_long)

                if trigger.short_description != "":
                    trigger_text_short = TriggerItem(ti.TYPE_OBJECTIVE_SHORT, trigger.name, trigger.short_description,
                                                     trigger_manager.triggers.index(trigger), NO_EFFECT)
                    self.content_triggers.append(trigger_text_short)

            else:
                for effect in trigger.effects:
                    if effect.effect_type != EFFECT_56 and effect.effect_type != EFFECT_91 and effect.message != "":
                        effect_message = TriggerItem(ti.TYPE_EFFECT_MESSAGE, trigger.name, effect.message,
                                                     trigger_manager.triggers.index(trigger),
                                                     trigger.effects.index(effect))
                        self.content_triggers.append(effect_message)

    def _load_content_into_ui(self):
        for player_index in range(0, 8):
            self.player_entries[player_index].delete(0, "end")
            self.player_entries[player_index].insert(0, self.content_players[player_index])

        self.combobox_message.current(0)
        self.textfield_message.delete(1.0, "end")
        self.textfield_message.insert(1.0, self.content_messages[0])

        for trigger_item in self.content_triggers:
            self.listbox_triggers.insert(1, trigger_item.name)
