from client.src.config.settings import PLAYER_SPEED, PLAYER_HP, BULLET_NUM, SCREEN_WIDTH, SCREEN_HEIGHT, RESOURCE_PATH
from .base import GameObject
from .bullets import *
import pygame


class Player(GameObject):
    def __init__(self, path, scale):
        super().__init__(path=path,
                         rotation=0,
                         scale=scale,
                         speed=PLAYER_SPEED,
                         hp=PLAYER_HP)
        self.fire = False
        self.last_shot_time = 0  # 上次发射时间
        
        # 不同武器的发射间隔(毫秒)
        self.weapon_cooldowns = {
            1: {"primary": 500, "secondary": 1200},   # 主武器0.5秒，副武器1.2秒
            2: {"primary": 100},                      # 0.1秒发射一次
            3: {"primary": 1000},                     # 1秒发射一次
        }
        self.fire_kind = 1
        self.bullets = pygame.sprite.Group()  # 玩家子弹组
        self.mleft = self.mright = self.mup = self.mdown = False
        self.original_image = pygame.image.load(path)
        self.tilted_image = pygame.image.load(f'{RESOURCE_PATH}/icon/plane_tilted.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def update(self):
        self._handle_movement()
        if self.fire and len(self.bullets) < BULLET_NUM:
            self._handle_firing()

    def _handle_firing(self):
        current_time = pygame.time.get_ticks()
        weapon = self.weapon_cooldowns[self.fire_kind]

        # 主武器发射逻辑
        if current_time - self.last_shot_time >= weapon["primary"]:
            if self.fire_kind == 1:
                self.bullets.add(PlayerBullet1(self))
            elif self.fire_kind == 2:
                self.bullets.add(PlayerBullet1(self))
            elif self.fire_kind == 3:
                self.bullets.add(PlayerBullet3(self))
            self.last_shot_time = current_time

        # 武器1的额外子弹
        if self.fire_kind == 1:
            if (current_time - self.last_shot_time) % weapon["secondary"] == 0:
                bullet2 = PlayerBullet2(self, 1)
                bullet3 = PlayerBullet2(self, -1)
                self.bullets.add(bullet2, bullet3)

    # 玩家移动
    def _handle_movement(self):
        if self.mleft and self.rect.left > 0:
            self.rect.x -= self.speed
        if self.mright and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if self.mup and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.mdown and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
