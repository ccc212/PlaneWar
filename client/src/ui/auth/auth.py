import pygame

from client.src.enums.game_state import MenuState
from client.src.managers.state_manager import GameStateManager
from client.src.ui.common.input_box import InputBox
from client.src.config.settings import BLACK, WHITE, API_BASE_URL
from client.src.ui.common.button import Button
import requests


class AuthDialog:
    def __init__(self, screen):
        # 初始化认证对话框
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 对话框尺寸和位置
        self.width = 400
        self.height = 300
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 设置字体
        self.font = pygame.font.SysFont('fangsong', 30, True)

        # 状态管理器
        self.state_manager = GameStateManager()

        # 创建用户名输入框
        self.username_input = InputBox(
            self.rect.left + 50,
            self.rect.top + 50,
            300,
            40,
            '用户名'
        )

        # 创建密码输入框
        self.password_input = InputBox(
            self.rect.left + 50,
            self.rect.top + 120,
            300,
            40,
            '密码',
            is_password=True
        )

        # 创建登录按钮
        self.login_button = Button(
            screen,
            '登录',
            self.font,
            BLACK,
            (self.rect.centerx - 80, self.rect.bottom - 50)
        )
        # 创建注册按钮
        self.register_button = Button(
            screen,
            '注册',
            self.font,
            BLACK,
            (self.rect.centerx + 80, self.rect.bottom - 50)
        )
        # 创建关闭按钮
        self.close_button = Button(
            screen,
            'X',
            self.font,
            BLACK,
            (self.rect.right - 20, self.rect.top + 20)
        )

    def draw(self):
        # 绘制对话框背景
        pygame.draw.rect(self.screen, WHITE, self.rect)
        pygame.draw.rect(self.screen, BLACK, self.rect, 2)

        # 绘制输入框和按钮
        self.username_input.draw(self.screen)
        self.password_input.draw(self.screen)
        self.login_button.draw()
        self.register_button.draw()
        self.close_button.draw()

    def handle_click(self, pos):
        # 点击关闭按钮
        if self.close_button.rect.collidepoint(pos):
            self.state_manager.set_menu_state(MenuState.MAIN)

        # 点击登录按钮
        if self.login_button.rect.collidepoint(pos):
            username = self._handle_login()
            self.state_manager.set_menu_state(MenuState.MAIN)
            return username

        # 点击注册按钮
        if self.register_button.rect.collidepoint(pos):
            username = self._handle_register()
            self.state_manager.set_menu_state(MenuState.MAIN)
            return username
            
        # 点击输入框
        self.username_input.handle_click(pos)
        self.password_input.handle_click(pos)

    def handle_event(self, event):
        # 只有当输入框激活时才处理键盘事件
        if self.username_input.active or self.password_input.active:
            self.username_input.handle_event(event)
            self.password_input.handle_event(event)

    def _handle_login(self):
        # 处理登录请求
        try:
            # 发送登录POST请求
            response = requests.post(
                f'{API_BASE_URL}/auth/login',
                json={
                    'username': self.username_input.text,
                    'password': self.password_input.text
                }
            )
            # 登录成功返回用户名
            if response.status_code == 200:
                return self.username_input.text
            else:
                # TODO: 显示错误信息
                return None
        except:
            # TODO: 显示网络错误
            return None
            
    def _handle_register(self):
        # 处理注册请求
        try:
            # 发送注册POST请求
            response = requests.post(
                f'{API_BASE_URL}/auth/register',
                json={
                    'username': self.username_input.text,
                    'password': self.password_input.text
                }
            )
            # 注册成功后自动登录
            if response.status_code == 200:
                return self._handle_login()
            else:
                # TODO: 显示错误信息
                return None
        except:
            # TODO: 显示网络错误
            return None