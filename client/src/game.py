import time
import pygame
import pyautogui
import os

from client.src.managers.score_manager import ScoreManager
from client.src.models.base import Screen
from client.src.ui.common.text import Text
from client.src.ui.game.menu import Menu
from config.settings import *
from managers.enemy_manager import EnemyManager
from models.player import Player
from client.src.enums.game_state import GameState, MenuState
from client.src.managers.state_manager import GameStateManager
from client.src.enums.even_type import EventType


class App:
    def __init__(self):
        pygame.init()

        # 获取 Screen 单例
        self.screen_manager = Screen()
        self.screen = self.screen_manager.screen
        self.screen_rect = self.screen_manager.rect

        # 鼠标位置
        self.mouse_pos = None

        # 初始化管理器
        self.score_manager = ScoreManager()
        self.enemy_manager = EnemyManager()
        self.state_manager = GameStateManager()
        self.state_manager.add_listener(EventType.GAME_STATE_CHANGE, self._on_game_state_change)

        # 初始化游戏状态
        self.game_state = GameState.NOT_STARTED
        self.setup_game()
        self.clock = pygame.time.Clock()

        # 初始化UI
        self.menu = Menu(self.screen)

        # 模拟按下shift键切换为英文输入
        pyautogui.press('shift')

    def setup_game(self):
        # 初始化玩家
        self.plane_group = pygame.sprite.Group()
        self.plane = Player(f'{RESOURCE_PATH}/icon/plane.png', 0.5)
        self.plane.rect.midbottom = self.screen_rect.midbottom
        self.plane_group.add(self.plane)

        # 初始化属性
        self._init_attributes()

    def _init_attributes(self):
        self.score = 0
        self.level = 1
        self.plane.hp = PLAYER_HP
        self.plane.rect.midbottom = self.screen_rect.midbottom
        self.enemy_manager.reset()

    def _on_game_state_change(self, new_state):
        print(new_state)
        # if new_state == GameState.PLAYING:
        #     self.start = True
        # elif new_state == GameState.OVER:
        #     self.restart_game()
        # elif new_state == GameState.MAIN:
        #     self.start = False

    def events(self):
        # 处理所有游戏事件
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                print('游戏已结束')
                pygame.quit()
            # 鼠标点击事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = pygame.mouse.get_pos()
                if self.game_state == GameState.NOT_STARTED or self.game_state == GameState.OVER:
                    self.menu.handle_click(self.mouse_pos)
            # 键盘按下事件
            elif event.type == pygame.KEYDOWN:
                if self.game_state == GameState.PLAYING:
                    match event.key:
                        case pygame.K_w | pygame.K_UP:
                            self.plane.mup = True
                        case pygame.K_a | pygame.K_LEFT:
                            self.plane.mleft = True
                            self.plane.image = pygame.transform.flip(self.plane.tilted_image, True, False)
                        case pygame.K_s | pygame.K_DOWN:
                            self.plane.mdown = True
                        case pygame.K_d | pygame.K_RIGHT:
                            self.plane.mright = True
                            self.plane.image = self.plane.tilted_image
                        case pygame.K_SPACE:
                            self.plane.fire = True
                        case pygame.K_RETURN:
                            self.state_manager.set_game_state(GameState.PAUSED)
                        case pygame.K_ESCAPE:
                            print('游戏已结束')
                            pygame.quit()
                            self.state_manager.set_game_state(GameState.OVER)
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
                            self.state_manager.set_game_state(GameState.OVER)

            # 键盘松开事件
            elif event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_w | pygame.K_UP:
                        self.plane.mup = False
                    case pygame.K_a | pygame.K_LEFT:
                        self.plane.mleft = False
                        if self.plane.mright == False:
                            self.plane.image = self.plane.original_image
                        else:
                            self.plane.image = self.plane.tilted_image
                    case pygame.K_s | pygame.K_DOWN:
                        self.plane.mdown = False
                    case pygame.K_d | pygame.K_RIGHT:
                        self.plane.mright = False
                        if self.plane.mleft == False:
                            self.plane.image = self.plane.original_image
                        else:
                            self.plane.image = pygame.transform.flip(self.plane.tilted_image, True, False)
                    case pygame.K_SPACE:
                        self.plane.fire = False

    # 玩家受伤
    def plane_hurt(self):
        self.plane.hp -= 1
        # TODO 无敌及闪烁效果

    def plane_die(self):
        self._init_attributes()

    def plane_hp(self):
        # 显示玩家血量
        plane_hp = pygame.sprite.Group()
        if self.game_state == GameState.PLAYING:
            for num in range(1, self.plane.hp + 1):
                love = pygame.sprite.Sprite()
                love.image = pygame.image.load(f'{RESOURCE_PATH}/icon/blood.png')
                love.image = pygame.transform.rotozoom(love.image, 0, 0.25)
                love.rect = love.image.get_rect()
                love.rect.x = SCREEN_WIDTH - num * 50 - 25

                love.rect.y = 25
                plane_hp.add(love)
            plane_hp.draw(self.screen)

    def restart_game(self):
        # 重置游戏状态
        self.plane.hp = 3
        self.plane.bullets.empty()
        self.enemy_manager.enemies.empty()
        self.game_state = GameState.NOT_STARTED
        self.plane.fire_kind = 1
        self.enemy_manager.bullets.empty()
        self.state_manager.set_menu_state(MenuState.MAIN)

    def collision(self):
        # 处理敌人碰撞检测
        for each in self.enemy_manager.enemies:
            if each.live:
                co1 = pygame.sprite.groupcollide(self.plane.bullets, self.enemy_manager.enemies, True, False)
                if each.hp > 0 and co1:
                    each.hp -= 1
                    if each.hp == 0:
                        self.enemy_manager.enemies.remove(each)
                        for item in co1.values():
                            self.score += self.enemy_manager.enemy.points * len(item)

        # 玩家碰撞检测
        if (pygame.sprite.spritecollideany(self.plane, self.enemy_manager.enemies) or 
            pygame.sprite.groupcollide(self.plane_group, self.enemy_manager.bullets, False, True)):
            if self.plane.hp > 0:
                self.plane_hurt()
            else:
                self.plane_die()

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

            self.game_state = self.state_manager.get_game_state()
            
            if self.game_state == GameState.PLAYING:
                self.plane_hp()
                self.collision()
                if self.plane.hp > 0:
                    self.screen.blit(self.plane.image, self.plane.rect)
                    self.level_change()
                    self.plane.update()
                    self.update_enemies()
                    self.update_bullets()
                    self.update_score()
                else:
                    self.state_manager.set_game_state(GameState.OVER)
            else:
                self.menu.draw()
                self._init_attributes()
                # self.restart_game()

            self.score_manager.update_highest_score(self.score)
            pygame.display.update()


if __name__ == '__main__':
    app = App()
    app.run()
