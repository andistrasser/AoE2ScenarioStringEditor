from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


class ScenarioHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_scenario(self):
        return AoE2DEScenario.from_file(self.file_path)
