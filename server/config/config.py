import os
from dotenv import load_dotenv


# 加载环境变量
load_dotenv()

class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 24 * 60 * 60  # 24小时
    JWT_ALGORITHM = 'HS256' # 密钥算法