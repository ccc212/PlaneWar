from typing import List, Dict
from server.domain.models.user import User
from server import db
from server.domain.vo.leaderboard_vo import TopScoreVO
from sqlalchemy import text


class LeaderboardService:
    # 更新用户分数
    def update_score(self, data: dict) -> int:
        # 参数校验
        username = data.get('username')
        score = data.get('score')
        
        if not score:
            raise ValueError('分数不能为空')
            
        # 查找用户
        user = User.query.filter_by(username=username).first()
        if not user:
            raise ValueError('用户不存在')
            
        # 只有超过最高分才更新
        if int(score) > int(user.highest_score):
            user.highest_score = score
            db.session.commit()
            return score
        return 0

    # 获取排行榜
    def get_top_scores(self, limit: int = 10) -> List[TopScoreVO]:
        # 参数校验
        if limit < 1:
            raise ValueError('limit必须大于0')
            
        # 使用窗口函数查询前N名玩家
        sql = text("""
            SELECT username, highest_score, 
                   DENSE_RANK() OVER (ORDER BY highest_score DESC) as `rank`
            FROM user
            LIMIT :limit
        """)
        
        results = db.session.execute(sql, {'limit': limit}).fetchall()
        
        return [TopScoreVO(
            username=result.username,
            score=result.highest_score,
            rank=result.rank
        ) for result in results]

    # 根据用户名获取排行榜
    def get_user_scores(self, username):
        # 使用子查询确保窗口函数在过滤前计算排名
        sql = text("""
            WITH ranked_users AS (
                SELECT username, highest_score, 
                       DENSE_RANK() OVER (ORDER BY highest_score DESC) as `rank`
                FROM user
            )
            SELECT * FROM ranked_users
            WHERE username = :username
        """)
        
        result = db.session.execute(sql, {'username': username}).first()
        
        return TopScoreVO(
            username=result.username,
            score=result.highest_score,
            rank=result.rank
        ) if result else None

    # 获取最高分数
    def get_highest_score(self) -> int:
        user = User.query.order_by(
            User.highest_score.desc()
        ).first()
        return user.highest_score if user else 0

    # 获取指定用户的最高分数
    def get_user_highest_score(self, username: str):
        user = User.query.filter_by(username=username).first()
        return user.highest_score if user else 0