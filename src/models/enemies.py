from .base import Enemy
from src.config.settings import RESOURCE_PATH, ENEMY_SPEEDS, SCREEN_WIDTH
import random
import pygame

class Enemy1(Enemy):
    def __init__(self):
        super().__init__(f'{RESOURCE_PATH}/icon/敌人1.png', 180, 0.5)
        self.points = 10
        self.speed = ENEMY_SPEEDS["enemy1"]
        self.rect.x = random.randint(0, SCREEN_WIDTH - (int)(0.5 * 200))
        self.hp = 1

    def update(self):
        self.rect.y += self.speed

class Enemy2(Enemy):
    def __init__(self):
        super().__init__(f'{RESOURCE_PATH}/icon/敌人2.png', 180, 0.75)
        self.points = 15
        self.speed = ENEMY_SPEEDS["enemy2"]
        self.rect.x = random.randint(500, SCREEN_WIDTH - 500 - 200)
        self.num = 0
        self.change = 1
        self.hp = 2

    def update(self):
        if not self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            if self.num % 3 == 0:
                self.rect.y += self.speed
            if self.num % 50 == 0:
                self.rect.y += self.speed
            if self.num % 25 == 0:
                self.rect.x += self.speed * self.num * self.change
                self.change *= -1
            if self.num == 500:
                self.num = 0
        else:
            self.rect.y += self.speed
        self.num += 1

class Enemy3(Enemy):
    def __init__(self):
        super().__init__(f'{RESOURCE_PATH}/icon/敌人3.png', 180, 0.5)
        self.points = 15
        self.speed = ENEMY_SPEEDS["enemy3"]
        self.rect.x = random.randint(0, SCREEN_WIDTH - (int)(0.5 * 200))
        self.el, self.er = False, True
        self.hp = 2

    def update(self):
        if self.rect.right >= self.screen_rect.right:
            self.el, self.er = True, False
            self.rect.y += 400
        elif self.rect.left <= 0:
            self.el, self.er = False, True
            self.rect.y += 400
        if self.rect.left > 0 and self.el:
            self.rect.x -= self.speed
        if self.rect.right < self.screen_rect.right and self.er:
            self.rect.x += self.speed


class Enemy4(Enemy):
    def __init__(self):
        super().__init__(f'{RESOURCE_PATH}/icon/敌人4.png', 180, 0.3)
        self.points = 15
        self.speed = ENEMY_SPEEDS["enemy4"]
        self.rect.x = random.randint(0, SCREEN_WIDTH - (int)(0.3 * 200))
        self.change = random.choice([1, -1])
        self.hp = 1

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.change
        if self.rect.right >= self.screen_rect.right:
            self.change *= -1
        elif self.rect.left <= 0:
            self.change *= -1


class Enemy5(Enemy):
    def __init__(self):
        super().__init__(f'{RESOURCE_PATH}/icon/敌人5.png', 180, 1)
        self.points = 20
        self.speed = ENEMY_SPEEDS["enemy5"]
        self.rect.x = random.randint(0, SCREEN_WIDTH - (int)(1 * 200))
        self.num = 0
        self.bullets = pygame.sprite.Group()
        self.hp = 4

    def update(self):
        self.fire_switch = True
        self.rect.y += self.speed

class EnemyBoss(Enemy):
    def __init__(self):
        super().__init__(f'{RESOURCE_PATH}/icon/敌人boss.png', 0, 1.5)
        self.points = 40
        self.speed = 1
        self.rect.midtop = self.screen_rect.midtop
        self.rect.y+=60
        self.hp = 20
        self.num=0
        self.el, self.er = False, True
        self.range=200

    def update(self):
        if self.rect.x+150 >= SCREEN_WIDTH/2+self.range:
            self.el, self.er = True, False
        elif self.rect.x+150 <= SCREEN_WIDTH/2-self.range:
            self.el, self.er = False, True
        if self.el:
            self.rect.x -= self.speed
        if self.er:
            self.rect.x += self.speed