class Button:
    def __init__(self, screen, text, font, color, center):
        # 保存按钮的基本属性
        self.screen = screen
        self.text = text
        self.font = font
        self.color = color
        
        # 渲染文本生成图像
        self.image = self.font.render(text, True, color)
        # 获取图像的矩形区域
        self.rect = self.image.get_rect()
        # 设置按钮位置
        self.rect.center = center
        
    def draw(self):
        # 在屏幕上绘制按钮
        self.screen.blit(self.image, self.rect)
        
    def update_text(self, text):
        # 更新按钮文本
        self.text = text
        # 重新渲染文本图像
        self.image = self.font.render(text, True, self.color)
        # 保存当前中心点位置
        center = self.rect.center
        # 获取新图像的矩形区域
        self.rect = self.image.get_rect()
        # 保持按钮位置不变
        self.rect.center = center