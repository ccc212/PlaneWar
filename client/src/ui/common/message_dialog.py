import pygame
from client.src.config.settings import BLACK, WHITE, RED, SCREEN_WIDTH, SCREEN_HEIGHT
from client.src.ui.common.button import Button


class MessageDialog:
    def __init__(self, screen):
        # 获取屏幕实例
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # 对话框尺寸和位置
        self.width = 300
        self.height = 150
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 设置字体
        self.font = pygame.font.SysFont('fangsong', 24, True)

        # 创建确认按钮
        self.confirm_button = Button(
            self.screen,
            '确定',
            self.font,
            BLACK,
            (self.rect.centerx, self.rect.bottom - 30)
        )

        self.message = ""
        self.visible = False
        self.callback = None

    # 显示消息对话框
    def show(self, message, callback=None):
        self.message = message
        self.visible = True
        self.callback = callback

    # 隐藏消息对话框
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

        # 绘制对话框背景
        pygame.draw.rect(self.screen, WHITE, self.rect)
        pygame.draw.rect(self.screen, BLACK, self.rect, 2)

        # 绘制消息文本
        text_surface = self.font.render(self.message, True, RED)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.rect.centerx, self.rect.centery - 20)
        self.screen.blit(text_surface, text_rect)

        # 绘制确认按钮
        self.confirm_button.draw()

    # 处理点击事件
    def handle_click(self, pos):
        if not self.visible:
            return False

        if self.confirm_button.rect.collidepoint(pos):
            self.hide()
            return True

        return False