import pygame
from src.config.settings import BULLET_SPEEDS


# 玩家子弹基类
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, plane, x=10, y=10):
        super().__init__()
        self.rect = pygame.Rect(0, 0, x, y)  # 子弹的尺寸
        self.rect.midbottom = plane.rect.midtop  # 子弹的初始位置
        self.live = False

class PlayerBullet1(PlayerBullet):
    def __init__(self, plane):
        super().__init__(plane, 10, 25)

    def update(self):
        self.rect.y -= BULLET_SPEEDS["bullet1"]


class PlayerBullet2(PlayerBullet):
    def __init__(self, plane, direction):
        super().__init__(plane)
        self.direction = direction

    def update(self):
        self.rect.y -= BULLET_SPEEDS["bullet2"]
        self.rect.x -= BULLET_SPEEDS["bullet2"] * self.direction


class PlayerBullet3(PlayerBullet):
    def __init__(self, plane):
        super().__init__(plane, 130, 10)

    def update(self):
        self.rect.y -= BULLET_SPEEDS["bullet3"]


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 10, 25)
        self.rect.midtop = enemy.rect.midbottom

    def update(self):
        self.rect.y += BULLET_SPEEDS["enemy"]
