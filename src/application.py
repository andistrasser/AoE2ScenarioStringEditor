import os
from tkinter.filedialog import askopenfilename

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
STATUS_LOADING = "loading "
STATUS_LOADING_SUCCESSFUL = " loaded successfully"
STATUS_LOADING_FAILED = " could not be loaded"
FILETYPES = [("AoE2DE scenario file", "*.aoe2scenario")]


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
        self.scenario_loaded = False
        self.ui = UserInterface()
        self.ui.status.set(STATUS_NO_SCENARIO_LOADED)
        self.last_message_index = 0
        self.last_trigger_index = 0
        self.content = Content()

    def _bind_functions(self):
        self.ui.menu_file.entryconfig(ui.MENU_OPEN, command=self._open_file)
        self.ui.menu_file.entryconfig(ui.MENU_RELOAD, command=self._reload_content)
        self.ui.combobox_message.bind("<<ComboboxSelected>>", self._message_selected)
        self.ui.listbox_triggers.bind("<<ListboxSelect>>", self._trigger_selected)
        self.ui.button_apply.config(command=self._button_apply_clicked)

    def _open_file(self):
        self.file_path = askopenfilename(filetypes=FILETYPES)

        if len(self.file_path) == 0:
            return

        self.scenario_handler = ScenarioHandler(self.file_path)

        file_name = os.path.basename(self.file_path)

        try:
            self.ui.set_status(STATUS_LOADING + file_name)
            self.scenario = self.scenario_handler.load_scenario()
            self.content.clear()
            self._load_content()
            self.ui.lock(False)
            self._display_content()
            self.scenario_loaded = True
            self.ui.set_status(file_name + STATUS_LOADING_SUCCESSFUL)
        except:
            self.ui.set_status(file_name + STATUS_LOADING_FAILED)

    def _load_content(self):
        # data header section
        data_header_section = self.scenario.sections["DataHeader"]

        self.content.internal_file_name = data_header_section.filename

        for index in range(0, 8):
            player_name = str(data_header_section.player_names[index])

            self.content.add_item_to_section("Players", player_name.replace("\x00", ""))

        # messages section
        messages_section = self.scenario.sections["Messages"]

        self.content.add_item_to_section("Messages", messages_section.ascii_instructions)
        self.content.add_item_to_section("Messages", messages_section.ascii_hints)
        self.content.add_item_to_section("Messages", messages_section.ascii_victory)
        self.content.add_item_to_section("Messages", messages_section.ascii_loss)
        self.content.add_item_to_section("Messages", messages_section.ascii_history)
        self.content.add_item_to_section("Messages", messages_section.ascii_scouts)

        # triggers
        trigger_manager = self.scenario.trigger_manager

        for trigger in trigger_manager.triggers:
            if trigger.display_as_objective:
                if trigger.description != "":
                    trigger_text_long = TriggerItem(ti.TYPE_OBJECTIVE_LONG, trigger.name, trigger.description,
                                                    trigger_manager.triggers.index(trigger), ti.NO_EFFECT)
                    self.content.add_item_to_section("Triggers", trigger_text_long)

                if trigger.short_description != "":
                    trigger_text_short = TriggerItem(ti.TYPE_OBJECTIVE_SHORT, trigger.name, trigger.short_description,
                                                     trigger_manager.triggers.index(trigger), ti.NO_EFFECT)
                    self.content.add_item_to_section("Triggers", trigger_text_short)

            else:
                for effect in trigger.effects:
                    if effect.effect_type != EFFECT_56 and effect.effect_type != EFFECT_91 and effect.message != "":
                        effect_message = TriggerItem(ti.TYPE_EFFECT_MESSAGE, trigger.name, effect.message,
                                                     trigger_manager.triggers.index(trigger),
                                                     trigger.effects.index(effect))
                        self.content.add_item_to_section("Triggers", effect_message)

        # raw
        self.content.create_raw_content()

    def _display_content(self):
        self.ui.entry_scenario_name.delete(0, "end")
        self.ui.entry_scenario_name.insert(0, self.content.internal_file_name)

        for player_index in range(0, 8):
            self.ui.player_entries[player_index].delete(0, "end")
            self.ui.player_entries[player_index].insert(0, self.content.get("Players")[player_index])

        ui.set_textfield_text(self.ui.textfield_message, self.content.get("Messages")[self.last_message_index])

        self.ui.listbox_triggers.delete(0, "end")

        for trigger_item in self.content.get("Triggers"):
            if trigger_item.effect_index != ti.NO_EFFECT:
                self.ui.listbox_triggers.insert("end", trigger_item.name + " - E#" + str(trigger_item.effect_index))
            else:
                self.ui.listbox_triggers.insert("end", trigger_item.name)

        ui.set_textfield_text(self.ui.textfield_triggers, self.content.get("Triggers")[self.last_trigger_index].text)
        ui.set_textfield_text(self.ui.textfield_raw, self.content.get("Raw"))

    def _reload_content(self):
        if self.scenario_loaded:
            self.content.clear()
            self._load_content()
            self._display_content()

    def _message_selected(self, event):
        if self.scenario_loaded:
            self.content.get("Messages")[self.last_message_index] = self.ui.textfield_message.get(1.0, "end")
            self.last_message_index = self.ui.combobox_message.current()

            ui.set_textfield_text(self.ui.textfield_message, self.content.get("Messages")[self.last_message_index])
        else:
            self.last_message_index = self.ui.combobox_message.current()

    def _trigger_selected(self, event):
        curselection = self.ui.listbox_triggers.curselection()

        if self.scenario_loaded and len(self.content.get("Triggers")) > 0 and len(curselection) > 0:
            self.content.get("Triggers")[self.last_trigger_index].text = self.ui.textfield_triggers.get(1.0, "end")
            self.last_trigger_index = self.ui.listbox_triggers.curselection()[0]

            ui.set_textfield_text(self.ui.textfield_triggers,
                                  self.content.get("Triggers")[self.last_trigger_index].text)

    def _button_apply_clicked(self):
        self.content.apply_raw_content(self.ui.textfield_raw.get(1.0, "end"))
        self._display_content()
