import copy

import pygame

from client.src.config.settings import BLACK, WHITE
from client.src.enums.game_state import MenuState, GameState
from client.src.managers.settings_manager import SettingsManager
from client.src.managers.state_manager import GameStateManager
from client.src.ui.common.message_dialog import MessageDialog


class SetDialog:
    def __init__(self, screen, before_state=None):
        # 初始化
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.before_state = before_state

        # 对话框尺寸和位置
        dialog_width = 400
        dialog_height = 700
        self.rect = pygame.Rect(
            (self.screen_rect.centerx - dialog_width // 2,
             self.screen_rect.centery - dialog_height // 2),
            (dialog_width, dialog_height)
        )

        # 创建消息对话框
        self.message_dialog = MessageDialog(screen)

        # 字体
        self.set_options_font = pygame.font.SysFont('fangsong', 30)
        self.set_options_bold_font = pygame.font.SysFont('fangsong', 35, True)

        # 设置选项
        self.set_options = [
            '按键设置',
            '音乐设置',
            '返回'
        ]

        # 按键设置
        self.keyboard_options = [
            ('前进', self.rect.left + 20),
            ('后退', self.rect.left + 20),
            ('左移', self.rect.left + 20),
            ('右移', self.rect.left + 20),
            ('暂停', self.rect.left + 20),
            ('射击', self.rect.left + 20)
        ]

        # 从设置管理器加载按键值
        keyboard_settings = SettingsManager().get_keyboard_settings()
        self.keyboard_values = [
            keyboard_settings['up'],
            keyboard_settings['down'],
            keyboard_settings['left'],
            keyboard_settings['right'],
            keyboard_settings['pause'],
            keyboard_settings['shoot']
        ]
        self.keyboard_values_temp = copy.deepcopy(self.keyboard_values)

        # 当前选中的设置项
        self.current_option = None
        # 当前正在设置的按键
        self.setting_key = False

    def draw(self):
        # 绘制对话框背景
        pygame.draw.rect(self.screen, WHITE, self.rect)
        pygame.draw.rect(self.screen, BLACK, self.rect, 2)
        
        # 绘制标题
        title = self.set_options_bold_font.render('设置', True, BLACK)
        title_rect = title.get_rect(centerx=self.rect.centerx, top=self.rect.top + 20)
        self.screen.blit(title, title_rect)

        # 绘制按键设置
        if self.current_option == 'keyboard':
            # 绘制按键设置内容
            self.draw_keyboard_settings(self.rect.top + 80)

            # 绘制保存按钮
            save_text = self.set_options_font.render('保存', True, BLACK)
            self.save_rect = save_text.get_rect(
                right=self.rect.right - 120,
                top=self.rect.top + 360
            )
            self.screen.blit(save_text, self.save_rect)

            # 绘制返回按钮
            back_text = self.set_options_font.render('返回', True, BLACK)
            self.back_rect = back_text.get_rect(
                right=self.rect.right - 20,
                top=self.rect.top + 360
            )
            self.screen.blit(back_text, self.back_rect)
        else:
            # 绘制主设置选项
            self.draw_main_options()

    # 绘制主设置选项
    def draw_main_options(self):
        start_y = self.rect.top + 80
        for i, option in enumerate(self.set_options):
            text = self.set_options_font.render(option, True, BLACK)
            if option == '返回':
                # 返回按钮靠右对齐
                rect = text.get_rect(
                    right=self.rect.right - 20,
                    top=start_y + i * 50
                )
            else:
                # 其他选项靠左对齐
                rect = text.get_rect(
                    left=self.rect.left + 20,
                    top=start_y + i * 50
                )
            self.screen.blit(text, rect)

    # 绘制按键设置
    def draw_keyboard_settings(self, start_y):
        for i, ((action, x), key) in enumerate(zip(self.keyboard_options, self.keyboard_values_temp)):
            # 绘制动作名称
            text = self.set_options_font.render(action, True, BLACK)
            rect = text.get_rect(left=x, top=start_y + i * 40)
            self.screen.blit(text, rect)
            
            # 绘制按键值
            key_name = pygame.key.name(key).upper()
            if self.setting_key and i == self.setting_key_index:
                key_text = self.set_options_font.render('请按键...', True, BLACK)
            else:
                key_text = self.set_options_font.render(key_name, True, BLACK)
            key_rect = key_text.get_rect(left=x + 150, top=start_y + i * 40)
            self.screen.blit(key_text, key_rect)
            
    def handle_click(self, pos):
        if not self.rect.collidepoint(pos):
            return

        # 处理按键设置界面的点击
        if self.current_option == 'keyboard':
            # 检查是否点击了返回按钮
            if self.back_rect.collidepoint(pos):
                self.keyboard_values_temp = copy.deepcopy(self.keyboard_values)
                self.current_option = None
                return

            # 检查是否点击了保存按钮
            if self.save_rect.collidepoint(pos):
                # 保存设置
                self.keyboard_values = copy.deepcopy(self.keyboard_values_temp)
                keyboard_settings = {
                    'up': self.keyboard_values[0],
                    'down': self.keyboard_values[1],
                    'left': self.keyboard_values[2],
                    'right': self.keyboard_values[3],
                    'pause': self.keyboard_values[4],
                    'shoot': self.keyboard_values[5]
                }
                SettingsManager().update_keyboard_settings(keyboard_settings)
                self.current_option = None
                return

            # 检查是否点击了具体按键
            start_y = self.rect.top + 80
            for i in range(len(self.keyboard_options)):
                if (self.rect.left + 150 <= pos[0] <= self.rect.left + 250 and
                    start_y + i * 40 <= pos[1] <= start_y + (i + 1) * 40):
                    self.setting_key = True
                    self.setting_key_index = i
                    return
        else:
            # 处理主设置界面的点击
            start_y = self.rect.top + 80
            for i, option in enumerate(self.set_options):
                if option == '返回':
                    # 返回按钮的点击检测
                    if (self.rect.right - 100 <= pos[0] <= self.rect.right - 20 and
                        start_y + i * 50 <= pos[1] <= start_y + (i + 1) * 50):
                        if self.before_state:
                            if isinstance(self.before_state, MenuState):
                                GameStateManager().set_menu_state(self.before_state)
                            elif isinstance(self.before_state, GameState):
                                GameStateManager().set_game_state(self.before_state)
                        return
                else:
                    # 其他选项的点击检测
                    if (self.rect.left + 20 <= pos[0] <= self.rect.left + 200 and
                        start_y + i * 50 <= pos[1] <= start_y + (i + 1) * 50):
                        if option == '按键设置':
                            self.current_option = 'keyboard'
                        # TODO: 处理其他选项
                        return

    def handle_keydown(self, event):
        if self.setting_key:
            self.keyboard_values_temp[self.setting_key_index] = event.key
            self.setting_key = False