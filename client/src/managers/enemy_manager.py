from client.src.config.settings import *
from client.src.enums.game_state import GameState
# from client.src.managers.game_mode_manager import GameModeManager
from client.src.managers.player_manager import PlayerManager
from client.src.managers.state_manager import GameStateManager
from client.src.models.base import Screen
from client.src.models.bullets import EnemyBullet
from client.src.models.enemies import *


class EnemyManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        # 获取 Screen 单例
        self.screen = Screen().screen
        self.screen_rect = Screen().rect

        # 初始化属性
        self._init_attributes()

    def _init_attributes(self):
        # 初始化敌人管理
        self.enemy_group = pygame.sprite.Group() # 敌人组
        self.enemy_bullet_group = pygame.sprite.Group() # 敌人子弹组
        self.enemies_count = 0 # 敌人总数
        self.born_time = 0
        self.born_gap = random.randint(80, 180) # 敌人生成间隔
        # self.enemy_list = [Enemy1, Enemy2, Enemy3, Enemy4, Enemy5] # 敌人类型列表
        self.enemy_list = [Enemy1, Enemy3, Enemy4, Enemy5] # 敌人类型列表
        self.enemy_type = random.choice(self.enemy_list) # 敌人类型
        self.enemy = self.enemy_type()
        self.num = 0
        self.boss_open = False # 是否为boss关
        
    def reset(self):
        # 重置敌人管理器状态
        self._init_attributes()

    def update_enemies(self):
        if not self.boss_open:
            self._handle_normal_enemies()
        else:
            self._handle_boss()

        self.born_time += 1
        self.enemy_group.update()

        # 绘制敌人
        self.enemy_group.draw(self.screen)

    def _handle_normal_enemies(self):
        if not self.enemy_group:
            self._spawn_enemy()
        if self.born_time >= self.born_gap and self.enemies_count < ENEMIES_TOTAL:
            self._spawn_enemy()
            self.born_time = 0
            self.enemies_count += 1
        if self.enemy.points == 20:
            self.enemy_bullet_update()

    def _handle_boss(self):
        self.boss_open = False
        if not self.enemy_group:
            self.enemy = EnemyBoss()
            self.enemy_group.add(self.enemy)
            self.enemies_count += ENEMIES_TOTAL
            if self.enemy.hp == 0:
                self.enemy_group.empty()
                self.enemies_count = 0

    # 随机生成敌人
    def _spawn_enemy(self):
        self.enemy_type = random.choice(self.enemy_list)
        self.enemy = self.enemy_type()
        self.enemy_group.add(self.enemy)

    def enemy_bullet_update(self):
        if self.num % 50 == 0:
            bullet = EnemyBullet(self.enemy)

            self.enemy_bullet_group.add(bullet)
            self.enemy_bullet_group.update()
            self.num = 0
        self.num += 1

    def restart(self):
        self.enemies_count = 0
        self.born_time = 0
        self.born_gap = random.randint(80, 180)
        self.enemy = self.enemy_type()

    def collision(self):
        from client.src.managers.game_mode_manager import GameModeManager
        # 游戏结束检测
        is_game_over = False

        # 处理敌人碰撞检测
        for each in self.enemy_group:
            if each.live:
                co1 = pygame.sprite.groupcollide(PlayerManager().get_current_player_bullets(),
                                                 self.enemy_group, True, False)
                if each.hp > 0 and co1:
                    each.hp -= 1
                    if each.hp == 0:
                        self.enemy_group.remove(each)
                        # for item in co1.values():
                        #     self.score += self.enemy.points * len(item)

        # 玩家碰撞检测
        if (pygame.sprite.groupcollide(PlayerManager().player_group, self.enemy_group, False, False) or
                pygame.sprite.groupcollide(PlayerManager().player_group, self.enemy_bullet_group, False,
                                           True)):
            is_game_over = GameModeManager().get_current_mode().check_game_over()
            if is_game_over:
                GameStateManager().set_game_state(GameState.OVER)
            else:
                PlayerManager().hurt_player()

        # # 敌人到达底部
        # for enemy in self.enemies:
        #     if enemy.rect.bottom >= self.screen_rect.bottom:
        #         self.restart_game()

        # 关卡完成检查
        if self.enemies_count == ENEMIES_TOTAL:
            if not self.enemy_group:
                self.restart()
                self.update_enemies()
                self.enemy_group.draw(Screen().screen)
                # self.level += 1

        return is_game_over
