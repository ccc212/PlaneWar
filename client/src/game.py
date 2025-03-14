import time
import pygame

from client.src.managers.score_manager import ScoreManager
from client.src.models.base import Screen
from client.src.ui.common.text import Text
from client.src.ui.game.menu import Menu
from config.settings import *
from managers.enemy_manager import EnemyManager
from models.player import Player


class App:
    def __init__(self):
        pygame.init()
        # 获取 Screen 单例
        self.screen_manager = Screen()
        self.screen = self.screen_manager.screen
        self.screen_rect = self.screen_manager.rect

        # 初始化游戏状态
        self.score = 0
        self.level = 1
        self.start = False

        # 初始化管理器
        self.score_manager = ScoreManager()
        self.enemy_manager = EnemyManager()

        # 初始化UI
        self.menu = Menu(self.screen)

        # 设置游戏状态
        self.setup_game()
        self.clock = pygame.time.Clock()

    def setup_game(self):
        # 初始化玩家
        self.plane_group = pygame.sprite.Group()
        self.plane = Player(f'{RESOURCE_PATH}/icon/plane.png', 0.5)
        self.plane.rect.midbottom = self.screen_rect.midbottom
        self.plane_group.add(self.plane)

        # 初始化UI
        self.play_font = pygame.font.SysFont('fangsong', 90, True)
        self.play_image = self.play_font.render('开始', True, BLACK)
        self.play_rect = self.play_image.get_rect()
        self.play_rect.center = self.screen_rect.center

        self.mouse_pos = None

    def events(self):
        # 处理所有游戏事件
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                print('游戏已结束')
                pygame.quit()
                self.restart.start_interface()
            # 鼠标点击事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = pygame.mouse.get_pos()
                if not self.start:
                    if self.menu.handle_click(self.mouse_pos):
                        self.start = True
            # 键盘按下事件
            elif event.type == pygame.KEYDOWN:
                if self.start:
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
                            self.start = False
                        case pygame.K_TAB:
                            # 切换武器类型
                            if self.plane.fire_kind == 1:
                                self.plane.fire_kind = 2
                            elif self.plane.fire_kind == 2:
                                self.plane.fire_kind = 3
                            elif self.plane.fire_kind == 3:
                                self.plane.fire_kind = 1
                else:
                    # 处理输入框事件
                    self.menu.auth_dialog.handle_event(event)

                    match event.key:
                        case pygame.K_ESCAPE:
                            print('游戏已结束')
                            pygame.quit()
                            self.start = False

            # 键盘松开事件
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
        # 玩家死亡处理
        self.plane.hp -= 1
        self.plane.rect.midbottom = self.screen_rect.midbottom
        time.sleep(0.5)

    def plane_hp(self):
        # 显示玩家血量
        plane_list = pygame.sprite.Group()
        if self.start == True:
            for num in range(1, self.plane.hp + 1):
                love = pygame.sprite.Sprite()
                love.image = pygame.image.load('../resources/icon/blood.png')
                love.image = pygame.transform.rotozoom(love.image, 0, 0.25)
                love.rect = love.image.get_rect()
                love.rect.x = SCREEN_WIDTH - num * 50 - 25

                love.rect.y = 25
                plane_list.add(love)
            plane_list.draw(self.screen)

    def restart_game(self):
        # 重置游戏状态
        self.plane.hp = 3
        self.plane.bullets.empty()
        self.enemy_manager.enemies.empty()
        self.start = False
        self.plane.fire_kind = 1
        self.enemy_manager.bullets.empty()

    def collision(self):
        # 处理碰撞检测
        for each in self.enemy_manager.enemies:
            if each.live:
                co1 = pygame.sprite.groupcollide(self.plane.bullets, self.enemy_manager.enemies, True, False)
                if each.hp > 0 and co1:
                    each.hp -= 1
                    if each.hp == 0:
                        self.enemy_manager.enemies.remove(each)
                        for item in co1.values():
                            self.score += self.enemy_manager.enemy.points * len(item)

        # 玩家与敌人碰撞
        if pygame.sprite.spritecollideany(self.plane, self.enemy_manager.enemies):
            self.plane_die()

        # 玩家与敌人子弹碰撞
        if pygame.sprite.groupcollide(self.plane_group, self.enemy_manager.bullets, False, True):
            self.plane.hp -= 1

        # 敌人到达底部
        for enemy in self.enemy_manager.enemies:
            if enemy.rect.bottom >= self.screen_rect.bottom:
                self.restart_game()

        # 关卡完成检查
        if self.enemy_manager.enemies_count == ENEMIES_TOTAL:
            if not self.enemy_manager.enemies:
                self.enemy_manager.restart()
                self.enemy_manager.update()
                self.enemy_manager.enemies.draw(self.screen)
                self.level += 1

    def update_score(self):
        # 更新分数显示
        self.highest_score_str = Text('最高分：' + str(self.score_manager.get_highest_score()))
        self.highest_score_str.str_rect = pygame.Rect(0, 0, 1800, 40)
        self.score_str = Text('分数：' + str(self.score))
        self.score_str.str_rect = pygame.Rect(0, 40, 1800, 40)
        self.level_str = Text('关卡：' + str(self.level))
        self.level_str.str_rect = pygame.Rect(0, 80, 1800, 40)
        self.tab_str = Text('按Tab更换攻击方式')
        self.tab_str.str_rect.midtop = self.screen_rect.midtop

        self.screen.blit(self.highest_score_str.str_image, self.highest_score_str.str_rect)
        self.screen.blit(self.score_str.str_image, self.score_str.str_rect)
        self.screen.blit(self.level_str.str_image, self.level_str.str_rect)
        self.screen.blit(self.tab_str.str_image, self.tab_str.str_rect)

    def update_bullets(self):
        # 更新子弹位置
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
        # 更新敌人位置
        self.enemy_manager.update()
        self.enemy_manager.enemies.draw(self.screen)

    def level_change(self):
        # 关卡变化处理
        if self.level % 3 == 0:
            self.enemy_manager.boss_open = True
        else:
            self.enemy_manager.boss_open = False

    def run(self):
        # 游戏主循环
        while True:
            self.score_manager.get_highest_score()
            self.clock.tick(FPS)
            self.screen.fill(WHITE)
            self.events()

            # 游戏运行中
            if self.plane.hp > 0 and self.start:
                self.screen.blit(self.plane.image, self.plane.rect)
                self.level_change()
                self.plane.update()
                self.update_enemies()
                self.update_bullets()
                self.update_score()
                self.collision()
            # 游戏结束或未开始
            else:
                self.menu.draw()
                self.score = 0
                self.level = 1
                self.restart_game()

            self.plane_hp()

            self.score_manager.update_highest_score(self.score)
            pygame.display.update()


if __name__ == '__main__':
    app = App()
    app.run()
