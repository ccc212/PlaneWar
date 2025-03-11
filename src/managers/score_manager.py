import os
from src.config.settings import HIGHEST_SCORE_FILE


class ScoreManager:
    def __init__(self):
        self.highest_score = self.get_highest_score()

    # 获取最高分
    def get_highest_score(self):
        if os.path.exists(HIGHEST_SCORE_FILE):
            with open(HIGHEST_SCORE_FILE, "r") as file:
                return int(file.read())
        return 0

    # 更新最高分
    def update_highest_score(self, current_score):
        if current_score > self.highest_score:
            self.highest_score = current_score
            with open(HIGHEST_SCORE_FILE, "w") as file:
                file.write(str(current_score))
