# 坦克类
import pygame
import random
from .bullet import Bullet


# 敌方坦克类
class enemyTank(pygame.sprite.Sprite):

    def __init__(self, x=None, is_red=None):
        pygame.sprite.Sprite.__init__(self)
        # 用于给刚生成的坦克播放出生特效
        self.born = True
        self.times = 90
        # 所有坦克
        self.tanks = ['Tank_War/images/enemyTank/enemyTank.png']
        self.tank = pygame.image.load(self.tanks[0]).convert_alpha()
        self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
        self.rect = self.tank_0.get_rect()
        # 坦克位置
        if x is None:
            self.x = random.randint(0, 2)
        else:
            self.x = x
        self.rect.left, self.rect.top = 3 + self.x * 12 * 24, 3
        # 坦克是否可以行动
        self.can_move = True
        # 坦克速度
        self.speed = 3
        # 方向
        self.direction_x, self.direction_y = 0, 1
        # 是否存活
        self.live = True
        # 子弹
        self.bullet = Bullet()

    # 射击
    def shoot(self):
        self.bullet.live = True
        self.bullet.turn(self.direction_x, self.direction_y)
        if self.direction_x == 0 and self.direction_y == -1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.bottom = self.rect.top - 1
        elif self.direction_x == 0 and self.direction_y == 1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.top = self.rect.bottom + 1
        elif self.direction_x == -1 and self.direction_y == 0:
            self.bullet.rect.right = self.rect.left - 1
            self.bullet.rect.top = self.rect.top + 20
        elif self.direction_x == 1 and self.direction_y == 0:
            self.bullet.rect.left = self.rect.right + 1
            self.bullet.rect.top = self.rect.top + 20
        else:
            raise ValueError('enemyTank class -> direction value error.')

    # 随机移动
    def move(self, tankGroup, brickGroup, ironGroup, myhome):
        self.rect = self.rect.move(self.speed * self.direction_x, self.speed * self.direction_y)
        is_move = True
        if self.direction_x == 0 and self.direction_y == -1:
            self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
            self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
            if self.rect.top < 3:
                self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
                self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
                is_move = False
        elif self.direction_x == 0 and self.direction_y == 1:
            self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
            self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
            if self.rect.bottom > 630 - 3:
                self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
                self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
                is_move = False
        elif self.direction_x == -1 and self.direction_y == 0:
            self.tank_0 = self.tank.subsurface((0, 96), (48, 48))
            self.tank_1 = self.tank.subsurface((48, 96), (48, 48))
            if self.rect.left < 3:
                self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
                self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
                is_move = False
        elif self.direction_x == 1 and self.direction_y == 0:
            self.tank_0 = self.tank.subsurface((0, 144), (48, 48))
            self.tank_1 = self.tank.subsurface((48, 144), (48, 48))
            if self.rect.right > 630 - 3:
                self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
                self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
                is_move = False
        else:
            raise ValueError('enemyTank class -> direction value error.')
        if pygame.sprite.spritecollide(self, brickGroup, False, None) or pygame.sprite.spritecollide(self, ironGroup, False, None) or pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
            is_move = False
        if pygame.sprite.collide_rect(self, myhome):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
            is_move = False
        return is_move

    # 重新载入坦克
    def reload(self):
        self.tank = pygame.image.load(self.tanks[0]).convert_alpha()
        self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
