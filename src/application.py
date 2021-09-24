import os
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
STATUS_INVALID_FILE_NAME = "invalid file name "
FILETYPES = [("AoE2DE scenario file", "*.aoe2scenario")]
SCENARIO_FILE_EXTENSION = ".aoe2scenario"


# application class
class App:
    def __init__(self):
        self._init()
        self._bind_functions()
        self.ui.lock(True)
        self.ui.mainloop()

    # build user interface, initialize variables
    def _init(self):
        self.file = ""
        self.ui = UserInterface()
        self.ui.status.set(STATUS_NO_SCENARIO_LOADED)
        self.last_message_index = 0
        self.last_trigger_index = 0
        self.content = Content()

    def _bind_functions(self):
        self.ui.menu_file.entryconfig(ui.MENU_OPEN, command=self._open_file)
        self.ui.menu_file.entryconfig(ui.MENU_RELOAD, command=self._reload_content)
        self.ui.menu_file.entryconfig(ui.MENU_SAVE, command=lambda: self._save(False))
        self.ui.menu_file.entryconfig(ui.MENU_SAVE_AS, command=lambda: self._save(True))
        self.ui.entry_file_name.bind("<FocusOut>", self._entry_file_name_focus_lost)
        self.ui.combobox_message.bind("<<ComboboxSelected>>", self._message_selected)
        self.ui.listbox_triggers.bind("<<ListboxSelect>>", self._trigger_selected)
        self.ui.button_apply.config(command=self._button_apply_clicked)

    def _open_file(self):
        self.file_path = askopenfilename(filetypes=FILETYPES)

        if len(self.file_path) == 0:
            return

        self.scenario_handler = ScenarioHandler(self.file_path)

        file_name = os.path.basename(self.file_path)

        self.ui.lock(True)

        try:
            self.ui.set_status(STATUS_READING + file_name)
            self.scenario_handler.load_scenario()
            self.content.clear()
            self._load_content()
            self.ui.set_status(file_name + STATUS_READING_SUCCESSFUL)
        except Exception as ex:
            self.ui.show_error_dialog(ex)
            self.ui.set_status(file_name + STATUS_READING_FAILED)

        if self.scenario_handler.is_scenario_loaded():
            self.ui.lock(False)
            self._display_content()

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

        # raw
        self.content.create_raw_content()

    def _display_content(self):
        self.ui.entry_file_name.delete(0, "end")
        self.ui.entry_file_name.insert(0, self.content.internal_file_name.replace(SCENARIO_FILE_EXTENSION, ""))

        for index in range(0, 8):
            self.ui.player_entries[index].delete(0, "end")
            self.ui.player_entries[index].insert(0, self.content.get("Players")[index])

        self.ui.set_textfield_text(self.ui.textfield_message, self.content.get("Messages")[self.last_message_index])

        self.ui.listbox_triggers.delete(0, "end")

        for trigger_item in self.content.get("Triggers"):
            if trigger_item.effect_index != ti.NO_EFFECT:
                self.ui.listbox_triggers.insert("end", trigger_item.name + " - E#" + str(trigger_item.effect_index))
            else:
                self.ui.listbox_triggers.insert("end", trigger_item.name)

        self.ui.set_textfield_text(self.ui.textfield_triggers,
                                   self.content.get("Triggers")[self.last_trigger_index].text)
        self.ui.set_textfield_text(self.ui.textfield_raw, self.content.get("Raw"))

    def _reload_content(self):
        self.content.clear()
        self._load_content()
        self._display_content()

    def _prepare_save(self):
        self.content.internal_file_name = self.ui.entry_file_name.get() + SCENARIO_FILE_EXTENSION

        for player_index in range(0, len(self.ui.player_entries)):
            player_name = self.ui.player_entries[player_index].get()

            for char_index in range(0, 256):
                if char_index >= len(player_name):
                    player_name += "\x00"

            self.content.get("Players")[player_index] = player_name

        self.content.get("Messages")[self.last_message_index] = self.ui.textfield_message.get(1.0, "end")
        self.content.get("Triggers")[self.last_trigger_index].text = self.ui.textfield_triggers.get(1.0, "end")

    def _save_content(self):
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

    def _save(self, save_as):
        self._prepare_save()
        self._save_content()

        if save_as:
            self.file_path = asksaveasfilename(filetypes=FILETYPES)

            if len(self.file_path) == 0:
                return
            elif SCENARIO_FILE_EXTENSION not in self.file_path:
                self.ui.set_status(STATUS_INVALID_FILE_NAME + os.path.basename(self.file_path))

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

    def _entry_file_name_focus_lost(self, _event):
        self.content.internal_file_name = self.ui.entry_file_name.get() + SCENARIO_FILE_EXTENSION

    def _message_selected(self, _event):
        self.content.get("Messages")[self.last_message_index] = self.ui.textfield_message.get(1.0, "end")
        self.last_message_index = self.ui.combobox_message.current()

        self.ui.set_textfield_text(self.ui.textfield_message, self.content.get("Messages")[self.last_message_index])

    def _trigger_selected(self, _event):
        curselection = self.ui.listbox_triggers.curselection()

        if len(self.content.get("Triggers")) > 0 and len(curselection) > 0:
            self.content.get("Triggers")[self.last_trigger_index].text = self.ui.textfield_triggers.get(1.0, "end")
            self.last_trigger_index = self.ui.listbox_triggers.curselection()[0]

            self.ui.set_textfield_text(self.ui.textfield_triggers,
                                       self.content.get("Triggers")[self.last_trigger_index].text)

    def _button_apply_clicked(self):
        self.content.apply_raw_content(self.ui.textfield_raw.get(1.0, "end"))
        self._display_content()
