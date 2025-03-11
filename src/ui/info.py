import pygame
from src.config.settings import GRAY

class Info:
    def __init__(self, text):
        self.font = pygame.font.SysFont('fangsong', 40, True)
        self.str_image = self.font.render(text, True, GRAY)
        self.str_rect = self.str_image.get_rect()