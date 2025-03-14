from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from server import db


class User(db.Model):
    # 指定表名
    __tablename__ = 'user'

    # 定义数据库字段
    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名，唯一且不能为空
    password_hash = db.Column(db.String(255))  # 密码哈希
    highest_score = db.Column(db.Integer, default=0)  # 最高分
    created_time = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间

    # 将密码转换为哈希存储
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码是否正确
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)