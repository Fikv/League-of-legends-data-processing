import pyodbc
import sys
from azure_database.get_data import GET_DATA
import datetime
import json
import datetime


class UPLOAD_DATA:
    def __init__(self):
        # Konfiguracja połączenia do bazy danych
        self.riot_key = 'RGAPI-f00bd7c6-e730-44f0-849d-6ae3f8f8bc6e'
        self.server = 'domino403.database.windows.net'
        self.database = 'lol-data-analise'
        self.username = 'domino403'
        self.password = 'Debica2001'
        self.driver = '{ODBC Driver 18 for SQL Server}'  # Upewnij się, że masz zainstalowany sterownik ODBC odpowiedni dla Twojego systemu, jeśli nie to pobierz go z linku poniżej
        # https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15
        # Tworzenie łańcucha połączenia
        self.connection_string = f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"

    def open_connection(self):
        # Nawiązanie połączenia z bazą danych
        self.conn = pyodbc.connect(self.connection_string)
        # Utworzenie kursora
        self.cursor = self.conn.cursor()
    def close_connection(self):
        # Zakończenie połączenia
        self.cursor.close()
        self.conn.close()

    def check_user_existence(self, id):
        self.open_connection()
        query = '''
                SELECT CASE WHEN EXISTS (
                    SELECT 1 FROM PLAYER WHERE PLAYER_ID = ?
                ) THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END AS PlayerExists
                '''
        self.cursor.execute(query,id)
        self.result = self.cursor.fetchone()
        player_exists = bool(self.result[0])
        self.close_connection()
        return player_exists


    def check_player_account_existence(self, id):
        self.open_connection()
        query = '''
                SELECT CASE WHEN EXISTS (
                    SELECT 1 FROM PLAYER_RIOT_ACCOUNT_DATA WHERE PLAYER_ID = ?
                ) THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END AS PlayerExists
                '''
        self.cursor.execute(query, id)
        self.result = self.cursor.fetchone()
        player_exists = bool(self.result[0])
        self.close_connection()
        return player_exists

    def check_matches_existence(self, id):
        self.open_connection()
        query = f'''
                SELECT CASE WHEN EXISTS (
                    SELECT 1 FROM MATCHES WHERE MATCH_ID = ?
                ) THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END AS PlayerExists
                '''
        self.cursor.execute(query, id)
        self.result = self.cursor.fetchone()
        player_exists = bool(self.result[0])
        self.close_connection()
        return player_exists


    def add_new_user(self, id, nickname, player_server, rank, league_points):
        query = f'''
                INSERT INTO PLAYER (PLAYER_ID, NICKNAME, PLAYER_SERVER, RANK_SOLO, LEAGUE_POINTS)
                VALUES (?, ?, ?, ?, ?)
                '''
        self.open_connection()
        self.cursor.execute(query, id, nickname, player_server, rank, league_points)
        self.conn.commit()
        self.close_connection()
        return self.result

    def add_new_player_account(self, player_id, account_id, puuid):
        query = f'''
                INSERT INTO PLAYER_RIOT_ACCOUNT_DATA (PLAYER_ID, ACCOUNT_ID, PUUID)
                VALUES (?, ?, ?)
                '''
        self.open_connection()
        self.cursor.execute(query, player_id, account_id, puuid)
        self.conn.commit()
        self.close_connection()

    def add_new_matches(self,player_id, date, match_id, match_type):
        query = f'''
                INSERT INTO MATCHES (PLAYER_ID, DATE_OF_MATCH, MATCH_ID, TYPE_OF_MATCH)
                VALUES (?, ?, ?, ?)
                '''
        self.open_connection()
        self.cursor.execute(query, player_id, date, match_id, match_type)
        self.conn.commit()
        self.close_connection()

    def add_new_lp_gains(self,player_id, date, LPS_amount):
        query = f'''
                INSERT INTO MATCHES (PLAYER_ID, DATE_OF_UPDATE, AMOUNT_OF_LPS)
                VALUES (?, ?, ?)
                '''
        self.open_connection()
        self.cursor.execute(query, player_id ,date , LPS_amount)
        self.conn.commit()
        self.close_connection()


    def add_match_data_info(self, data):
        query = f'''INSERT INTO MATCH_DATA (PLAYER_ID, MATCH_ID, DATE_OF_MATCH, WIN,
                                      RANKED_SOLO, RANKED_DUO, GAME_CREATION, GAME_DURATION, GAME_END_TIMESTAMP, GAME_MODE, 
                                      GAME_START_TIMESTAMP, GAME_TYPE, MAP_ID, EARLIEST_BARON, DETECTOR_WARDS_PLACED, FIRST_BLOOD_KILL,  
                                      ENEMY_MISSING_PING, VISION_SCORE, WARD_PLACED, ASSISTS_ME_PINGS, BARON_KILLS, DRAGON_KILLS, 
                                      HERALD_KILLS, FIRST_TURRET, CONTROL_WARDS_PLACED, TEAM_ID)  
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                      '''
        #data = json.loads(match_info)
        #zadanie jest dość proste muszę wyciągnać obiekt participant dla kązdego puuid i wrzucić do bazy :)
        players = [participant['puuid'] for participant in data["info"]['participants']]
        info = data["info"]
        for participant in data['info']['participants']:
            riot_data_tool = riot_data_tool = GET_DATA(key=self.riot_key, region="eun1", server="europe")
            user = riot_data_tool.user_by_name(participant["summonerName"])
            if user:
                ranks = riot_data_tool.ranks_by_id(user["id"])
                for rank in ranks:
                    if rank["queueType"] == "RANKED_SOLO_5x5":
                        if not self.check_user_existence(user["id"]):
                            self.add_new_user(user["id"], participant["summonerName"], "europe", rank["tier"] + rank["rank"],
                                              rank["leaguePoints"])

                        match_list = riot_data_tool.match_list_by_puuid(user["puuid"], volume=30)
            puuid = participant['puuid']
            #tu musi byc wyszstko zeby do tabeli wrzucic pozdro, mozliwe potrzebne parsowanie ale chyba nie do dat
            if participant["role"] == "SOLO":
                solo = True
                duo = False
            else:
                solo = False
                duo = True
            if participant["challenges"]["takedownOnFirstTurret"] == 1:
                firstTurret = True
            else:
                firstTurret = False

            converted_date = datetime.datetime.fromtimestamp(info["gameStartTimestamp"]/1000)
            human_readable_date = converted_date.strftime('%Y-%m-%d %H:%M:%S')
            parameters = [participant["summonerId"] ,data["metadata"]["matchId"], converted_date ,participant["win"], solo, duo, info["gameCreation"], info["gameDuration"], info["gameEndTimestamp"], info["gameMode"], info["gameStartTimestamp"] ,info["gameType"], info["mapId"], 0,
                          participant["detectorWardsPlaced"], participant["firstBloodKill"], participant["enemyMissingPings"], participant["visionScore"],
                          participant["wardsPlaced"], participant["assistMePings"], participant["baronKills"], participant["dragonKills"], participant["challenges"]["teamRiftHeraldKills"],
                          firstTurret, participant["challenges"]["controlWardsPlaced"], participant["teamId"]
            ]
            self.open_connection()
            self.cursor.execute(query, parameters)
            self.conn.commit()

        self.close_connection()


    def main_adding_tool(self, user_name, region, server, match_list_volume):
        riot_data_tool = GET_DATA(key=self.riot_key, region=region, server=server)
        user = riot_data_tool.user_by_name(user_name)
        if user:
            ranks = riot_data_tool.ranks_by_id(user["id"])
            for rank in ranks:
                if rank["queueType"]=="RANKED_SOLO_5x5":
                    if not self.check_user_existence(user["id"]):
                        self.add_new_user(user["id"], user_name, server, rank["tier"]+rank["rank"], rank["leaguePoints"])

                    match_list = riot_data_tool.match_list_by_puuid(user["puuid"], volume=match_list_volume)
                    for match in match_list:
                        match_info = riot_data_tool.get_match_data(match)
                        #trzeba tutaj wypobirać wszystkie dane jsonowe
                        #player_id mam z wyzej
                        #trzeba tu zrobic system ze w z kazdego meczu biore tez mecze innych XDXD


                        print(match_info)

                        timestamp = match_info["info"]["gameCreation"]/1000
                        date = datetime.datetime.fromtimestamp(timestamp).date()
                        self.add_new_matches(user["id"],date, match, match_info["info"]["gameMode"])
                        print(match)
                        self.add_match_data_info(match_info)


test = UPLOAD_DATA()
test.main_adding_tool("RaidenShockblade","eun1","europe", 98)