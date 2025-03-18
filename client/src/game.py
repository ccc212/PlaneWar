import pyautogui
import pygame

from client.src.enums.even_type import EventType
from client.src.enums.game_state import GameState, MenuState
from client.src.managers.score_manager import ScoreManager
from client.src.managers.state_manager import GameStateManager
from client.src.models.base import Screen
from client.src.ui.game.game import GameUI
from client.src.ui.game.menu import Menu
from client.src.ui.game.pause_dialog import PauseDialog
from config.settings import *
from managers.enemy_manager import EnemyManager
from models.player import Player
from client.src.managers.settings_manager import SettingsManager


class App:
    def __init__(self):
        pygame.init()

        # 获取 Screen 单例
        self.screen_manager = Screen()
        self.screen = self.screen_manager.screen
        self.screen_rect = self.screen_manager.rect

        # 鼠标位置
        self.mouse_pos = None

        # 添加游戏状态监听器
        GameStateManager().add_listener(EventType.GAME_STATE_CHANGE, self._on_game_state_change)

        # 初始化游戏状态
        GameStateManager().set_game_state(GameState.NOT_STARTED)
        self.setup_game()
        self.clock = pygame.time.Clock()

        # 初始化UI
        self.menu = Menu(self.screen)
        self.game_ui = GameUI(self.screen)
        self.pause_dialog = PauseDialog(self.screen)

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
        EnemyManager().reset()

    def _on_game_state_change(self, new_state):
        print(new_state)
        if new_state == GameState.OVER:
            ScoreManager().update_highest_score(self.score)

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
                if (GameStateManager().get_game_state() == GameState.NOT_STARTED 
                        or GameStateManager().get_game_state() == GameState.OVER):
                    self.menu.handle_click(self.mouse_pos)
                elif GameStateManager().get_game_state() == GameState.PAUSED:
                    is_restart = self.pause_dialog.handle_click(self.mouse_pos)
                    if is_restart:
                        self.setup_game()
                        GameStateManager().set_game_state(GameState.PLAYING)
            # 键盘按下事件
            elif event.type == pygame.KEYDOWN:
                if GameStateManager().get_game_state() == GameState.PLAYING:
                    keyboard_settings = SettingsManager().get_keyboard_settings()
                    if event.key == keyboard_settings['up']:
                        self.plane.mup = True
                    elif event.key == keyboard_settings['down']:
                        self.plane.mdown = True
                    elif event.key == keyboard_settings['left']:
                        self.plane.mleft = True
                        self.plane.image = pygame.transform.flip(self.plane.tilted_image, True, False)
                    elif event.key == keyboard_settings['right']:
                        self.plane.mright = True
                        self.plane.image = self.plane.tilted_image
                    elif event.key == keyboard_settings['shoot']:
                        self.plane.fire = True
                    elif event.key == keyboard_settings['pause']:
                        GameStateManager().set_game_state(GameState.PAUSED)
                        self.pause_dialog.show()
                    elif event.key == pygame.K_TAB:
                        # 切换武器类型
                        if self.plane.fire_kind == 1:
                            self.plane.fire_kind = 2
                        elif self.plane.fire_kind == 2:
                            self.plane.fire_kind = 3
                        elif self.plane.fire_kind == 3:
                            self.plane.fire_kind = 1

                elif GameStateManager().get_menu_state() == MenuState.AUTH:
                    # 处理输入框事件
                    self.menu.auth_dialog.handle_event(event)

                elif GameStateManager().get_menu_state() == MenuState.SET:
                    self.menu.set_dialog.handle_keydown(event)

                elif GameStateManager().get_game_state() == GameState.PAUSED and self.pause_dialog.is_set:
                    self.pause_dialog.set_dialog.handle_keydown(event)

            # 键盘松开事件
            elif event.type == pygame.KEYUP:
                keyboard_settings = SettingsManager().get_keyboard_settings()
                if event.key == keyboard_settings['up']:
                    self.plane.mup = False
                elif event.key == keyboard_settings['down']:
                    self.plane.mdown = False
                elif event.key == keyboard_settings['left']:
                    self.plane.mleft = False
                    if not self.plane.mright:
                        self.plane.image = self.plane.original_image
                    else:
                        self.plane.image = self.plane.tilted_image
                elif event.key == keyboard_settings['right']:
                    self.plane.mright = False
                    if not self.plane.mleft:
                        self.plane.image = self.plane.original_image
                    else:
                        self.plane.image = pygame.transform.flip(self.plane.tilted_image, True, False)
                elif event.key == keyboard_settings['shoot']:
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
        if GameStateManager().get_game_state() == GameState.PLAYING:
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
        EnemyManager().enemies.empty()
        GameStateManager().set_game_state(GameState.NOT_STARTED)
        self.plane.fire_kind = 1
        EnemyManager().bullets.empty()
        GameStateManager().set_menu_state(MenuState.MAIN)

    def collision(self):
        # 处理敌人碰撞检测
        for each in EnemyManager().enemies:
            if each.live:
                co1 = pygame.sprite.groupcollide(self.plane.bullets, EnemyManager().enemies, True, False)
                if each.hp > 0 and co1:
                    each.hp -= 1
                    if each.hp == 0:
                        EnemyManager().enemies.remove(each)
                        for item in co1.values():
                            self.score += EnemyManager().enemy.points * len(item)

        # 玩家碰撞检测
        if (pygame.sprite.spritecollideany(self.plane, EnemyManager().enemies) or
            pygame.sprite.groupcollide(self.plane_group, EnemyManager().bullets, False, True)):
            if self.plane.hp > 0:
                self.plane_hurt()
            else:
                self.plane_die()

        # 敌人到达底部
        for enemy in EnemyManager().enemies:
            if enemy.rect.bottom >= self.screen_rect.bottom:
                self.restart_game()

        # 关卡完成检查
        if EnemyManager().enemies_count == ENEMIES_TOTAL:
            if not EnemyManager().enemies:
                EnemyManager().restart()
                EnemyManager().update()
                EnemyManager().enemies.draw(self.screen)
                self.level += 1

    def update_enemies(self):
        # 更新敌人位置
        EnemyManager().update()
        EnemyManager().enemies.draw(self.screen)

    def level_change(self):
        # 关卡变化处理
        if self.level % 3 == 0:
            EnemyManager().boss_open = True
        else:
            EnemyManager().boss_open = False

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)
            self.events()

            if GameStateManager().get_game_state() == GameState.PLAYING:
                self.game_ui.draw_hp(self.plane.hp)
                self.collision()
                if self.plane.hp > 0:
                    self.screen.blit(self.plane.image, self.plane.rect)
                    self.level_change()
                    self.plane.update()
                    self.update_enemies()
                    self.game_ui.draw_bullets(self.plane.bullets, EnemyManager().bullets)
                    self.game_ui.draw_score(
                        self.score,
                        ScoreManager().get_highest_score(),
                        self.level
                    )
                else:
                    GameStateManager().set_game_state(GameState.OVER)
            elif GameStateManager().get_game_state() == GameState.PAUSED:
                self.game_ui.draw_hp(self.plane.hp)
                self.screen.blit(self.plane.image, self.plane.rect)
                self.game_ui.draw_bullets(self.plane.bullets, EnemyManager().bullets)
                self.game_ui.draw_score(
                    self.score,
                    ScoreManager().get_highest_score(),
                    self.level
                )
                EnemyManager().enemies.draw(self.screen)
                self.pause_dialog.draw()
            else:
                self.menu.draw()
                self._init_attributes()

            pygame.display.update()


if __name__ == '__main__':
    app = App()
    app.run()
