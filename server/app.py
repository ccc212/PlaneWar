from flask import Flask
from server import db
from controller.auth import auth_bp
from controller.leaderboard import leaderboard_bp
from config.config import Config


def create_app():
    # 创建Flask应用实例
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(Config)

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图，设置URL前缀
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(leaderboard_bp, url_prefix='/leaderboard')

    return app


if __name__ == '__main__':
    app = create_app()
    # 以调试模式运行服务器
    app.run(debug=True)