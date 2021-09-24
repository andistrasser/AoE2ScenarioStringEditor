from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


# scenario handler class
class ScenarioHandler:
    def __init__(self):
        self.scenario = None

    # loads the scenario from the given file path
    def load_scenario(self, file_path):
        self.scenario = AoE2DEScenario.from_file(file_path)

    # gets the given data section
    def get_section(self, section):
        return self.scenario.sections[section]

    # gets the triggers of the scenario
    def get_triggers(self):
        return self.scenario.trigger_manager.triggers

    # save the scenario to the file system
    def save_scenario(self, file_path):
        self.scenario.write_to_file(file_path)

    # retunrs True if a scenario is loaded, else False
    def is_scenario_loaded(self):
        return self.scenario is not None
