from sqlalchemy import Column, Integer, Date, String, ForeignKey
from Entities.Base import Base
from Entities.Player import Player
from sqlalchemy.orm import relationship

class Match(Base):
    __tablename__ = 'matches'

    player_id = Column(Integer, ForeignKey('player.player_id'), primary_key=True)
    date_of_match = Column(Date, primary_key=True)
    match_id = Column(String)
    type_of_match = Column(String)

    player = relationship('Player')

    def __init__(self, player_id, date_of_match, match_id, type_of_match):
        self.player_id = player_id
        self.date_of_match = date_of_match
        self.match_id = match_id
        self.type_of_match = type_of_match
