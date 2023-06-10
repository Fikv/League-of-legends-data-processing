
from Entities.Player import Player
from Entities.PlayerRiotAccountData import PlayerRiotAccountData
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class UserDataMapper:

    engine = create_engine('postgresql://postgres:postgres@localhost:5432/lol_data3')
    Session = sessionmaker(bind=engine)
    session = Session()

    def mapUserDataToTable(self, json, json2):
        riot_account = PlayerRiotAccountData(
            json['id'],
            json['accointId'],
            json['puuid']
        )
        
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S") 
        player = Player(
            json['name'],
            'EUNE',
            json2['tier'] + ' ' + json['rank'],
            json2['leaguePoints'],
            formatted_datetime
        )
        self.session.add(player)
        self.session.add(riot_account)
        self.session.commit()
        self.session.close()


    def __init__(self):
        engine = create_engine('postgresql://postgres:postgres@localhost:5432/lol_data3')
        Session = sessionmaker(bind=engine)
        session = Session()
