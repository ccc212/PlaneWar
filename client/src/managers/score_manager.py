from client.src.config.settings import API_BASE_URL
from client.src.managers.auth_manager import AuthManager
from client.src.models.base import Screen
from client.src.ui.common.message_dialog import MessageDialog
from client.src.utils.http_client import HttpClient


class ScoreManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self._highest_score = None
        self.get_highest_score()
        self.screen = Screen().screen
        self.message_dialog = MessageDialog(self.screen)

    # 获取最高分
    def get_highest_score(self):
        if self._highest_score is None:
            try:
                response = HttpClient.get(f'{API_BASE_URL}/leaderboard/highest')
                self._highest_score = response.json()['data'] if response.status_code == 200 else 0
            except Exception as e:
                self.message_dialog.show(str(e))
                self._highest_score = 0
        return self._highest_score

    # 更新最高分
    def update_highest_score(self, current_score):
        if current_score > self._highest_score:
            self._highest_score = current_score
            username = AuthManager().get_username()
            if username is not None:
                try:
                    response = HttpClient.put(f'{API_BASE_URL}/leaderboard/update', {
                        'username': username,
                        'score': current_score
                    })
                    return response.json()['msg'] == '分数更新成功'
                except Exception as e:
                    self.message_dialog.show(str(e))
