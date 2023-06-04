from sqlalchemy import DateTime, ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Create the engine and session
engine = create_engine('postgresql://postgres:postgres@localhost:5432/lol_data3')
Session = sessionmaker(bind=engine)
session = Session()

# Declare the base class for table mapping
Base = declarative_base()

# Define the PLAYER and PLAYER_RIOT_ACCOUNT_DATA table models
class Player(Base):
    __tablename__ = 'player'

    player_id = Column(Integer, primary_key=True)
    nickname = Column(String)
    player_server = Column(String)
    rank_solo = Column(String)
    league_points = Column(Integer)
    last_update = Column(DateTime)
    riot_account = relationship("PlayerRiotAccountData", back_populates="player")  # Add this relationship

class PlayerRiotAccountData(Base):
    __tablename__ = 'player_riot_account_data'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.player_id'))
    account_id = Column(String)
    puuid = Column(String)
    player = relationship("Player", back_populates="riot_account")

# Create the tables if they don't exist
Base.metadata.create_all(engine)

# Add a new record to the tables
def add_player_riot_account(id,player_name, puuid):
    account_data = PlayerRiotAccountData(1, puuid=puuid)
    session.add(account_data)
    session.commit()
    print("Player Riot Account added successfully.")

# Modify an existing record in the tables
def modify_player_riot_account(player_id, new_account_id):
    account_data = session.query(PlayerRiotAccountData).filter_by(player_id=player_id).first()
    if account_data:
        account_data.account_id = new_account_id
        session.commit()
        print("Player Riot Account modified successfully.")
    else:
        print("Player Riot Account not found.")

# Usage example
add_player_riot_account("John", "123456", "abcxyz")
