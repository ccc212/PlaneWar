from client.src.enums.game_mode_type import GameModeType
from client.src.modes.endless_mode import EndlessMode
from client.src.modes.level_mode import LevelMode

class GameModeManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.current_mode = None
            cls._instance.modes = {}
        return cls._instance
    
    def init_modes(self):
        # 初始化游戏模式
        self.modes = {
            GameModeType.ENDLESS: EndlessMode(),
            GameModeType.LEVEL: LevelMode(),
            # TODO: 添加肉鸽模式
        }
        self.current_mode = self.modes[GameModeType.ENDLESS]
    
    def switch_mode(self, mode_type: GameModeType):
        # 切换游戏模式
        if mode_type in self.modes:
            self.current_mode = self.modes[mode_type]
            self.current_mode.reset()

    def get_current_mode(self):
        # 获取游戏模式
        return self.current_mode