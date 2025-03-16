import os
from client.src.config.settings import HIGHEST_SCORE_FILE


class ScoreManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
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
