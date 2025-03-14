import pygame
from client.src.config.settings import GRAY

class Text:
    def __init__(self, text, size=40):
        # 创建字体对象
        # - 'fangsong': 字体名称，使用仿宋字体
        # - 40: 字体大小（像素）
        # - True: 是否加粗 (bold)
        self.font = pygame.font.SysFont('fangsong', size, True)

        # 渲染文本为图像
        # - text: 要渲染的文本内容
        # - True: 是否使用抗锯齿(antialiasing)，使文字更平滑
        # - GRAY: 文字颜色，使用灰色
        # 返回一个 Surface 对象，包含渲染后的文本图像
        self.str_image = self.font.render(text, True, GRAY)

        # 获取碰撞器
        self.str_rect = self.str_image.get_rect()