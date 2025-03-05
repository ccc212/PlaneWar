# 场景类
import pygame


# 石头墙
class Brick(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 调用图片素材brick（规格24*24）
        self.brick = pygame.image.load('Tank_War/images/scene/brick.png')
        self.rect = self.brick.get_rect()
        self.live = False


# 钢墙
class Iron(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 调用图片素材iron（规格24*24）
        self.iron = pygame.image.load('Tank_War/images/scene/iron.png')
        self.rect = self.iron.get_rect()
        self.live = False


# 地图
class Map():

    def __init__(self, F_map):
        self.brickGroup = pygame.sprite.Group()
        self.ironGroup = pygame.sprite.Group()
        self.iceGroup = pygame.sprite.Group()
        self.riverGroup = pygame.sprite.Group()
        self.treeGroup = pygame.sprite.Group()
        self.F_map()

    # 地图编辑
    def F_map(self):
        for x in [2, 3, 6, 7, 18, 19, 22, 23]:
            for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23]:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brick.live = True
                self.brickGroup.add(self.brick)
        for x in [10, 11, 14, 15]:
            for y in [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brick.live = True
                self.brickGroup.add(self.brick)
        for x in [4, 5, 6, 7, 18, 19, 20, 21]:
            for y in [13, 14]:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brick.live = True
                self.brickGroup.add(self.brick)
        for x in [12, 13]:
            for y in [16, 17]:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brick.live = True
                self.brickGroup.add(self.brick)
        for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24),
                     (14, 24), (11, 25), (14, 25)]:
            self.brick = Brick()
            self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
            self.brick.live = True
            self.brickGroup.add(self.brick)
        for x, y in [(0, 14), (1, 14), (12, 6), (13, 6), (12, 7), (13, 7),
                     (24, 14), (25, 14)]:
            self.iron = Iron()
            self.iron.rect.left, self.iron.rect.top = 3 + x * 24, 3 + y * 24
            self.iron.live = True
            self.ironGroup.add(self.iron)

    def protect_home(self):
        for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24),
                     (14, 24), (11, 25), (14, 25)]:
            self.iron = Iron()
            self.iron.rect.left, self.iron.rect.top = 3 + x * 24, 3 + y * 24
            self.iron.live = True
            self.ironGroup.add(self.iron)
