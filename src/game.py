import pygame, time
from config.settings import *
from models.player import Player
from managers.enemy_manager import EnemyManager
from src.models.base import Screen
from src.ui.info import Info
from os import path
from src.managers.score_manager import ScoreManager


class App(Screen):
    def __init__(self):
        super().__init__()
        pygame.init()

        self.score = 0
        self.level = 1
        self.score_manager = ScoreManager()
        self.enemy_manager = EnemyManager()

        self.setup_game()
        self.clock = pygame.time.Clock()

    def setup_game(self):
        # 初始化玩家
        self.plane_group = pygame.sprite.Group()
        self.plane = Player(f'{RESOURCE_PATH}/icon/飞机.png', 0.5)
        self.plane.rect.midbottom = self.screen_rect.midbottom
        self.plane_group.add(self.plane)

        # 初始化UI
        self.play_font = pygame.font.SysFont('fangsong', 90, True)
        self.play_image = self.play_font.render('开始', True, BLACK)
        self.play_rect = self.play_image.get_rect()
        self.play_rect.center = self.screen_rect.center

        self.mouse_pos = None
        self.start = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('游戏已结束')
                pygame.quit()
                self.restart.start_interface()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = pygame.mouse.get_pos()
                if self.play_rect.collidepoint(self.mouse_pos):
                    self.start = True
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w | pygame.K_UP:
                        self.plane.mup = True
                    case pygame.K_a | pygame.K_LEFT:
                        self.plane.mleft = True
                    case pygame.K_s | pygame.K_DOWN:
                        self.plane.mdown = True
                    case pygame.K_d | pygame.K_RIGHT:
                        self.plane.mright = True
                    case pygame.K_SPACE:
                        self.plane.fire = True
                    case pygame.K_RETURN:
                        self.start = True
                    case pygame.K_ESCAPE:
                        print('游戏已结束')
                        pygame.quit()
                        self.start
                    case pygame.K_TAB:
                        if self.plane.fire_kind==1:
                            self.plane.fire_kind = 2
                        elif  self.plane.fire_kind==2:
                            self.plane.fire_kind = 3
                        elif  self.plane.fire_kind==3:
                            self.plane.fire_kind = 1

            elif event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_w | pygame.K_UP:
                        self.plane.mup = False
                    case pygame.K_a | pygame.K_LEFT:
                        self.plane.mleft = False
                    case pygame.K_s | pygame.K_DOWN:
                        self.plane.mdown = False
                    case pygame.K_d | pygame.K_RIGHT:
                        self.plane.mright = False
                    case pygame.K_SPACE:
                        self.plane.fire = False

    def plane_die(self):
        self.plane.HP -= 1
        self.plane.rect.midbottom = self.screen_rect.midbottom
        time.sleep(0.5)

    def plane_hp(self):
        plane_list = pygame.sprite.Group()
        if self.start == True:
            for num in range(1, self.plane.HP + 1):
                love = pygame.sprite.Sprite()
                love.image = pygame.image.load('../resources/icon/血.png')
                love.image = pygame.transform.rotozoom(love.image, 0, 0.25)
                love.rect = love.image.get_rect()
                love.rect.x = SCREEN_WIDTH - num * 50 - 25

                love.rect.y = 25
                plane_list.add(love)
            plane_list.draw(self.screen)

    def restart_game3(self):
        self.plane.HP = 3
        self.plane.bullets.empty()
        self.enemy_manager.enemies.empty()
        self.start = False
        self.plane.fire_kind=1
        self.enemy_manager.bullets.empty()

    def collision(self):
        for each in self.enemy_manager.enemies:
            if each.live:
                co1 =pygame.sprite.groupcollide(self.plane.bullets,self.enemy_manager.enemies,True,False)
                if each.hp>0 and co1:
                    each.hp-=1
                    if each.hp == 0:
                        self.enemy_manager.enemies.remove(each)
                        for item in co1.values():
                            self.score += self.enemy_manager.enemy.points * len(item)

        if pygame.sprite.spritecollideany(self.plane, self.enemy_manager.enemies):
            self.plane_die()

        if pygame.sprite.groupcollide(self.plane_group, self.enemy_manager.bullets, False, True):
            self.plane.HP -= 1

        for enemy in self.enemy_manager.enemies:
            if enemy.rect.bottom >= self.screen_rect.bottom:
                self.restart_game3()

        if self.enemy_manager.enemies_count == ENEMIES_TOTAL:
            if not self.enemy_manager.enemies:
                self.enemy_manager.restart()
                self.enemy_manager.update()
                self.enemy_manager.enemies.draw(self.screen)
                self.level += 1

    def update_score(self):
        self.highest_score_str = Info('最高分：' + str(self.highest_score))
        self.highest_score_str.str_rect = pygame.Rect(0, 0, 1800, 40)
        self.score_str = Info('分数：' + str(self.score))
        self.score_str.str_rect = pygame.Rect(0, 40, 1800, 40)
        self.level_str = Info('关卡：' + str(self.level))
        self.level_str.str_rect = pygame.Rect(0, 80, 1800, 40)
        self.tab_str = Info('按Tab更换攻击方式')
        self.tab_str.str_rect.midtop = self.screen_rect.midtop

        self.screen.blit(self.highest_score_str.str_image, self.highest_score_str.str_rect)
        self.screen.blit(self.score_str.str_image, self.score_str.str_rect)
        self.screen.blit(self.level_str.str_image, self.level_str.str_rect)
        self.screen.blit(self.tab_str.str_image, self.tab_str.str_rect)

    def update_bullets(self):
        for bullet in self.plane.bullets:
            pygame.draw.rect(self.screen, BLACK, bullet.rect)
            bullet.update()
            if bullet.rect.bottom < 0:
                self.plane.bullets.remove(bullet)
        for bullet in self.enemy_manager.bullets:
            pygame.draw.rect(self.screen, BLACK, bullet.rect)
            bullet.update()
            if bullet.rect.bottom > self.screen_rect.bottom:
                self.enemy_manager.bullets.remove(bullet)

    def update_enemies(self):
        self.enemy_manager.update()
        self.enemy_manager.enemies.draw(self.screen)

    def update_high_score(self):
        self.highest_score = self.get_high_score()
        if self.score > self.highest_score:
            with open(HIGHEST_SCORE_FILE, "w") as file:
                file.write(str(self.score))

    def get_high_score(self):
        if path.exists(HIGHEST_SCORE_FILE):
            with open(HIGHEST_SCORE_FILE, "r") as file:
                high_score = int(file.read())
        return high_score

    def level_change(self):
        if self.level == 3:
            self.enemy_manager.boss_open=True
        else:
            self.enemy_manager.boss_open=False

    def run(self):
        while True:
            self.get_high_score()
            self.clock.tick(FPS)
            self.screen.fill(WHITE)
            self.events()

            if self.plane.HP > 0 and self.start:
                self.screen.blit(self.plane.image, self.plane.rect)
                self.level_change()
                self.plane.update()
                self.update_enemies()
                self.update_bullets()
                self.update_score()
                self.collision()
            else:
                self.screen.blit(self.play_image, self.play_rect)
                self.score = 0
                self.level = 1
                self.restart_game3()

            self.plane_hp()

            self.update_high_score()
            pygame.display.update()

if __name__ == '__main__':
    app = App()
    app.run()