import pygame
from .base import Screen
from src.config.settings import PLAYER_SPEED, CHARACTER_HP, BULLET_NUM
from .bullets import *


class Player(Screen):
    def __init__(self, path, scale):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.rect = self.image.get_rect()
        self.speed = PLAYER_SPEED
        self.mleft = self.mright = self.mup = self.mdown = self.fire = False
        self.HP = CHARACTER_HP
        self.bullets = pygame.sprite.Group()
        self.num = 0
        self.fire_kind = 1
        self.live = True

    def update(self):
        if self.fire and len(self.bullets) < BULLET_NUM:
            if self.fire_kind == 1:
                if self.num % 50 == 0:
                    bullet1 = CharacterBullet1(self)
                    self.bullets.add(bullet1)
                if self.num % 120 == 0:
                    bullet2 = CharacterBullet2(self, 1)
                    bullet3 = CharacterBullet2(self, -1)
                    self.bullets.add(bullet2, bullet3)
                    self.num = 0
            elif self.fire_kind == 2 and self.num % 3 == 0:
                bullet = CharacterBullet1(self)
                self.bullets.add(bullet)
                self.num = 0
            elif self.fire_kind == 3 and self.num % 50 == 0:
                bullet = CharacterBullet3(self)
                self.bullets.add(bullet)
                self.num = 0
        if self.mleft and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if self.mright and self.rect.right < self.screen_rect.right:
            self.rect.x += PLAYER_SPEED
        if self.mup and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if self.mdown and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += PLAYER_SPEED
        self.num += 1