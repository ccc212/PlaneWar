import pygame
from pygame.sprite import Sprite

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT

# 屏幕基类
class Screen(Sprite):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()

# 敌人基类
class Enemy(Screen):
    def __init__(self, path, rotation, scale):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.rotozoom(self.image, rotation, scale)
        self.rect = self.image.get_rect()
        self.live = True