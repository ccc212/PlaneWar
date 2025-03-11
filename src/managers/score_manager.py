import os
from src.config.settings import HIGHEST_SCORE_FILE

class ScoreManager:
    def __init__(self):
        self.highest_score = self.get_high_score()

    def get_high_score(self):
        if os.path.exists(HIGHEST_SCORE_FILE):
            with open(HIGHEST_SCORE_FILE, "r") as file:
                return int(file.read())
        return 0

    def update_high_score(self, current_score):
        if current_score > self.highest_score:
            self.highest_score = current_score
            with open(HIGHEST_SCORE_FILE, "w") as file:
                file.write(str(current_score))