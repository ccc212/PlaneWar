from functools import wraps
from flask import request, jsonify
from ..config.config import Config
import jwt

from ..domain.dto.common_dto import Result


# 创建JWT令牌
def create_token(user_id, username):
    return jwt.encode(
        {
            'user_id': user_id,
            'username': username
         },
        Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

# 检查JWT令牌
def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 获取请求头中的token
        token = request.headers.get('Authorization')

        # 验证token是否存在
        if not token:
            return jsonify(vars(Result.error('缺少认证token'))), 401

        try:
            # 解析token
            token = token.split(' ')[1]  # Bearer token
            data = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=[Config.JWT_ALGORITHM]
            )
            request.user_id = data['user_id']
            request.username = data['username']
        except:
            return jsonify(vars(Result.error('无效的token'))), 401
        return f(*args, **kwargs)
    return decorated