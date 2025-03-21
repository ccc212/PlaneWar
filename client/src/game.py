import pyautogui
import pygame

from client.src.enums.even_type import EventType
from client.src.enums.game_state import GameState, MenuState
from client.src.managers.game_mode_manager import GameModeManager
from client.src.managers.player_manager import PlayerManager
from client.src.managers.score_manager import ScoreManager
from client.src.managers.settings_manager import SettingsManager
from client.src.managers.state_manager import GameStateManager
from client.src.models.base import Screen
from client.src.ui.game.game import GameUI
from client.src.ui.game.menu import Menu
from client.src.ui.game.pause_dialog import PauseDialog
from config.settings import *
from managers.enemy_manager import EnemyManager


class App:
    def __init__(self):
        pygame.init()

        # 获取 Screen 单例
        self.screen = Screen().screen
        self.screen_rect = Screen().rect

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

    # 初始化游戏
    def setup_game(self):
        # 初始化游戏模式
        GameModeManager().init_modes()

        # 初始化属性
        self._init_attributes()

    def _init_attributes(self):
        self.score = 0
        self.level = 1
        PlayerManager().init_player()
        EnemyManager().reset()

    def _on_game_state_change(self, new_state):
        print(new_state)
        # if new_state == GameState.OVER:
            # ScoreManager().update_highest_score(self.score)

    def events(self):
        player = PlayerManager().get_player()
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
                        player.mup = True
                    elif event.key == keyboard_settings['down']:
                        player.mdown = True
                    elif event.key == keyboard_settings['left']:
                        player.mleft = True
                        player.image = pygame.transform.flip(player.tilted_image, True, False)
                    elif event.key == keyboard_settings['right']:
                        player.mright = True
                        player.image = player.tilted_image
                    elif event.key == keyboard_settings['shoot']:
                        player.fire = True
                    elif event.key == keyboard_settings['pause']:
                        GameStateManager().set_game_state(GameState.PAUSED)
                        self.pause_dialog.show()
                    elif event.key == pygame.K_TAB:
                        # 切换武器类型
                        if player.fire_kind == 1:
                            player.fire_kind = 2
                        elif player.fire_kind == 2:
                            player.fire_kind = 3
                        elif player.fire_kind == 3:
                            player.fire_kind = 1

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
                    player.mup = False
                elif event.key == keyboard_settings['down']:
                    player.mdown = False
                elif event.key == keyboard_settings['left']:
                    player.mleft = False
                    if not player.mright:
                        player.image = player.original_image
                    else:
                        player.image = player.tilted_image
                elif event.key == keyboard_settings['right']:
                    player.mright = False
                    if not player.mleft:
                        player.image = player.original_image
                    else:
                        player.image = pygame.transform.flip(player.tilted_image, True, False)
                elif event.key == keyboard_settings['shoot']:
                    player.fire = False

    def plane_die(self):
        self._init_attributes()

    def restart_game(self):
        # 重置游戏状态
        # self.plane.hp = 3
        # self.plane.bullets.empty()
        EnemyManager().enemy_group.empty()
        GameStateManager().set_game_state(GameState.NOT_STARTED)
        # self.plane.fire_kind = 1
        EnemyManager().enemy_bullet_group.empty()
        GameStateManager().set_menu_state(MenuState.MAIN)

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
                self.game_ui.draw_hp()
                is_game_over = EnemyManager().collision()
                if not is_game_over:
                    # 使用当前游戏模式更新游戏
                    GameModeManager().get_current_mode().update()

                    # self.level_change()
                    PlayerManager().update_players()
                    EnemyManager().update_enemies()

                    self.game_ui.draw_bullets(
                        PlayerManager().get_current_player_bullets(),
                        EnemyManager().enemy_bullet_group
                    )
                    self.game_ui.draw_score(
                        GameModeManager().current_mode.score,
                        ScoreManager().get_highest_score(),
                        GameModeManager().current_mode.level
                    )
                else:
                    GameStateManager().set_game_state(GameState.OVER)
            elif GameStateManager().get_game_state() == GameState.PAUSED:
                self.game_ui.draw_hp()
                self.game_ui.draw_bullets(
                    PlayerManager().get_current_player_bullets(),
                    EnemyManager().enemy_bullet_group
                )
                self.game_ui.draw_score(
                    self.score,
                    ScoreManager().get_highest_score(),
                    self.level
                )
                PlayerManager().player_group.draw(self.screen)
                EnemyManager().enemy_group.draw(self.screen)
                self.pause_dialog.draw()
            else:
                self.menu.draw()
                self._init_attributes()

            pygame.display.update()

if __name__ == '__main__':
    app = App()
    app.run()
