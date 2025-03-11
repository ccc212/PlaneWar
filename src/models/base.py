import pygame
from pygame.sprite import Sprite
from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
import random


# 屏幕管理类
class Screen:
    _instance = None  # 单例模式

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                pygame.FULLSCREEN
            )
            cls._instance.rect = cls._instance.screen.get_rect()  # 用于处理碰撞检测和位置计算
        return cls._instance


# 游戏对象基类
class GameObject(Sprite):
    def __init__(self, path, rotation, scale, speed, hp):
        super().__init__()
        # 加载并处理图片
        self.image = pygame.image.load(path)  # 加载图片
        self.image = pygame.transform.rotozoom(self.image, rotation, scale)  # 对图片进行旋转及缩放
        self.rect = self.image.get_rect()  # 获取图片的碰撞器

        # 基础属性
        self.speed = speed  # 移动速度
        self.hp = hp  # 生命值
        self.live = True  # 是否活着

        # 获取 Screen 单例
        self.screen_manager = Screen()
        self.screen = self.screen_manager.screen
        self.screen_rect = self.screen_manager.rect


# 敌人基类
class Enemy(GameObject):
    def __init__(self, path, rotation, scale, points, speed, hp, spawn_x=None):
        super().__init__(path, rotation, scale, speed, hp)
        # 击败后获得的分数
        self.points = points

        # 设置初始位置
        if spawn_x is None:
            # 默认在屏幕宽度范围内随机生成
            self.rect.x = random.randint(0, SCREEN_WIDTH - int(scale * 200))
        else:
            self.rect.x = spawn_x
