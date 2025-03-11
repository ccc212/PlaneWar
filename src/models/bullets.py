import pygame
from src.config.settings import BULLET_SPEEDS


class CharacterBullet(pygame.sprite.Sprite):
    def __init__(self, plane, x=10, y=10):
        super().__init__()
        self.rect = pygame.Rect(0, 0, x, y)
        self.rect.midbottom = plane.rect.midtop
        self.live = False


class CharacterBullet1(CharacterBullet):
    def __init__(self, plane):
        super().__init__(plane, 10, 25)

    def update(self):
        self.rect.y -= BULLET_SPEEDS["character1"]


class CharacterBullet2(CharacterBullet):
    def __init__(self, plane, direction):
        super().__init__(plane)
        self.direction = direction

    def update(self):
        self.rect.y -= BULLET_SPEEDS["character2"]
        self.rect.x -= BULLET_SPEEDS["character2"] * self.direction


class CharacterBullet3(CharacterBullet):
    def __init__(self, plane):
        super().__init__(plane, 130, 10)

    def update(self):
        self.rect.y -= BULLET_SPEEDS["character3"]


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 10, 25)
        self.rect.midtop = enemy.rect.midbottom

    def update(self):
        self.rect.y += BULLET_SPEEDS["enemy"]