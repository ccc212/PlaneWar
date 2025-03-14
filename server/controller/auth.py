from flask import Blueprint, request, jsonify
from server.service.auth import AuthService
from server.domain.dto.auth_dto import LoginDTO, RegisterDTO
from server.domain.dto.common_dto import Result

# 创建认证蓝图
auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

# 注册
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        register_request = RegisterDTO(**data)
        register_data = auth_service.register(register_request)
        return jsonify(vars(Result.success(
            data=register_data,
            msg='注册成功'
        )))
    except ValueError as e:
        return jsonify(vars(Result.error(str(e)))), 400

# 登录
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        login_request = LoginDTO(**data)
        login_data = auth_service.login(login_request)
        return jsonify(vars(Result.success(
            data=login_data,
            msg='登录成功'
        )))
    except ValueError as e:
        return jsonify(vars(Result.error(str(e), 401))), 401