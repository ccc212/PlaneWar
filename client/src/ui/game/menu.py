import pygame

from client.src.config.settings import BLACK
from client.src.ui.auth.auth import AuthDialog
from client.src.ui.common.button import Button


class Menu:
    def __init__(self, screen):
        # 保存游戏主屏幕
        self.screen = screen
        # 获取屏幕矩形区域
        self.screen_rect = screen.get_rect()
        
        # 创建开始按钮字体
        self.play_font = pygame.font.SysFont('fangsong', 90, True)
        # 创建开始按钮,放在屏幕中央
        self.play_button = Button(
            screen=screen,
            text='开始',
            font=self.play_font,
            color=BLACK,
            center=self.screen_rect.center
        )
        
        # 创建用户状态按钮字体
        self.auth_font = pygame.font.SysFont('fangsong', 30, True)
        # 创建用户状态按钮,放在右上角
        self.auth_button = Button(
            screen=screen,
            text='未登录',
            font=self.auth_font,
            color=BLACK,
            center=(self.screen_rect.right - 100, 50)
        )
        
        # 创建登录对话框
        self.auth_dialog = AuthDialog(screen)
        # 控制是否显示登录对话框
        self.show_auth = False
        
        # 保存当前登录用户名
        self.username = None
        
    def draw(self):
        if not self.show_auth:
            # 如果未登录显示"未登录",否则显示用户名
            if not self.username:
                self.auth_button.update_text('未登录')
            else:
                self.auth_button.update_text(self.username)
            # 绘制用户状态按钮和开始按钮
            self.auth_button.draw()
            self.play_button.draw()
        else:
            # 显示登录对话框
            self.auth_dialog.draw()
            
    def handle_click(self, pos):
        if self.show_auth:
            # 处理登录对话框的点击
            result = self.auth_dialog.handle_click(pos)
            if result:
                if result == 'close':
                    # 点击关闭按钮,关闭对话框
                    self.show_auth = False
                elif isinstance(result, str):
                    # 登录成功,保存用户名并关闭对话框
                    self.username = result
                    self.show_auth = False
        else:
            # 点击用户状态按钮,显示登录对话框
            if self.auth_button.rect.collidepoint(pos):
                self.show_auth = True
            # 返回是否点击了开始按钮
            return self.play_button.rect.collidepoint(pos)
        return False