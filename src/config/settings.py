# 游戏基础设置
FPS = 60 # 帧率
BULLET_NUM = 30 # 玩家子弹总数

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)

# 速度设置
PLAYER_SPEED = 5 # 玩家速度
ENEMY_SPEEDS = {
    "enemy1": 1,
    "enemy2": 2,
    "enemy3": 3,
    "enemy4": 1,
    "enemy5": 1
}

# 游戏参数
ENEMIES_TOTAL = 10
CHARACTER_HP = 3

# 屏幕设置
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000

# 子弹速度
BULLET_SPEEDS = {
    "character1": 3,
    "character2": 2,
    "character3": 10,
    "enemy": 5
}

# 资源路径
RESOURCE_PATH = "../resources"
HIGHEST_SCORE_FILE = f"{RESOURCE_PATH}/highest_score.txt"