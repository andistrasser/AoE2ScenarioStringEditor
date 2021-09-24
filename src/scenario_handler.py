from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


class ScenarioHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.scenario = None

    def load_scenario(self):
        self.scenario = AoE2DEScenario.from_file(self.file_path)

    def get_section(self, section):
        return self.scenario.sections[section]

    def get_triggers(self):
        return self.scenario.trigger_manager.triggers

    def save_scenario(self, file_path):
        self.scenario.write_to_file(file_path)

    def is_scenario_loaded(self):
        return self.scenario is not None
