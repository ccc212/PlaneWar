from enum import Enum, auto


class MenuState(Enum):
    # 菜单相关状态
    MAIN = auto()
    AUTH = auto()
    LEADERBOARD = auto()
    SET = auto()
    MODE_SELECT = auto()

class GameState(Enum):
    # 游戏相关状态
    NOT_STARTED = auto()
    PLAYING = auto()
    PAUSED = auto()
    OVER = auto()
