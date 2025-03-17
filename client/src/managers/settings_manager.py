import json
import os

import pygame


class SettingsManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.settings_file = 'settings.json'
        self.default_settings = {
            'keyboard': {
                'up': pygame.K_w,
                'down': pygame.K_s,
                'left': pygame.K_a,
                'right': pygame.K_d,
                'pause': pygame.K_p,
                'shoot': pygame.K_SPACE
            }
        }
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            return self.default_settings.copy()
        except:
            return self.default_settings.copy()

    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(f"保存设置失败: {e}")

    def get_keyboard_settings(self):
        return self.settings.get('keyboard', self.default_settings['keyboard'])

    def update_keyboard_settings(self, key_settings):
        self.settings['keyboard'] = key_settings
        self.save_settings()