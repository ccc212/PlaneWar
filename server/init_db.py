from app import create_app
from server import db

# 初始化数据库
def init_database():
    app = create_app()
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("数据库初始化成功！")

if __name__ == "__main__":
    init_database()