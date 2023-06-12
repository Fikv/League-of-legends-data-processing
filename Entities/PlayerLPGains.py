from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from Entities.Base import Base
from Entities.Player import Player
from sqlalchemy.orm import relationship

class PlayerLPGains(Base):
    __tablename__ = 'player_lp_gains'

    player_id = Column(Integer, ForeignKey('player.player_id'), primary_key=True)
    date_of_update = Column(TIMESTAMP, primary_key=True)
    amount_of_lps = Column(Integer)

    player = relationship('Player')

    def __init__(self, player_id, date_of_update, amount_of_lps):
        self.player_id = player_id
        self.date_of_update = date_of_update
        self.amount_of_lps = amount_of_lps
