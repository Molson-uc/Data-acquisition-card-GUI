import json


exampleFactors = {"WheelSpeedFactor": 2.0,
                  "SuspensionFactor": 1.0, "TemperatureFactor": 1.0}

# with open("data/settings.json", "r+") as file:
# json.dump(exampleFactors, file)


class FileManager():
    def __init__(self, fileTrack):
        self.fileTrack = fileTrack

    def save_setting_file(self, settings):
        try:
            with open(self.fileTrack, "r+", encoding="UTF-8") as file:
                json.dump(settings, file)
        except TypeError:
            print("only string")
        except json.decoder.JSONDecodeError:
            print("wrong file format")

    def change_setting_factor(self, key, factor):
        with open(self.fileTrack, "r+", encoding="UTF-8") as file:
            try:

                settings = json.load(file)
                settings[key] = factor
                file.seek(0)
                print(settings)
                json.dump(settings, file)
                file.truncate()
            except (ValueError, TypeError):
                print("wrong type")

    def load_setting_factor(self, key):
        with open(self.fileTrack, "r+", encoding="UTF-8") as file:
            settings = json.load(file)
            return settings[key]

    def load_setting_file(self):
        try:
            with open(self.fileTrack, encoding="UTF-8") as file:
                return json.load(file)
        except TypeError:
            print("only string")
            return 0

    def get_settings_keys(self):
        settings = self.load_setting_file()
        return settings.keys()

    def get_settings_factor(self, key):
        settings = self.load_setting_file()
        return settings.get(key)

    def get_all_factors(self):
        settings = self.load_setting_file()
        factorList = []
        for settingNumber in settings:
            factorList.append(round(float(settings[settingNumber]), 3))
        return factorList


fm = FileManager(
    "C:\\programing\\workspace\\workspacePython\\Data\\settings.json")
fm.change_setting_factor("WheelSpeedFactor", 5.0)
print(fm.get_all_factors())
