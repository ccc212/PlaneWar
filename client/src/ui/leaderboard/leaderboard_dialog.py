import pygame
import requests

from client.src.config.settings import BLACK, WHITE, API_BASE_URL
from client.src.enums.game_state import MenuState
from client.src.managers.state_manager import GameStateManager
from client.src.managers.auth_manager import AuthManager
from client.src.ui.common.message_dialog import MessageDialog
from client.src.utils.http_client import HttpClient


class LeaderboardDialog:
    def __init__(self, screen):
        # 初始化
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 状态管理器
        self.state_manager = GameStateManager()

        # 对话框尺寸和位置
        dialog_width = 400
        dialog_height = 620
        self.rect = pygame.Rect(
            (self.screen_rect.centerx - dialog_width//2,
             self.screen_rect.centery - dialog_height//2),
            (dialog_width, dialog_height)
        )

        # 创建关闭按钮
        self.close_font = pygame.font.SysFont('fangsong', 30, True)
        self.close_text = self.close_font.render('×', True, BLACK)
        self.close_rect = self.close_text.get_rect()
        self.close_rect.topright = (self.rect.right - 10, self.rect.top + 10)

        # 标题
        self.title_font = pygame.font.SysFont('fangsong', 40, True)
        self.title_text = self.title_font.render('排行榜', True, BLACK)
        self.title_rect = self.title_text.get_rect()
        self.title_rect.centerx = self.rect.centerx
        self.title_rect.top = self.rect.top + 20

        # 表头
        self.header_font = pygame.font.SysFont('fangsong', 30, True)
        self.headers = [
            ('排名', self.rect.left + 20),
            ('用户名', self.rect.left + 120),
            ('分数', self.rect.right - 80)
        ]

        # 排行榜数据
        self.leaderboard_data = []
        self.item_font = pygame.font.SysFont('fangsong', 30)

        # 创建消息对话框
        self.message_dialog = MessageDialog(screen)

    def fetch_leaderboard(self):
        # 获取排行榜数据
        try:
            response = HttpClient.get(f'{API_BASE_URL}/leaderboard/top')
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 200:
                    self.leaderboard_data = data['data']
        except Exception as e:
            self.message_dialog.show(str(e))
            self.leaderboard_data = []

    def draw(self):
        # 绘制对话框背景
        pygame.draw.rect(self.screen, WHITE, self.rect)
        pygame.draw.rect(self.screen, BLACK, self.rect, 2)

        # 绘制标题
        self.screen.blit(self.title_text, self.title_rect)

        # 绘制关闭按钮
        self.screen.blit(self.close_text, self.close_rect)

        # 绘制表头
        header_y = self.rect.top + 80
        for header_text, x_pos in self.headers:
            text = self.header_font.render(header_text, True, BLACK)
            rect = text.get_rect()
            rect.left = x_pos
            rect.top = header_y
            self.screen.blit(text, rect)

        # 绘制分割线
        pygame.draw.line(
            self.screen,
            BLACK,
            (self.rect.left, header_y),
            (self.rect.right, header_y),
            1
        )

        # 绘制排行榜数据
        start_y = header_y + 60
        my_rank_data = None
        username = AuthManager().get_username()
        for item in self.leaderboard_data:
            # 排名
            rank_text = self.item_font.render(f"{item['rank']}", True, BLACK)
            rank_rect = rank_text.get_rect()
            rank_rect.left = self.rect.left + 20
            rank_rect.top = start_y

            # 用户名
            name_text = self.item_font.render(item['username'], True, BLACK)
            name_rect = name_text.get_rect()
            name_rect.left = self.rect.left + 120
            name_rect.top = start_y
            if item['username'] == username:
                # 存下我的排行榜数据
                my_rank_data = item

            # 分数
            score_text = self.item_font.render(str(item['score']), True, BLACK)
            score_rect = score_text.get_rect()
            score_rect.left = self.rect.right - 80
            score_rect.top = start_y

            # 绘制
            self.screen.blit(rank_text, rank_rect)
            self.screen.blit(name_text, name_rect)
            self.screen.blit(score_text, score_rect)

            start_y += 40

        # 绘制分割线
        pygame.draw.line(
            self.screen,
            BLACK,
            (self.rect.left, start_y),
            (self.rect.right, start_y),
            1
        )

        # 绘制我的排名
        start_y += 20
        if my_rank_data:
            # 排名
            rank_text = self.item_font.render(f"{my_rank_data['rank']}", True, BLACK)
            rank_rect = rank_text.get_rect()
            rank_rect.left = self.rect.left + 20
            rank_rect.top = start_y

            # 用户名
            name_text = self.item_font.render(my_rank_data['username'], True, BLACK)
            name_rect = name_text.get_rect()
            name_rect.left = self.rect.left + 120
            name_rect.top = start_y

            # 分数
            score_text = self.item_font.render(str(my_rank_data['score']), True, BLACK)
            score_rect = score_text.get_rect()
            score_rect.left = self.rect.right - 80
            score_rect.top = start_y

            # 绘制
            self.screen.blit(rank_text, rank_rect)
            self.screen.blit(name_text, name_rect)
            self.screen.blit(score_text, score_rect)
        else:
            # 未登录
            text = self.item_font.render('未登录', True, BLACK)
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.centerx
            text_rect.top = start_y
            self.screen.blit(text, text_rect)


    def handle_click(self, pos):
        # 处理点击事件
        if self.close_rect.collidepoint(pos):
            self.state_manager.set_menu_state(MenuState.MAIN)