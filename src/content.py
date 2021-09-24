# constants
WRITEABLE_SECTIONS = ["Players", "Messages", "Triggers"]
READABLE_SECTIONS = ["Players", "Messages", "Triggers", "Raw"]


class Content:
    def __init__(self):
        self.internal_file_name = ""
        self._content = {"Players": [], "Messages": [], "Triggers": [], "Raw": ""}

    def clear(self):
        self.internal_file_name = ""
        self._content["Players"].clear()
        self._content["Messages"].clear()
        self._content["Triggers"].clear()
        self._content["Raw"] = ""

    def add_item_to_section(self, section, item):
        if section in WRITEABLE_SECTIONS:
            self._content[section].append(item)

    def create_raw_content(self):
        for player in self._content["Players"]:
            self._content["Raw"] += (player + "\n")

        for message in self._content["Messages"]:
            self._content["Raw"] += (self._one_line(message) + "\n")

        for trigger in self._content["Triggers"]:
            self._content["Raw"] += (self._one_line(trigger.text) + "\n")

    @staticmethod
    def _one_line(string):
        return string.replace("\n", "\\n")

    @staticmethod
    def _multi_line(string):
        return string.replace("\\n", "\n")

    def apply_raw_content(self, raw_content):
        self._content["Raw"] = raw_content
        raw_lines = []
        start_index = 0

        for index in range(0, len(raw_content)):
            if raw_content[index] == "\n":
                raw_lines.append(raw_content[start_index:index])
                start_index = (index + 1)

        length_players = len(self._content["Players"])
        length_messages = len(self._content["Messages"])
        length_triggers = len(self._content["Triggers"])

        self._content["Players"].clear()
        self._content["Messages"].clear()

        for index in range(0, len(raw_lines)):
            if index >= (length_players + length_messages + length_triggers):
                break
            elif index < length_players:
                self._content["Players"].append(raw_lines[index])
            elif index < (length_players + length_messages):
                self._content["Messages"].append(self._multi_line(raw_lines[index]))
            else:
                self._content["Triggers"][index - length_players - length_messages].text = self._multi_line(
                    raw_lines[index])

    def get(self, section):
        if section in READABLE_SECTIONS:
            return self._content[section]
        else:
            return None
