from client.src.config.settings import ENEMIES_TOTAL, RESOURCE_PATH
from client.src.managers.auth_manager import AuthManager
from client.src.managers.enemy_manager import EnemyManager
from client.src.managers.player_manager import PlayerManager
from client.src.models.base import Screen
from client.src.models.player import Player
from client.src.modes.base_mode import BaseGameMode


class EndlessMode(BaseGameMode):
    def __init__(self):
        super().__init__()
        self.enemies_total = ENEMIES_TOTAL
        PlayerManager().clear_players()
        self.plane = Player(
            f'{RESOURCE_PATH}/icon/plane.png',
            f'{RESOURCE_PATH}/icon/plane_tilted.png',
            0.5
        )
        PlayerManager().add_player(
            AuthManager().get_username(),
            self.plane
        )

    def update(self):
        if self.check_game_over():
            return

        # 关卡完成检查
        if EnemyManager().enemies_count == self.enemies_total:
            if not EnemyManager().enemy_group:
                self.next_wave()

    def next_wave(self):
        # 进入下一波
        EnemyManager().restart()
        EnemyManager().update_enemies()
        self.level += 1
        # 每5关出现boss
        if self.level % 5 == 0:
            EnemyManager().boss_open = True
        else:
            EnemyManager().boss_open = False

    def reset(self):
        self.score = 0
        self.level = 1
        EnemyManager().reset()
        self.plane.rect.midbottom = Screen().rect.midbottom
