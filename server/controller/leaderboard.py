from flask import Blueprint, request, jsonify

from server.domain.dto.common_dto import Result
from server.service.leaderboard import LeaderboardService
from server.utils.jwt_util import jwt_required

# 创建排行榜蓝图
leaderboard_bp = Blueprint('leaderboard', __name__)
leaderboard_service = LeaderboardService()

# 更新分数
@leaderboard_bp.route('/update', methods=['PUT'])
@jwt_required  # 需要JWT认证
def update_score():
    data = request.get_json()

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
    limit = request.args.get('limit', 10, type=int)
    try:
        scores = leaderboard_service.get_top_scores(limit)
    except ValueError as e:
        return jsonify(vars(Result.error(str(e)))), 400
    return jsonify(Result.success(
        data=scores
    ))

# 获取最高分数
@leaderboard_bp.route('/highest', methods=['GET'])
def get_highest_score():
    score = leaderboard_service.get_highest_score()
    return jsonify(Result.success(
        data=score
    ))

# 获取指定用户的最高分数
@leaderboard_bp.route('/user/<string:username>', methods=['GET'])
def get_user_highest_score(username):
    score = leaderboard_service.get_user_highest_score(username)
    return jsonify(Result.success(
        data=score
    ))

