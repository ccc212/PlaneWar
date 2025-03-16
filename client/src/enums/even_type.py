from enum import Enum, auto

class EventType(Enum):
    # UI状态变化事件
    UI_STATE_CHANGE = auto()

    # 游戏状态变化事件
    GAME_STATE_CHANGE = auto()