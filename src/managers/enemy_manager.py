from src.config.settings import *
from src.models.base import Screen
from src.models.bullets import EnemyBullet
from src.models.enemies import *


class EnemyManager(Screen):
    def __init__(self):
        super().__init__()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies_count = 0
        self.born_time = 0
        self.born_gap = random.randint(80, 180)
        self.enemy_list = [Enemy1, Enemy2, Enemy3, Enemy4, Enemy5]
        self.enemy_type = random.choice(self.enemy_list)
        self.enemy = self.enemy_type
        self.num = 0
        self.boss_open = False

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