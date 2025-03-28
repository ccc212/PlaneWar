from .base import Enemy
from client.src.config.settings import RESOURCE_PATH, ENEMY_SPEEDS, SCREEN_WIDTH
import random
import pygame


class Enemy1(Enemy):
    def __init__(self):
        super().__init__(
            path=f'{RESOURCE_PATH}/icon/enemy1.png',
            rotation=180,
            scale=0.5,
            points=10,
            speed=ENEMY_SPEEDS["enemy1"],
            hp=1,
            spawn_x=random.randint(0, SCREEN_WIDTH - (int)(0.5 * 200)))

    def update(self):
        self.rect.y += self.speed


class Enemy2(Enemy):
    def __init__(self):
        super().__init__(
            path=f'{RESOURCE_PATH}/icon/enemy2.png',
            rotation=180,
            scale=0.75,
            points=15,
            speed=ENEMY_SPEEDS["enemy2"],
            hp=2,
            spawn_x=random.randint(500, SCREEN_WIDTH - 500 - 200))
        self.num = 0
        self.change = 1

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
        super().__init__(
            path=f'{RESOURCE_PATH}/icon/enemy3.png',
            rotation=180,
            scale=0.5,
            points=15,
            speed=ENEMY_SPEEDS["enemy3"],
            hp=2,
            spawn_x=random.randint(0, SCREEN_WIDTH - (int)(0.5 * 200)))
        self.el, self.er = False, True

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
        super().__init__(
            path=f'{RESOURCE_PATH}/icon/enemy4.png',
            rotation=180,
            scale=0.3,
            points=15,
            speed=ENEMY_SPEEDS["enemy4"],
            hp=1,
            spawn_x=random.randint(0, SCREEN_WIDTH - (int)(0.3 * 200)))
        self.change = random.choice([1, -1])

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.change
        if self.rect.right >= self.screen_rect.right:
            self.change *= -1
        elif self.rect.left <= 0:
            self.change *= -1


class Enemy5(Enemy):
    def __init__(self):
        super().__init__(
            path=f'{RESOURCE_PATH}/icon/enemy5.png',
            rotation=180,
            scale=1,
            points=20,
            speed=ENEMY_SPEEDS["enemy5"],
            hp=4,
            spawn_x=random.randint(0, SCREEN_WIDTH - (int)(1 * 200)))
        self.num = 0
        self.enemy_bullet_group = pygame.sprite.Group()

    def update(self):
        self.fire_switch = True
        self.rect.y += self.speed


class EnemyBoss(Enemy):
    def __init__(self):
        super().__init__(
            path=f'{RESOURCE_PATH}/icon/enemy_boss.png',
            rotation=0,
            scale=1.5,
            points=40,
            speed=1,
            hp=20)
        self.rect.midtop = self.screen_rect.midtop
        self.rect.y += 60
        self.num = 0
        self.el, self.er = False, True
        self.range = 200

    def update(self):
        if self.rect.x + 150 >= SCREEN_WIDTH / 2 + self.range:
            self.el, self.er = True, False
        elif self.rect.x + 150 <= SCREEN_WIDTH / 2 - self.range:
            self.el, self.er = False, True
        if self.el:
            self.rect.x -= self.speed
        if self.er:
            self.rect.x += self.speed
