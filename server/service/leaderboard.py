from typing import List, Dict
from server.domain.models.user import User
from server import db
from server.domain.vo.leaderboard_vo import TopScoreVO


class LeaderboardService:
    # 更新用户分数
    def update_score(self, data: dict) -> bool:
        # 参数校验
        user_id = data.get('user_id')
        score = data.get('score')
        
        if not score:
            raise ValueError('分数不能为空')
            
        # 查找用户
        user = User.query.get(user_id)
        if not user:
            raise ValueError('用户不存在')
            
        # 只有超过最高分才更新
        if score > user.highest_score:
            user.highest_score = score
            db.session.commit()
            return True
            
        return False

    # 获取排行榜
    def get_top_scores(self, limit: int = 10) -> List[TopScoreVO]:
        # 参数校验
        if limit < 1:
            raise ValueError('limit必须大于0')
            
        # 查询前N名玩家
        top_users = User.query.order_by(
            User.highest_score.desc()
        ).limit(limit).all()

        return [TopScoreVO(
            username=user.username,
            score=user.highest_score,
            rank=index + 1
        ) for index, user in enumerate(top_users)]

    # 获取指定用户的排名信息
    def get_user_rank(self, user_id: int) -> Dict:
        user = User.query.get(user_id)
        if not user:
            raise ValueError('用户不存在')
            
        # 计算用户排名
        rank = User.query.filter(
            User.highest_score > user.highest_score
        ).count() + 1
        
        return {
            'username': user.username,
            'score': user.highest_score,
            'rank': rank
        }