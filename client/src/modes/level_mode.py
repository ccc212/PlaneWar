from client.src.modes.base_mode import BaseGameMode
from client.src.managers.enemy_manager import EnemyManager
# from client.src.levels.level_manager import LevelManager

class LevelMode(BaseGameMode):
    def __init__(self):
        super().__init__()

    def update(self):
        if self.check_game_over():
            return
            
        # 检查关卡是否完成
        if not EnemyManager().enemy_group:
            self.next_level()
    
    def next_level(self):
        print('next_level')
        # 进入下一关
        # self.level += 1
        # level_data = LevelManager().get_level(self.level)
        # if level_data:
        #     self.load_level(level_data)
        # else:
        #     # 所有关卡完成
        #     GameStateManager().set_game_state(GameState.WIN)
    
    def load_level(self, level_data):
        # 加载关卡数据
        EnemyManager().load_level(level_data)
    
    def reset(self):
        self.score = 0
        self.level = 1
        EnemyManager().reset()