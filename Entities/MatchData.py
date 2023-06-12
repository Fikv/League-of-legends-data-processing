from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, BigInteger, Decimal, ForeignKey
from Entities.Base import Base
from Entities.Player import Player
from sqlalchemy.orm import relationship


class MatchData(Base):
    __tablename__ = 'match_data'

    player_id = Column(Integer, ForeignKey('player.player_id'), primary_key=True)
    match_id = Column(String, primary_key=True)
    date_of_match = Column(TIMESTAMP)
    win = Column(Boolean)
    ranked_solo = Column(Boolean)
    ranked_duo = Column(Boolean)
    game_creation = Column(BigInteger)
    game_duration = Column(BigInteger)
    game_end_timestamp = Column(BigInteger)
    game_mode = Column(String)
    game_start_timestamp = Column(BigInteger)
    game_type = Column(String)
    map_id = Column(Integer)
    earliest_baron = Column(Decimal)
    detector_wards_placed = Column(Integer)
    first_blood_kill = Column(Boolean)
    enemy_missing_ping = Column(Integer)
    vision_score = Column(Integer)
    ward_placed = Column(Integer)
    assists_me_pings = Column(Integer)
    baron_kills = Column(Integer)
    dragon_kills = Column(Integer)
    herald_kills = Column(Integer)
    first_turret = Column(Boolean)
    control_wards_placed = Column(Integer)
    team_id = Column(String)

    player = relationship('Player')

    def __init__(self, player_id, match_id, date_of_match, win, ranked_solo, ranked_duo, game_creation,
                 game_duration, game_end_timestamp, game_mode, game_start_timestamp, game_type, map_id,
                 earliest_baron, detector_wards_placed, first_blood_kill, enemy_missing_ping, vision_score,
                 ward_placed, assists_me_pings, baron_kills, dragon_kills, herald_kills, first_turret,
                 control_wards_placed, team_id):
        self.player_id = player_id
        self.match_id = match_id
        self.date_of_match = date_of_match
        self.win = win
        self.ranked_solo = ranked_solo
        self.ranked_duo = ranked_duo
        self.game_creation = game_creation
        self.game_duration = game_duration
        self.game_end_timestamp = game_end_timestamp
        self.game_mode = game_mode
        self.game_start_timestamp = game_start_timestamp
        self.game_type = game_type
        self.map_id = map_id
        self.earliest_baron = earliest_baron
        self.detector_wards_placed = detector_wards_placed
        self.first_blood_kill = first_blood_kill
        self.enemy_missing_ping = enemy_missing_ping
        self.vision_score = vision_score
        self.ward_placed = ward_placed
        self.assists_me_pings = assists_me_pings
        self.baron_kills = baron_kills
        self.dragon_kills = dragon_kills
        self.herald_kills = herald_kills
        self.first_turret = first_turret
        self.control_wards_placed = control_wards_placed
        self.team_id = team_id
