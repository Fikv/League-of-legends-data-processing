from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from Entities.Base import Base

class Player(Base):
    __tablename__ = 'player'

    player_id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(Text)
    player_server = Column(Text)
    rank_solo = Column(Text)
    league_points = Column(Integer)
    last_update = Column(TIMESTAMP)

    def __init__(self, nickname, player_server, rank_solo, league_points, last_update):
        self.nickname = nickname
        self.player_server = player_server
        self.rank_solo = rank_solo
        self.league_points = league_points
        self.last_update = last_update

    @classmethod
    def from_dict(cls, player_dict):
        return cls(
            nickname=player_dict.get('nickname'),
            player_server=player_dict.get('player_server'),
            rank_solo=player_dict.get('rank_solo'),
            league_points=player_dict.get('league_points'),
            last_update=player_dict.get('last_update')
        )    