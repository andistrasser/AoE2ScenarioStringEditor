# constants
WRITEABLE_SECTIONS = ["Players", "Messages", "Triggers"]
READABLE_SECTIONS = ["Players", "Messages", "Triggers", "Raw"]


# content class
class Content:
    def __init__(self):
        self.internal_file_name = ""
        self._content = {"Players": [], "Messages": [], "Triggers": [], "Raw": ""}

    # clears the content container
    def clear(self):
        self.internal_file_name = ""
        self._content["Players"].clear()
        self._content["Messages"].clear()
        self._content["Triggers"].clear()
        self._content["Raw"] = ""

    # adds an item to a given section
    def add_item_to_section(self, section, item):
        if section in WRITEABLE_SECTIONS:
            self._content[section].append(item)

    # creates the raw content where each item of the content container consists of one line
    def create_raw_content(self):
        for player in self._content["Players"]:
            self._content["Raw"] += (player + "\n")

        for message in self._content["Messages"]:
            self._content["Raw"] += (self._one_line(message) + "\n")

        for trigger in self._content["Triggers"]:
            self._content["Raw"] += (self._one_line(trigger.text) + "\n")

    # replaces the invisible new line character with \n
    @staticmethod
    def _one_line(string):
        return string.replace("\n", "\\n")

    # replaces \n with the invisible new line character
    @staticmethod
    def _multi_line(string):
        return string.replace("\\n", "\n")

    # fills the content container with the content of the raw section
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

    # returns the given section
    def get(self, section):
        if section in READABLE_SECTIONS:
            return self._content[section]
        else:
            return None
