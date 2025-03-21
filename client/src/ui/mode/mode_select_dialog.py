import pygame
from client.src.config.settings import BLACK, WHITE
from client.src.enums.game_mode_type import GameModeType
from client.src.ui.common.button import Button


class ModeSelectDialog:
    def __init__(self, screen):
        # 获取屏幕尺寸
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 对话框尺寸和位置
        self.width = 400
        self.height = 500
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 设置字体
        self.title_font = pygame.font.SysFont('fangsong', 40, True)
        self.button_font = pygame.font.SysFont('fangsong', 30, True)

        # 创建按钮
        button_y = self.rect.top + 100
        button_spacing = 80

        self.endless_button = Button(
            screen=screen,
            text='无尽模式',
            font=self.button_font,
            color=BLACK,
            center=(self.rect.centerx, button_y)
        )

        self.level_button = Button(
            screen=screen,
            text='关卡模式',
            font=self.button_font,
            color=BLACK,
            center=(self.rect.centerx, button_y + button_spacing)
        )

        self.roguelike_button = Button(
            screen=screen,
            text='肉鸽模式',
            font=self.button_font,
            color=BLACK,
            center=(self.rect.centerx, button_y + button_spacing * 2)
        )

        self.back_button = Button(
            screen=screen,
            text='返回',
            font=self.button_font,
            color=BLACK,
            center=(self.rect.centerx, button_y + button_spacing * 3)
        )

        # 模式描述
        self.descriptions = {
            GameModeType.ENDLESS: "无尽模式：敌人无限生成，难度逐渐提升，看你能坚持多久！",
            GameModeType.LEVEL: "关卡模式：通过精心设计的关卡，挑战不同的敌人组合！",
            GameModeType.ROGUELIKE: "肉鸽模式：每次游戏随机生成不同的能力和敌人，体验不一样的挑战！"
        }

        # 当前选中的模式
        self.selected_mode = None

    def draw(self):
        # 绘制半透明背景
        s = pygame.Surface((self.screen_rect.width, self.screen_rect.height))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))

        # 绘制对话框背景
        pygame.draw.rect(self.screen, WHITE, self.rect)
        pygame.draw.rect(self.screen, BLACK, self.rect, 2)

        # 绘制标题
        title = self.title_font.render('选择游戏模式', True, BLACK)
        title_rect = title.get_rect(centerx=self.rect.centerx, top=self.rect.top + 30)
        self.screen.blit(title, title_rect)

        # 绘制按钮
        self.endless_button.draw()
        self.level_button.draw()
        self.roguelike_button.draw()
        self.back_button.draw()

    def handle_click(self, pos):
        if not self.rect.collidepoint(pos):
            return None

        if self.endless_button.rect.collidepoint(pos):
            self.selected_mode = GameModeType.ENDLESS
            return GameModeType.ENDLESS
        elif self.level_button.rect.collidepoint(pos):
            self.selected_mode = GameModeType.LEVEL
            return GameModeType.LEVEL
        elif self.roguelike_button.rect.collidepoint(pos):
            self.selected_mode = GameModeType.ROGUELIKE
            return GameModeType.ROGUELIKE
        elif self.back_button.rect.collidepoint(pos):
            return "back"

        return None

    def handle_mouse_motion(self, pos):
        self.draw()

        # 如果有选中的模式，显示描述
        if (self.endless_button.rect.collidepoint(pos)
                or self.level_button.rect.collidepoint(pos)
                or self.roguelike_button.rect.collidepoint(pos)):
            desc_font = pygame.font.SysFont('fangsong', 20)
            desc_text = self.descriptions.get(self.selected_mode, "")

            # 自动换行显示描述文本
            words = desc_text.split(' ')
            lines = []
            line = ""
            for word in words:
                test_line = line + word + " "
                if desc_font.size(test_line)[0] < self.width - 40:
                    line = test_line
                else:
                    lines.append(line)
                    line = word + " "
            lines.append(line)

            # 绘制描述文本
            for i, line in enumerate(lines):
                text = desc_font.render(line, True, BLACK)
                self.screen.blit(text, (self.rect.left + 20, self.rect.bottom - 80 + i * 25))
