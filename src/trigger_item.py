# constants
TYPE_OBJECTIVE_LONG = 0
TYPE_OBJECTIVE_SHORT = 1
TYPE_EFFECT_MESSAGE = 2
NO_EFFECT = -1


class TriggerItem:
    def __init__(self, item_type, name, text, trigg_index, effect_index):
        self.item_type = item_type
        self.name = name
        self.text = text
        self.trigger_index = trigg_index
        self.effect_index = effect_index
