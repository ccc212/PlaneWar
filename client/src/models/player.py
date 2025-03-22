from client.src.config.settings import PLAYER_SPEED, PLAYER_HP, BULLET_NUM, SCREEN_WIDTH, SCREEN_HEIGHT
from .base import GameObject
from .bullets import *


class Player(GameObject):
    def __init__(self, path, tilted_path, scale, speed=PLAYER_SPEED, hp=PLAYER_HP):
        super().__init__(path=path,
                         rotation=0,
                         scale=scale,
                         speed=speed,
                         hp=hp)
        # 发射状态
        self.fire = False

        # 上次发射时间
        self.last_shot_time = 0

        # 不同武器的发射间隔(毫秒)
        self.weapon_cooldowns = {
            1: {"primary": 500, "secondary": 1200},  # 主武器0.5秒，副武器1.2秒
            2: {"primary": 100},  # 0.1秒发射一次
            3: {"primary": 1000},  # 1秒发射一次
        }

        # 武器类型
        self.fire_kind = 1

        # 玩家子弹组
        self.bullets = pygame.sprite.Group()

        # 玩家移动状态
        self.mleft = self.mright = self.mup = self.mdown = False

        # 正常状态图片
        self.original_image = pygame.transform.rotozoom(
            pygame.image.load(path),
            0,
            scale
        )

        # 倾斜状态图片
        self.tilted_image = pygame.transform.rotozoom(
            pygame.image.load(tilted_path),
            0,
            scale
        )

    def update(self):
        # 在方法内部导入
        from ..managers.player_manager import PlayerManager

        self._handle_movement()

        if self.fire and len(PlayerManager().get_current_player_bullets()) < BULLET_NUM:
            self._handle_firing()

    def _handle_firing(self):
        # 在方法内部导入
        from ..managers.player_manager import PlayerManager

        current_time = pygame.time.get_ticks()
        weapon = self.weapon_cooldowns[self.fire_kind]

        # 主武器发射逻辑
        if current_time - self.last_shot_time >= weapon["primary"]:
            if self.fire_kind == 1:
                PlayerManager().get_current_player_bullets().add(PlayerBullet1(self))
            elif self.fire_kind == 2:
                PlayerManager().get_current_player_bullets().add(PlayerBullet1(self))
            elif self.fire_kind == 3:
                PlayerManager().get_current_player_bullets().add(PlayerBullet3(self))
            self.last_shot_time = current_time

        # 武器1的额外子弹
        if self.fire_kind == 1:
            if (current_time - self.last_shot_time) % weapon["secondary"] == 0:
                bullet2 = PlayerBullet2(self, 1)
                bullet3 = PlayerBullet2(self, -1)
                PlayerManager().get_current_player_bullets().add(bullet2, bullet3)

    # 玩家移动
    def _handle_movement(self):
        if self.mleft and self.rect.left > 0:
            self.rect.x -= self.speed
        if self.mright and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if self.mup and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.mdown and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def hurt(self):
        self.hp -= 1
        # TODO 无敌及闪烁效果

        if self.hp <= 0:
            self.live = False
