from abc import ABC, abstractmethod

from client.src.enums.game_state import GameState
from client.src.managers.player_manager import PlayerManager
from client.src.managers.state_manager import GameStateManager


class BaseGameMode(ABC):
    def __init__(self):
        self.score = None
        self.level = None
        self.init_attributes()
    
    @abstractmethod
    def update(self):
        # 更新游戏
        pass
    
    @abstractmethod
    def reset(self):
        # 重置游戏状态
        pass

    def init_attributes(self):
        self.score = 0
        self.level = 1
    
    def check_game_over(self):
        # 检查游戏是否结束
        all_players_dead = all(player.hp <= 0 for player in PlayerManager().players.values())
        if all_players_dead:
            GameStateManager().set_game_state(GameState.OVER)
            return True
        return False