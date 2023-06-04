from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from Entities.Base import Base

class Player(Base):
    __tablename__ = 'player'

    player_id = Column(Integer, primary_key=True)
    nickname = Column(Text)
    player_server = Column(Text)
    rank_solo = Column(Text)
    league_points = Column(Integer)
    last_update = Column(TIMESTAMP)