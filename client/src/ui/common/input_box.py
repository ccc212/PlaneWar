import pygame
from client.src.config.settings import BLACK, WHITE, GRAY

class InputBox:
    def __init__(self, x, y, w, h, placeholder, is_password=False):
        # 创建输入框的矩形区域
        self.rect = pygame.Rect(x, y, w, h)
        # 设置输入框边框颜色
        self.color = BLACK
        # 初始化输入文本为空
        self.text = ''
        # 设置占位符文本
        self.placeholder = placeholder
        # 创建字体对象,使用仿宋字体,大小30
        self.font = pygame.font.SysFont('fangsong', 30)
        # 是否为密码输入框
        self.is_password = is_password
        # 输入框是否处于激活状态
        self.active = False
        
    def handle_click(self, pos):
        # 检查点击位置是否在输入框内
        if self.rect.collidepoint(pos):
            self.active = True
        else:
            self.active = False
            
    def handle_event(self, event):
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # 删除最后一个字符
                self.text = self.text[:-1]
            else:
                # 添加新字符
                self.text += event.unicode

    def draw(self, screen):
        # 绘制输入框背景
        pygame.draw.rect(screen, WHITE, self.rect, 0)
        # 绘制输入框边框
        pygame.draw.rect(screen, self.color, self.rect, 2)
        
        # 绘制文本
        if self.text:
            # 如果是密码框则显示星号,否则显示实际文本
            text = '*' * len(self.text) if self.is_password else self.text
            text_surface = self.font.render(text, True, self.color)
        else:
            # 如果没有输入文本则显示占位符
            text_surface = self.font.render(self.placeholder, True, GRAY)
            
        # 将文本绘制到屏幕上,位置在输入框内部偏移5像素
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))