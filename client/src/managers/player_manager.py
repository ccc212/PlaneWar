import pygame

from client.src.config.settings import PLAYER_HP
from client.src.managers.auth_manager import AuthManager
from client.src.models.base import Screen
from client.src.models.player import Player


class PlayerManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance
    def _init(self):
        self.player_group = pygame.sprite.Group()
        self.players = {}  # 存储所有玩家对象，key 为用户名
        self.players_bullet_group = {}  # 键为用户名，值为子弹组
        guest_bullet_group = pygame.sprite.Group()
        self.players_bullet_group[AuthManager().GUEST] = guest_bullet_group

    def add_player(self, player_name, player: Player):
        self.player_group.add(player)
        self.players[player_name] = player

    def remove_player(self, player_name):
        if player_name in self.players:
            self.player_group.remove(self.players[player_name])
            del self.players[player_name]

    def clear_players(self):
        self.player_group.empty()
        self.players.clear()

    def update_players(self):
        for player in self.players.values():
            player.update()
        self.player_group.draw(Screen().screen)

    def get_player(self, player_name=None) -> Player:
        return self.players.get(player_name) if player_name else self.players.get(AuthManager().get_username())

    def init_player(self):
        for player in self.players.values():
            player.hp = PLAYER_HP
            player.live = True
            player.rect.midbottom = Screen().rect.midbottom

    def hurt_player(self):
        for player in self.players.values():
            player.hurt()

    def get_current_player_bullets(self):
        username = AuthManager().get_username()
        if username == None:
            return self.players_bullet_group.get(AuthManager().GUEST)
        return self.players_bullet_group.get(username)