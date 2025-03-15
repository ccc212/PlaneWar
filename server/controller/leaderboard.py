from flask import Blueprint, request, jsonify

from server.domain.dto.common_dto import Result
from server.service.leaderboard import LeaderboardService
from server.utils.jwt_util import jwt_required

# 创建排行榜蓝图
leaderboard_bp = Blueprint('leaderboard', __name__)
leaderboard_service = LeaderboardService()

# 更新分数
@leaderboard_bp.route('/score', methods=['POST'])
@jwt_required  # 需要JWT认证
def update_score():
    # 获取请求数据
    data = request.get_json()
    data['user_id'] = request.user_id  # 从JWT中获取用户ID
    
    try:
        updated = leaderboard_service.update_score(data)
        return jsonify({
            'msg': '分数更新成功',
            'new_highest': updated
        })
    except ValueError as e:
        return jsonify(vars(Result.error(str(e)))), 400

# 获取排行榜
@leaderboard_bp.route('/top', methods=['GET'])
def get_top_scores():
    # 获取请求参数
    limit = request.args.get('limit', 10, type=int)
    try:
        scores = leaderboard_service.get_top_scores(limit)
    except ValueError as e:
        return jsonify(vars(Result.error(str(e)))), 400
    return jsonify(Result.success(
        data=scores
    ))