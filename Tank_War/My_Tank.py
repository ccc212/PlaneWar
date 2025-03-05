# 坦克类
import pygame
from .bullet import Bullet


# 我方坦克类
class myTank(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 初始化玩家坦克
        self.tanks = ['Tank_War/images/myTank/tank_T1.png']
        # 载入(两个tank是为了轮子特效)
        self.tank = pygame.image.load(self.tanks[0]).convert_alpha()
        self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
        self.rect = self.tank_0.get_rect()
        # 坦克方向
        self.direction_x, self.direction_y = 0, -1
        # 初始化玩家坦克位置
        self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24
        # 坦克速度
        self.speed = 3
        # 是否存活
        self.live = True
        # 有几条命
        self.life = 3
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
            raise ValueError('myTank class -> direction value error.')

    # 向上
    def move_up(self, tankGroup, brickGroup, ironGroup, myhome):
        self.direction_x, self.direction_y = 0, -1
        # 先移动后判断
        self.rect = self.rect.move(self.speed * self.direction_x,
                                   self.speed * self.direction_y)
        self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
        # 是否可以移动
        is_move = True
        # 地图顶端
        if self.rect.top < 3:
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        # 撞石头/钢墙
        if pygame.sprite.spritecollide(self, brickGroup, False, None) or pygame.sprite.spritecollide(self, ironGroup, False, None):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        # 撞其他坦克
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        # 大本营
        if pygame.sprite.collide_rect(self, myhome):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        return is_move

    # 向下
    def move_down(self, tankGroup, brickGroup, ironGroup, myhome):
        self.direction_x, self.direction_y = 0, 1
        # 先移动后判断
        self.rect = self.rect.move(self.speed * self.direction_x, self.speed * self.direction_y)
        self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
        # 是否可以移动
        is_move = True
        # 地图底端
        if self.rect.bottom > 630 - 3:
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        # 撞石头/钢墙
        if pygame.sprite.spritecollide(self, brickGroup, False, None) or pygame.sprite.spritecollide(self, ironGroup, False, None):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        # 撞其他坦克
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        # 大本营
        if pygame.sprite.collide_rect(self, myhome):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        return is_move

    # 向左
    def move_left(self, tankGroup, brickGroup, ironGroup, myhome):
        self.direction_x, self.direction_y = -1, 0
        # 先移动后判断
        self.rect = self.rect.move(self.speed * self.direction_x, self.speed * self.direction_y)
        self.tank_0 = self.tank.subsurface((0, 96), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 96), (48, 48))
        # 是否可以移动
        is_move = True
        # 地图左端
        if self.rect.left < 3:
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        # 撞石头/钢墙
        if pygame.sprite.spritecollide(self, brickGroup, False, None) or pygame.sprite.spritecollide(self, ironGroup, False, None):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        # 撞其他坦克
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        # 大本营
        if pygame.sprite.collide_rect(self, myhome):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        return is_move

    # 向右
    def move_right(self, tankGroup, brickGroup, ironGroup, myhome):
        self.direction_x, self.direction_y = 1, 0
        # 先移动后判断
        self.rect = self.rect.move(self.speed * self.direction_x, self.speed * self.direction_y)
        self.tank_0 = self.tank.subsurface((0, 144), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 144), (48, 48))
        # 是否可以移动
        is_move = True
        # 地图右端
        if self.rect.right > 630 - 3:
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        # 撞石头/钢墙
        if pygame.sprite.spritecollide(self, brickGroup, False, None) or pygame.sprite.spritecollide(self, ironGroup, False, None):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        # 撞其他坦克
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        # 大本营
        if pygame.sprite.collide_rect(self, myhome):
            self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
            is_move = False
        return is_move

    # 死后重置
    def reset(self):
        self.tank = pygame.image.load(self.tanks[0]).convert_alpha()
        self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
        self.rect = self.tank_0.get_rect()
        self.direction_x, self.direction_y = 0, -1
        self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24
        self.speed = 3
