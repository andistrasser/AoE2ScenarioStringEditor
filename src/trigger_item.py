# constants
TYPE_OBJECTIVE_LONG = 0
TYPE_OBJECTIVE_SHORT = 1
TYPE_EFFECT_MESSAGE = 2
NO_EFFECT = -1


# trigger item class
class TriggerItem:
    def __init__(self, item_type, name, text, trigger_index, effect_index):
        self.type = item_type
        self.name = name
        self.text = text
        self.trigger_index = trigger_index
        self.effect_index = effect_index
