from server.domain.models.user import User
from server import db
from server.utils.jwt_util import create_token
from server.domain.dto.auth_dto import LoginDTO,RegisterDTO
from server.domain.vo.auth_vo import LoginVO,RegisterVO


class AuthService:
    # 注册
    def register(self, data: RegisterDTO) -> RegisterVO:
        # 检查用户名是否已存在
        if User.query.filter_by(username=data.username).first():
            raise ValueError('用户名已存在')

        # 创建新用户
        user = User()
        user.username = data.username
        user.set_password(data.password)

        # 保存到数据库
        db.session.add(user)
        db.session.commit()

        return RegisterVO(user_id=user.id)

    # 登录
    def login(self, data: LoginDTO) -> LoginVO:
        # 查找用户
        user = User.query.filter_by(username=data.username).first()
        if not user:
            raise ValueError('用户不存在')

        # 验证密码
        if not user.check_password(data.password):
            raise ValueError('密码错误')

        # 生成token
        token = create_token(user.id)

        return LoginVO(
            token=token,
            username=user.username,
            user_id=user.id
        )