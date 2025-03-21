import pygame

from client.src.config.settings import BLACK
from client.src.enums.game_state import MenuState, GameState
from client.src.enums.even_type import EventType
from client.src.managers.game_mode_manager import GameModeManager
from client.src.ui.auth.auth import AuthDialog
from client.src.ui.common.button import Button
from client.src.ui.leaderboard.leaderboard_dialog import LeaderboardDialog
from client.src.managers.state_manager import GameStateManager
from client.src.ui.mode.mode_select_dialog import ModeSelectDialog
from client.src.ui.set.set_dialog import SetDialog


class Menu:
    def __init__(self, screen):
        # 保存游戏主屏幕
        self.screen = screen
        # 获取屏幕矩形区域
        self.screen_rect = screen.get_rect()

        # 按钮字体
        self.button_font = pygame.font.SysFont('fangsong', 50, True)

        # 开始按钮
        self.play_button = Button(
            screen=screen,
            text='开始',
            font=self.button_font,
            color=BLACK,
            center=(self.screen_rect.centerx, self.screen_rect.centery - 100)
        )

        # 排行榜按钮
        self.leaderboard_button = Button(
            screen=screen,
            text='排行榜',
            font=self.button_font,
            color=BLACK,
            center=(self.screen_rect.centerx, self.screen_rect.centery)
        )

        # 设置按钮
        self.set_button = Button(
            screen=screen,
            text='设置',
            font=self.button_font,
            color=BLACK,
            center=(self.screen_rect.centerx, self.screen_rect.centery + 100)
        )

        # 退出游戏按钮
        self.exit_button = Button(
            screen=screen,
            text='退出游戏',
            font=self.button_font,
            color=BLACK,
            center=(self.screen_rect.centerx, self.screen_rect.centery + 200)
        )

        # 用户状态按钮
        self.auth_font = pygame.font.SysFont('fangsong', 30, True)
        self.auth_button = Button(
            screen=screen,
            text='未登录',
            font=self.auth_font,
            color=BLACK,
            center=(self.screen_rect.right - 150, 50)
        )

        # 创建登录对话框
        self.auth_dialog = AuthDialog(screen)
        # 创建排行榜对话框
        self.leaderboard_dialog = LeaderboardDialog(screen)
        # 创建设置对话框
        self.set_dialog = SetDialog(screen, MenuState.MAIN)
        # 创建关卡选择对话框
        self.mode_select_dialog = ModeSelectDialog(screen)

        # 注册状态变化监听器
        GameStateManager().add_listener(EventType.UI_STATE_CHANGE, self._on_ui_state_change)
        # 初始化状态
        GameStateManager().set_menu_state(MenuState.MAIN)

        # 保存当前登录用户名
        self.username = None

    def _on_ui_state_change(self, new_state):
        self.current_state = new_state
        if new_state == MenuState.LEADERBOARD:
            self.leaderboard_dialog.fetch_leaderboard()

    def draw(self):
        if self.current_state == MenuState.LEADERBOARD:
            self.leaderboard_dialog.draw()
        elif self.current_state == MenuState.AUTH:
            self.auth_dialog.draw()
        elif self.current_state == MenuState.SET:
            self.set_dialog.draw()
        elif self.current_state == MenuState.MAIN:
            # 用户显示
            if not self.username:
                self.auth_button.update_text('未登录')
            else:
                self.auth_button.update_text(self.username)

            # 绘制按钮
            self.auth_button.draw()
            self.play_button.draw()
            self.set_button.draw()
            self.exit_button.draw()
            self.leaderboard_button.draw()
        elif self.current_state == MenuState.MODE_SELECT:
            self.mode_select_dialog.draw()

    def handle_click(self, pos):
        if self.current_state == MenuState.LEADERBOARD:
            self.leaderboard_dialog.handle_click(pos)
        elif self.current_state == MenuState.AUTH:
            result = self.auth_dialog.handle_click(pos)
            if isinstance(result, str):
                self.username = result
        elif self.current_state == MenuState.SET:
            self.set_dialog.handle_click(pos)
        elif self.current_state == MenuState.MAIN:
            if self.auth_button.rect.collidepoint(pos):
                GameStateManager().set_menu_state(MenuState.AUTH)
            elif self.leaderboard_button.rect.collidepoint(pos):
                GameStateManager().set_menu_state(MenuState.LEADERBOARD)
            elif self.play_button.rect.collidepoint(pos):
                GameStateManager().set_menu_state(MenuState.MODE_SELECT)
            elif self.set_button.rect.collidepoint(pos):
                GameStateManager().set_menu_state(MenuState.SET)
            elif self.exit_button.rect.collidepoint(pos):
                pygame.quit()
        elif self.current_state == MenuState.MODE_SELECT:
            mode = self.mode_select_dialog.handle_click(pos)
            if mode:
                if mode == "back":
                    GameStateManager().set_menu_state(MenuState.MAIN)
                else:
                    # 设置游戏模式并开始游戏
                    GameStateManager().set_game_state(GameState.PLAYING)
                    GameModeManager().switch_mode(mode)
