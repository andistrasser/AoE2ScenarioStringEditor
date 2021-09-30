import os
import webbrowser
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

import trigger_item as ti
import user_interface as ui
from content import Content
from scenario_handler import ScenarioHandler
from trigger_item import TriggerItem
from user_interface import UserInterface

# constants
EFFECT_56 = 56
EFFECT_91 = 91
STATUS_NO_SCENARIO_LOADED = "no scenario file loaded at the moment"
STATUS_READING = "reading "
STATUS_READING_SUCCESSFUL = " read successfully"
STATUS_READING_FAILED = " could not be read"
STATUS_WRITING = "writing "
STATUS_WRITING_SUCCESSFUL = " written successfully"
STATUS_WRITING_FAILED = " could not be written"
FILETYPES = [("AoE2DE scenario file", "*.aoe2scenario")]
SCENARIO_FILE_EXTENSION = ".aoe2scenario"
HELP_GITHUB_DOC = "https://github.com/andistrasser/AoE2ScenarioStringEditor/blob/dev/docs/DOC.md"
ABOUT_TITLE = "About"
ABOUT_MESSAGE = "Autor: andistrasser\nGithub: https://github.com/andistrasser"


# application class
class App:
    def __init__(self):
        self._init()
        self._bind_functions()
        self.ui.lock(True)
        self.ui.mainloop()

    # builds user interface, initializes variables
    def _init(self):
        self.file = ""
        self.ui = UserInterface()
        self.ui.status.set(STATUS_NO_SCENARIO_LOADED)
        self.scenario_handler = None
        self.last_message_index = 0
        self.last_trigger_index = 0
        self.content = Content()

    # binds functions to the ui widgets
    def _bind_functions(self):
        # menu event bindings
        self.ui.menu_file.entryconfig(ui.MENU_OPEN, command=self._open_file)
        self.ui.menu_file.entryconfig(ui.MENU_RELOAD, command=self._reload_content)
        self.ui.menu_file.entryconfig(ui.MENU_SAVE, command=lambda: self._save(False))
        self.ui.menu_file.entryconfig(ui.MENU_SAVE_AS, command=lambda: self._save(True))
        self.ui.menu_help.entryconfig(ui.MENU_HELP, command=self._help)
        self.ui.menu_help.entryconfig(ui.MENU_ABOUT, command=self._about)

        # widget event bindings
        self.ui.entry_file_name.bind("<FocusOut>", self._entry_file_name_focus_lost)
        self.ui.combobox_message.bind("<<ComboboxSelected>>", self._message_selected)
        self.ui.listbox_triggers.bind("<<ListboxSelect>>", self._trigger_selected)
        self.ui.button_apply.config(command=self._button_apply_clicked)

        # keyboard shortcuts
        self.ui.bind("<F1>", self._help)
        self.ui.bind("<Control-o>", self._open_file)
        self.ui.bind("<Control-r>", self._reload_content)
        self.ui.bind("<Control-s>", lambda save_as: self._save(False))
        self.ui.bind("<Control-Alt-s>", lambda save_as: self._save(True))
        self.ui.bind("<Control-q>", self.ui.exit)

    # opens the file for further reading actions
    def _open_file(self, _event=None):
        self.file_path = askopenfilename(filetypes=FILETYPES)

        if len(self.file_path) == 0:
            return

        self.scenario_handler = ScenarioHandler()

        file_name = os.path.basename(self.file_path)

        self.ui.lock(True)

        try:
            self.ui.set_status(STATUS_READING + file_name)
            self.scenario_handler.load_scenario(self.file_path)
            self.content.clear()
            self._load_content()
            self.ui.set_status(file_name + STATUS_READING_SUCCESSFUL)
        except Exception as ex:
            self.ui.show_error_dialog(ex)
            self.ui.set_status(file_name + STATUS_READING_FAILED)

        if self.scenario_handler.is_scenario_loaded():
            self.ui.lock(False)
            self._display_content()

    # reads all kinds of strings from the scenario file and loads them into the content container
    def _load_content(self):
        # data header section
        data_header_section = self.scenario_handler.get_section("DataHeader")

        self.content.internal_file_name = data_header_section.filename

        for index in range(0, 8):
            player_name = data_header_section.player_names[index]

            self.content.add_item_to_section("Players", player_name.replace("\x00", ""))

        # messages section
        messages_section = self.scenario_handler.get_section("Messages")

        self.content.add_item_to_section("Messages", messages_section.ascii_instructions)
        self.content.add_item_to_section("Messages", messages_section.ascii_hints)
        self.content.add_item_to_section("Messages", messages_section.ascii_victory)
        self.content.add_item_to_section("Messages", messages_section.ascii_loss)
        self.content.add_item_to_section("Messages", messages_section.ascii_history)
        self.content.add_item_to_section("Messages", messages_section.ascii_scouts)

        # triggers
        triggers = self.scenario_handler.get_triggers()

        for trigger in triggers:
            if trigger.display_as_objective:
                if trigger.description != "":
                    trigger_text_long = TriggerItem(ti.TYPE_OBJECTIVE_LONG, trigger.name, trigger.description,
                                                    triggers.index(trigger), ti.NO_EFFECT)
                    self.content.add_item_to_section("Triggers", trigger_text_long)

                if trigger.short_description != "":
                    trigger_text_short = TriggerItem(ti.TYPE_OBJECTIVE_SHORT, trigger.name, trigger.short_description,
                                                     triggers.index(trigger), ti.NO_EFFECT)
                    self.content.add_item_to_section("Triggers", trigger_text_short)

            else:
                for effect in trigger.effects:
                    if effect.effect_type != EFFECT_56 and effect.effect_type != EFFECT_91 and effect.message != "":
                        effect_message = TriggerItem(ti.TYPE_EFFECT_MESSAGE, trigger.name, effect.message,
                                                     triggers.index(trigger), trigger.effects.index(effect))
                        self.content.add_item_to_section("Triggers", effect_message)

        # clean line feed
        self.content.clean_linefeed()

        # raw
        self.content.create_raw_content()

    # loads the content into the ui widgets
    def _display_content(self):
        self.ui.entry_file_name.delete(0, "end")
        self.ui.entry_file_name.insert(0, self.content.internal_file_name.replace(SCENARIO_FILE_EXTENSION, ""))

        for index in range(0, 8):
            self.ui.player_entries[index].delete(0, "end")
            self.ui.player_entries[index].insert(0, self.content.get("Players")[index])

        self.ui.set_textfield_text(self.ui.textfield_message, self.content.get("Messages")[self.last_message_index])

        self.ui.listbox_triggers.delete(0, "end")

        for trigger_item in self.content.get("Triggers"):
            if trigger_item.type == ti.TYPE_EFFECT_MESSAGE:
                self.ui.listbox_triggers.insert("end",
                                                trigger_item.name + " - [E#" + str(trigger_item.effect_index) + "]")
            elif trigger_item.type == ti.TYPE_OBJECTIVE_LONG:
                self.ui.listbox_triggers.insert("end", trigger_item.name + " - [Obj. long]")
            else:
                self.ui.listbox_triggers.insert("end", trigger_item.name + " - [Obj. short]")

        self.ui.set_textfield_text(self.ui.textfield_triggers,
                                   self.content.get("Triggers")[self.last_trigger_index].text)
        self.ui.set_textfield_text(self.ui.textfield_raw, self.content.get("Raw"))

    # reloads the content from the scenario file
    def _reload_content(self, _event=None):
        if self.scenario_handler is not None and self.scenario_handler.is_scenario_loaded():
            self.content.clear()
            self._load_content()
            self._display_content()

    # reads all the strings from the ui widgets and writes them into the content container
    def _prepare_write(self):
        self.content.internal_file_name = self.ui.entry_file_name.get() + SCENARIO_FILE_EXTENSION

        for player_index in range(0, len(self.ui.player_entries)):
            player_name = self.ui.player_entries[player_index].get()

            for char_index in range(0, 256):
                if char_index >= len(player_name.encode("utf-8")):
                    player_name += "\x00"

            self.content.get("Players")[player_index] = player_name

        self.content.get("Messages")[self.last_message_index] = self.ui.textfield_message.get(1.0, "end-1c")
        self.content.get("Triggers")[self.last_trigger_index].text = self.ui.textfield_triggers.get(1.0, "end-1c")

    # writes the content to the scenario file
    def _write_content_to_scenario(self):
        # data header section
        data_header_section = self.scenario_handler.get_section("DataHeader")

        data_header_section.filename = self.content.internal_file_name

        for index in range(0, 8):
            data_header_section.player_names[index] = self.content.get("Players")[index]

        # messages section
        messages_section = self.scenario_handler.get_section("Messages")

        messages_section.ascii_instructions = self.content.get("Messages")[0]
        messages_section.ascii_hints = self.content.get("Messages")[1]
        messages_section.ascii_victory = self.content.get("Messages")[2]
        messages_section.ascii_loss = self.content.get("Messages")[3]
        messages_section.ascii_history = self.content.get("Messages")[4]
        messages_section.ascii_scouts = self.content.get("Messages")[5]

        # triggers
        triggers = self.scenario_handler.get_triggers()

        for item in self.content.get("Triggers"):
            if item.type == ti.TYPE_OBJECTIVE_LONG:
                triggers[item.trigger_index].description = item.text
            elif item.type == ti.TYPE_OBJECTIVE_SHORT:
                triggers[item.trigger_index].short_description = item.text
            elif item.type == ti.TYPE_EFFECT_MESSAGE:
                triggers[item.trigger_index].effects[item.effect_index].message = item.text

    # writes the scenario file to the file system
    def _save(self, save_as, _event=None):
        if self.scenario_handler is not None and self.scenario_handler.is_scenario_loaded():
            self._prepare_write()
            self._write_content_to_scenario()

            if save_as:
                self.file_path = asksaveasfilename(filetypes=FILETYPES)
                print(os.path.splitext(self.file_path)[1])

                if len(self.file_path) == 0:
                    return

                extension = os.path.splitext(self.file_path)[1]

                if extension == "" or extension != SCENARIO_FILE_EXTENSION:
                    self.file_path += SCENARIO_FILE_EXTENSION

            file_name = os.path.basename(self.file_path)

            self.ui.lock(True)

            try:
                self.ui.set_status(STATUS_WRITING + file_name)
                self.scenario_handler.save_scenario(self.file_path)
                self.ui.set_status(file_name + STATUS_WRITING_SUCCESSFUL)
            except Exception as ex:
                self.ui.show_error_dialog(ex)
                self.ui.set_status(file_name + STATUS_WRITING_FAILED)

            self.ui.lock(False)

    # opens the github doc page
    @staticmethod
    def _help(_event=None):
        webbrowser.open(HELP_GITHUB_DOC)

    def _about(self):
        self.ui.show_info_dialog(ABOUT_TITLE, ABOUT_MESSAGE)

    # gets called when the focus on the internal file name entry has been lost
    def _entry_file_name_focus_lost(self, _event):
        self.content.internal_file_name = self.ui.entry_file_name.get() + SCENARIO_FILE_EXTENSION

    # gets called when a message combobox item has been selected
    def _message_selected(self, _event):
        self.content.get("Messages")[self.last_message_index] = self.ui.textfield_message.get(1.0, "end-1c")
        self.last_message_index = self.ui.combobox_message.current()

        self.ui.set_textfield_text(self.ui.textfield_message, self.content.get("Messages")[self.last_message_index])

    # gets called when a trigger has been selected
    def _trigger_selected(self, _event):
        curselection = self.ui.listbox_triggers.curselection()

        if len(self.content.get("Triggers")) > 0 and len(curselection) > 0:
            self.content.get("Triggers")[self.last_trigger_index].text = self.ui.textfield_triggers.get(1.0, "end-1c")
            self.last_trigger_index = self.ui.listbox_triggers.curselection()[0]

            self.ui.set_textfield_text(self.ui.textfield_triggers,
                                       self.content.get("Triggers")[self.last_trigger_index].text)

    # gets called when the apply button has been clicked
    def _button_apply_clicked(self):
        self.content.apply_raw_content(self.ui.textfield_raw.get(1.0, "end-1c"))
        self._display_content()
