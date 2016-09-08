class Calculator:
    def __init__(self, data: DataCollector):
        self.current_xp = data.char_levels[0]
        self.goal_xp = data.char_levels[1]
        self.needed_xp = self.calculate_needed_xp()
        self.current_skill_levels = data.skill_levels

    def calculate_needed_xp(self):
        a = 12.5 * (self.goal_xp ** 2 - self.current_xp ** 2)
        b = 62.5 * (self.goal_xp - self.current_xp)
        return a + b

    def get_fastest_results(self):
        still_needed = self.needed_xp
        end_levels = self.current_skill_levels.copy()
        times_legendary = {}
        for skill in end_levels:
            times_legendary[skill] = 0

        while still_needed > 0:
            selected = max(end_levels, key=lambda key: end_levels[key])
            training_result = self.train_skill(end_levels[selected])
            end_levels[selected] = training_result
            if training_result == 15:
                times_legendary[selected] += 1
                still_needed -= 100
            else:
                still_needed -= training_result
        return self.reformat_results(end_levels, times_legendary)

    def get_easiest_results(self):
        still_needed = self.needed_xp
        end_levels = self.current_skill_levels.copy()
        times_legendary = {}
        for skill in end_levels:
            times_legendary[skill] = 0

        while still_needed > 0:
            selected = min(end_levels, key=lambda key: end_levels[key])
            training_result = self.train_skill(end_levels[selected])
            end_levels[selected] = training_result
            if training_result == 15:
                times_legendary[selected] += 1
                still_needed -= 100
            else:
                still_needed -= training_result
        return self.reformat_results(end_levels, times_legendary)

    def get_balanced_results(self):
        still_needed = self.needed_xp
        end_levels = self.current_skill_levels.copy()
        times_legendary = {}
        for skill in end_levels:
            times_legendary[skill] = 0

        over = False
        while not over:
            for skill in end_levels:
                training_result = self.train_skill(end_levels[skill])
                end_levels[skill] = training_result
                if training_result == 15:
                    times_legendary[skill] += 1
                    still_needed -= 100
                else:
                    still_needed -= training_result
                over = still_needed <= 0
                if over:
                    break
        return self.reformat_results(end_levels, times_legendary)

    def train_skill(self, level):
        level += 1
        if level == 100:
            level = 15
        return level

    def reformat_results(self, end_levels, times_legendary):
        results = {}
        for skill in end_levels:
            results[skill] = {"start": self.current_skill_levels[skill],
                              "end": end_levels[skill],
                              "legendary": times_legendary[skill]
                              }
        return results


class DataCollector:
    def __init__(self):
        self.__goal = ""
        self.__now = ""
        self.__race = ""
        self.__selected_skills = []
        self.__skill_levels = {}

    def set_race(self, race):
        if InputValidator.is_valid_race(race):
            self.__race = race
        else:
            raise ValidationException("Please select a race.")

    def set_char_levels(self, goal, now=1):
        valid_goal = InputValidator.is_valid_level(goal)
        valid_now = now == 1 or InputValidator.is_valid_level(now)

        if valid_goal and valid_now:
            if InputValidator.is_valid_level_combination(goal=goal, now=now):
                self.__goal = goal
                self.__now = now
            else:
                raise ValidationException(
                    "Your goal level must be higher than your current level.",
                    ["goal", "now"])
        elif valid_goal:
            raise ValidationException("Please enter a valid goal level.",
                                      "now")
        elif valid_now:
            raise ValidationException("Please enter a valid character level.",
                                      "goal")
        else:
            raise ValidationException("Please enter valid levels.",
                                      ["goal", "now"])

    def set_selected_skills(self, skills):
        if InputValidator.is_valid_selection(skills):
            if InputValidator.are_valid_skills(skills):
                self.__selected_skills = skills
            else:
                raise ValidationException("Those skills are invalid.")
        else:
            raise ValidationException("You need to select at least one skill.")

    def set_skill_levels(self, skill_levels):  # TODO

        self.__skill_levels = skill_levels

    # old

    def generate_selected_skill_levels(self):
        skill_info = self.get_race_skills_info()[self.race]
        self.skill_levels = {}
        for skill in self.selected_skills:
            self.skill_levels[skill] = skill_info[skill]

    @staticmethod
    def get_race_skills_info():
        return {
            "Breton": {
                "Illusion": 20,
                "Conjuration": 25,
                "Destruction": 15,
                "Restoration": 20,
                "Alteration": 20,
                "Enchanting": 15,
                "Smithing": 15,
                "Heavy Armor": 15,
                "Block": 15,
                "Two-handed": 15,
                "One-handed": 15,
                "Archery": 15,
                "Light Armor": 15,
                "Sneak": 15,
                "Lockpicking": 15,
                "Pickpocket": 15,
                "Speech": 20,
                "Alchemy": 20,
            },
            "Nord": {
                "Illusion": 15,
                "Conjuration": 15,
                "Destruction": 15,
                "Restoration": 15,
                "Alteration": 15,
                "Enchanting": 15,
                "Smithing": 20,
                "Heavy Armor": 15,
                "Block": 20,
                "Two-handed": 25,
                "One-handed": 20,
                "Archery": 15,
                "Light Armor": 20,
                "Sneak": 15,
                "Lockpicking": 15,
                "Pickpocket": 15,
                "Speech": 20,
                "Alchemy": 15,
            },
            "Imperial": {
                "Illusion": 15,
                "Conjuration": 15,
                "Destruction": 20,
                "Restoration": 25,
                "Alteration": 15,
                "Enchanting": 20,
                "Smithing": 15,
                "Heavy Armor": 20,
                "Block": 20,
                "Two-handed": 15,
                "One-handed": 20,
                "Archery": 15,
                "Light Armor": 15,
                "Sneak": 15,
                "Lockpicking": 15,
                "Pickpocket": 15,
                "Speech": 15,
                "Alchemy": 15,
            },
            "Redguard": {
                "Illusion": 15,
                "Conjuration": 15,
                "Destruction": 20,
                "Restoration": 15,
                "Alteration": 20,
                "Enchanting": 15,
                "Smithing": 20,
                "Heavy Armor": 15,
                "Block": 20,
                "Two-handed": 15,
                "One-handed": 25,
                "Archery": 20,
                "Light Armor": 15,
                "Sneak": 15,
                "Lockpicking": 15,
                "Pickpocket": 15,
                "Speech": 15,
                "Alchemy": 15,
            },
            "Altmer": {
                "Illusion": 25,
                "Conjuration": 20,
                "Destruction": 20,
                "Restoration": 20,
                "Alteration": 20,
                "Enchanting": 20,
                "Smithing": 15,
                "Heavy Armor": 15,
                "Block": 15,
                "Two-handed": 15,
                "One-handed": 15,
                "Archery": 15,
                "Light Armor": 15,
                "Sneak": 15,
                "Lockpicking": 15,
                "Pickpocket": 15,
                "Speech": 15,
                "Alchemy": 15,
            },
            "Bosmer": {
                "Illusion": 15,
                "Conjuration": 15,
                "Destruction": 15,
                "Restoration": 15,
                "Alteration": 15,
                "Enchanting": 15,
                "Smithing": 15,
                "Heavy Armor": 15,
                "Block": 15,
                "Two-handed": 15,
                "One-handed": 15,
                "Archery": 25,
                "Light Armor": 20,
                "Sneak": 20,
                "Lockpicking": 20,
                "Pickpocket": 20,
                "Speech": 15,
                "Alchemy": 20,
            },
            "Dunmer": {
                "Illusion": 20,
                "Conjuration": 15,
                "Destruction": 25,
                "Restoration": 15,
                "Alteration": 20,
                "Enchanting": 15,
                "Smithing": 15,
                "Heavy Armor": 15,
                "Block": 15,
                "Two-handed": 15,
                "One-handed": 15,
                "Archery": 15,
                "Light Armor": 20,
                "Sneak": 20,
                "Lockpicking": 15,
                "Pickpocket": 15,
                "Speech": 15,
                "Alchemy": 20,
            },
            "Orc": {
                "Illusion": 15,
                "Conjuration": 15,
                "Destruction": 15,
                "Restoration": 15,
                "Alteration": 15,
                "Enchanting": 20,
                "Smithing": 20,
                "Heavy Armor": 25,
                "Block": 20,
                "Two-handed": 20,
                "One-handed": 20,
                "Archery": 15,
                "Light Armor": 15,
                "Sneak": 15,
                "Lockpicking": 15,
                "Pickpocket": 15,
                "Speech": 15,
                "Alchemy": 15,
            },
            "Argonian": {
                "Illusion": 15,
                "Conjuration": 15,
                "Destruction": 15,
                "Restoration": 20,
                "Alteration": 20,
                "Enchanting": 15,
                "Smithing": 15,
                "Heavy Armor": 15,
                "Block": 15,
                "Two-handed": 15,
                "One-handed": 15,
                "Archery": 15,
                "Light Armor": 20,
                "Sneak": 20,
                "Lockpicking": 25,
                "Pickpocket": 20,
                "Speech": 15,
                "Alchemy": 15,
            },
            "Khajiit": {
                "Illusion": 15,
                "Conjuration": 15,
                "Destruction": 15,
                "Restoration": 15,
                "Alteration": 15,
                "Enchanting": 15,
                "Smithing": 15,
                "Heavy Armor": 15,
                "Block": 15,
                "Two-handed": 15,
                "One-handed": 20,
                "Archery": 20,
                "Light Armor": 15,
                "Sneak": 25,
                "Lockpicking": 20,
                "Pickpocket": 20,
                "Speech": 15,
                "Alchemy": 20,
            }
        }


class InputValidator:
    @staticmethod
    def is_valid_level_combination(now, goal):
        return now < goal

    @staticmethod
    def is_valid_level(level):
        try:
            level = int(level)
        except ValueError:
            return False

        return 0 < level < 300  # arbitrary cap, >= 252

    @staticmethod
    def is_valid_race(race):  # TODO
        return True

    @staticmethod
    def is_valid_selection(selection):
        return selection is not None and len(selection) > 0

    @staticmethod
    def are_valid_skills(skills):  # TODO
        return True


class ValidationException(Exception):
    def __init__(self, message, errors=None):
        super(ValidationException, self).__init__(message)
        self.__errors = errors

    def get_errors(self):
        return self.__errors