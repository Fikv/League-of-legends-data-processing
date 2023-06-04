from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.orm import relationship
from Entities.Base import Base

class MatchParticipants(Base):
    __tablename__ = 'match_participants'

    match_id = Column(Text, ForeignKey('matches.match_id'), primary_key=True)
    top_b = Column(Text)
    jung_b = Column(Text)
    mid_b = Column(Text)
    adc_b = Column(Text)
    support_b = Column(Text)
    top_r = Column(Text)
    jung_r = Column(Text)
    mid_r = Column(Text)
    adc_r = Column(Text)
    support_r = Column(Text)

    match = relationship("Matches", backref="match_participants")
