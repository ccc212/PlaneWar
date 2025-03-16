from client.src.config.settings import *
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
        self.screen_manager = Screen()
        self.screen = self.screen_manager.screen
        self.screen_rect = self.screen_manager.rect

        # 初始化属性
        self._init_attributes()

    def _init_attributes(self):
        # 初始化敌人管理
        self.enemies = pygame.sprite.Group() # 敌人组
        self.bullets = pygame.sprite.Group() # 敌人子弹组
        self.enemies_count = 0 # 敌人总数
        self.born_time = 0
        self.born_gap = random.randint(80, 180) # 敌人生成间隔
        # self.enemy_list = [Enemy1, Enemy2, Enemy3, Enemy4, Enemy5] # 敌人类型列表
        self.enemy_list = [Enemy1, Enemy3, Enemy4, Enemy5] # 敌人类型列表
        self.enemy_type = random.choice(self.enemy_list) # 敌人类型
        self.enemy = self.enemy_type
        self.num = 0
        self.boss_open = False # 是否为boss关
        
    def reset(self):
        # 重置敌人管理器状态
        self._init_attributes()

    def update(self):
        if not self.boss_open:
            self._handle_normal_enemies()
        else:
            self._handle_boss()

        self.born_time += 1
        self.enemies.update()

    def _handle_normal_enemies(self):
        if not self.enemies:
            self._spawn_enemy()
        if self.born_time >= self.born_gap and self.enemies_count < ENEMIES_TOTAL:
            self._spawn_enemy()
            self.born_time = 0
            self.enemies_count += 1
        if self.enemy.points == 20:
            self.enemy_bullet_update()

    def _handle_boss(self):
        self.boss_open = False
        if not self.enemies:
            self.enemy = EnemyBoss()
            self.enemies.add(self.enemy)
            self.enemies_count += ENEMIES_TOTAL
            if self.enemy.hp == 0:
                self.enemies.empty()
                self.enemies_count = 0

    # 随机生成敌人
    def _spawn_enemy(self):
        self.enemy_type = random.choice(self.enemy_list)
        self.enemy = self.enemy_type()
        self.enemies.add(self.enemy)

    def enemy_bullet_update(self):
        if self.num % 50 == 0:
            bullet = EnemyBullet(self.enemy)
            self.bullets.add(bullet)
            self.bullets.update()
            self.num = 0
        self.num += 1

    def restart(self):
        self.enemies_count = 0
        self.born_time = 0
        self.born_gap = random.randint(80, 180)
        self.enemy = self.enemy_type
