# 后端调用的URL
API_BASE_URL = 'http://localhost:5428'

# 游戏基础设置
FPS = 60  # 帧率
BULLET_NUM = 20  # 玩家子弹总数

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
RED = (255, 0, 0)

# 速度设置
PLAYER_SPEED = 5  # 玩家飞行速度
ENEMY_SPEEDS = {  # 敌人飞行速度
    "enemy1": 1,
    "enemy2": 2,
    "enemy3": 3,
    "enemy4": 1,
    "enemy5": 1
}

# 游戏参数
ENEMIES_TOTAL = 10  # 敌人总数
PLAYER_HP = 3  # 玩家生命值

# 屏幕设置
SCREEN_WIDTH = 1920  # 屏幕宽度
SCREEN_HEIGHT = 1080  # 屏幕高度

# 子弹速度
BULLET_SPEEDS = {
    "bullet1": 5,
    "bullet2": 4,
    "bullet3": 12,
    "enemy": 5
}

# 资源路径
RESOURCE_PATH = "../resources"
HIGHEST_SCORE_FILE = f"{RESOURCE_PATH}/highest_score.txt"
