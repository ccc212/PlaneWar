import pygame

from client.src.config.settings import BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from client.src.enums.game_state import GameState, MenuState
from client.src.managers.state_manager import GameStateManager
from client.src.ui.common.button import Button
from client.src.ui.set_dialog.set_dialog import SetDialog


class PauseDialog:
    def __init__(self, screen):
        # 获取屏幕实例
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # 对话框尺寸和位置
        self.width = 150
        self.height = 220
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 设置字体
        self.font = pygame.font.SysFont('fangsong', 30, True)

        # 继续游戏按钮
        self.continue_button = Button(
            self.screen,
            '继续游戏',
            self.font,
            BLACK,
            (self.rect.centerx, self.rect.top + 40)
        )
 
        # 重新开始按钮
        self.restart_button = Button(
            self.screen,
            '重新开始',
            self.font,
            BLACK,
            (self.rect.centerx, self.rect.top + 90)
        )

        # 返回菜单按钮
        self.menu_button = Button(
            self.screen,
            '返回菜单',
            self.font,
            BLACK,
            (self.rect.centerx, self.rect.top + 140)
        )

        # 设置按钮
        self.set_button = Button(
            self.screen,
            '设置',
            self.font,
            BLACK,
            (self.rect.centerx, self.rect.top + 190)
        )

        self.visible = False
        self.callback = None
        self.set_dialog = SetDialog(self.screen, GameState.PAUSED)
        self.is_set = False

    # 显示暂停对话框
    def show(self, callback=None):
        self.visible = True
        self.callback = callback

    # 隐藏暂停对话框
    def hide(self):
        self.visible = False
        if self.callback:
            self.callback()
            self.callback = None

    # 绘制对话框
    def draw(self):
        if not self.visible:
            return

        # 绘制半透明背景
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))

        if not self.is_set:
            # 绘制暂停对话框
            pygame.draw.rect(self.screen, WHITE, self.rect)
            pygame.draw.rect(self.screen, BLACK, self.rect, 2)

            # 绘制按钮
            self.continue_button.draw()
            self.restart_button.draw()
            self.menu_button.draw()
            self.set_button.draw()
        else:
            # 绘制设置对话框
            self.set_dialog.draw()

    # 返回是否重新开始游戏
    def handle_click(self, pos):
        if not self.visible:
            return False

        if self.is_set:
            # 处理设置对话框的点击
            self.set_dialog.handle_click(pos)
            # 如果设置对话框返回到主界面，则回到暂停对话框
            if self.set_dialog.current_option is None:
                self.is_set = False
        else:
            # 处理暂停对话框的点击
            if self.continue_button.rect.collidepoint(pos):
                self.hide()
                GameStateManager().set_game_state(GameState.PLAYING)
            elif self.restart_button.rect.collidepoint(pos):
                self.hide()
                return True
            elif self.menu_button.rect.collidepoint(pos):
                self.hide()
                GameStateManager().set_game_state(GameState.NOT_STARTED)
            elif self.set_button.rect.collidepoint(pos):
                self.is_set = True

        return False