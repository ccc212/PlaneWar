import pygame

from client.src.config.settings import BLACK, RESOURCE_PATH, SCREEN_WIDTH, GRAY
from client.src.managers.enemy_manager import EnemyManager
from client.src.managers.player_manager import PlayerManager
from client.src.ui.common.message_dialog import MessageDialog


class GameUI:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game_font = pygame.font.SysFont('fangsong', 40, True)
        self.message_dialog = MessageDialog(screen)

    def draw_hp(self):
        # 显示玩家血量
        player = PlayerManager().get_player()
        plane_hp_group = pygame.sprite.Group()
        for num in range(1, player.hp + 1):
            love = pygame.sprite.Sprite()
            love.image = pygame.image.load(f'{RESOURCE_PATH}/icon/blood.png')
            love.image = pygame.transform.rotozoom(love.image, 0, 0.25)
            love.rect = love.image.get_rect()
            love.rect.x = SCREEN_WIDTH - num * 50 - 25
            love.rect.y = 25
            plane_hp_group.add(love)
        plane_hp_group.draw(self.screen)

    def draw_score(self, score, highest_score, level):
        # 更新分数显示
        highest_score_str = self.game_font.render(f'最高分：{highest_score}', True, GRAY)
        highest_score_str_rect = pygame.Rect(0, 0, 1800, 40)

        score_str = self.game_font.render(f'分数：{score}', True, GRAY)
        score_str_rect = pygame.Rect(0, 40, 1800, 40)

        level_str = self.game_font.render(f'关卡：{level}', True, GRAY)
        level_str_rect = pygame.Rect(0, 80, 1800, 40)

        tab_str = self.game_font.render('按Tab更换攻击方式', True, GRAY)
        tab_str_rect = tab_str.get_rect()
        tab_str_rect.midtop = self.screen_rect.midtop

        self.screen.blit(highest_score_str, highest_score_str_rect)
        self.screen.blit(score_str, score_str_rect)
        self.screen.blit(level_str, level_str_rect)
        self.screen.blit(tab_str, tab_str_rect)

    def draw_bullets(self, plane_bullets, enemy_bullets):
        # 更新玩家子弹位置
        if plane_bullets:
            for bullet in plane_bullets:
                pygame.draw.rect(self.screen, BLACK, bullet.rect)
                bullet.update()
                if bullet.rect.bottom < 0:
                    plane_bullets.remove(bullet)

        # 更新敌人子弹位置
        EnemyManager().enemy_bullet_update()
        if enemy_bullets:
            for bullet in enemy_bullets:
                pygame.draw.rect(self.screen, BLACK, bullet.rect)
                bullet.update()
                if bullet.rect.bottom > self.screen_rect.bottom:
                    enemy_bullets.remove(bullet)