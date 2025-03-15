from dataclasses import dataclass

@dataclass
class TopScoreVO:
    username: str
    score: int
    rank: int