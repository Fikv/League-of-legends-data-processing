from sqlalchemy import Column, Integer, String, ForeignKey
from Entities.Base import Base
from Entities.Player import Player
from sqlalchemy.orm import relationship


class PlayerRiotAccountData(Base):
    __tablename__ = 'player_riot_account_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id_fk = Column(Integer, ForeignKey('player.player_id'))
    player_id = Column(String)
    account_id = Column(String)
    puuid = Column(String)
    
    player = relationship('Player')

    def __init__(self,player_id ,account_id, puuid):
        self.player_id = player_id
        self.account_id = account_id
        self.puuid = puuid