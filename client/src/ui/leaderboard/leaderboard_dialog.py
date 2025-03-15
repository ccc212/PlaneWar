import pygame
import requests

from client.src.config.settings import BLACK, WHITE, API_BASE_URL


class LeaderboardDialog:
    def __init__(self, screen):
        # 初始化
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 对话框尺寸和位置
        dialog_width = 400
        dialog_height = 500
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

    def fetch_leaderboard(self):
        """获取排行榜数据"""
        try:
            response = requests.get(f'{API_BASE_URL}/leaderboard/top')
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 200:
                    self.leaderboard_data = data['data']
        except:
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
            (self.rect.left, header_y + 40),
            (self.rect.right, header_y + 40),
            1
        )
        
        # 绘制排行榜数据
        start_y = header_y + 60
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

    def handle_click(self, pos):
        """处理点击事件"""
        if self.close_rect.collidepoint(pos):
            return 'close'
        return None