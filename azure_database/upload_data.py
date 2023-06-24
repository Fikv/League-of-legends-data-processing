import pyodbc
import sys
from azure_database.get_data import GET_DATA
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
        '''
        description:
            function adding the information to table PLAYER_LP_GAINS
        params:
            player_id - this is player id get from riot api
            date - the date when the account information was updated
            lps_amount - amount of league points for user
        '''
        query = f'''
                INSERT INTO PLAYER_LP_GAINS (PLAYER_ID, DATE_OF_UPDATE, AMOUNT_OF_LPS)
                VALUES (?, ?, ?)
                '''
        self.open_connection()
        self.cursor.execute(query, player_id ,date , LPS_amount)
        self.conn.commit()
        self.close_connection()

    def main_adding_tool(self, user_name:str, region:str, server:str, match_list_volume:int):
        '''
        description:
            The main function for adding tool. While calling it and providing a user information you can add him to the database
            and information about his games and ranks progress.

        params:
            user_name - league name from the game
            region - region where player have located the account, for example eun1
            server - name for game server, for example eun1 have server named europe
            match_list_volume - number how many games counting from the newest one you want to add to the database
        '''
        # create connection to riot API
        riot_data_tool = GET_DATA(key=self.riot_key, region=region, server=server)
        # get user data {"id","accountId","puuid","name","profileIconId","revisionDate","summonerLevel"}
        user = riot_data_tool.user_by_name(user_name)
        if user: # if exist go to next steps
            # get users ranks info this will be a list of rank dicts, one dict have structure: {"leagueId","queueType","tier","rank","summonerId","summonerName","leaguePoints","wins","losses","veteran","inactive","freshBlood","hotStreak"
            ranks = riot_data_tool.ranks_by_id(user["id"])
            for rank in ranks: # iter on the ranks list and find 'solo duo' :D
                if rank["queueType"]=="RANKED_SOLO_5x5":
                    # check if user is already added to database and if not add him
                    if not self.check_user_existence(user["id"]):
                        self.add_new_user(user["id"], user_name, server, rank["tier"]+rank["rank"], rank["leaguePoints"])

                    # get match list by user puuid
                    match_list = riot_data_tool.match_list_by_puuid(user["puuid"], volume=match_list_volume)
                    for match in match_list: # iter by elements in the matches list
                        # get data about specific match from the list
                        match_info = riot_data_tool.get_match_data(match)
                        # get match time stamp and convert it to date
                        timestamp = match_info["info"]["gameCreation"]/1000
                        date = datetime.datetime.fromtimestamp(timestamp).date()
                        self.add_new_matches(user["id"],date, match, match_info["info"]["gameMode"])

test = UPLOAD_DATA()
test.main_adding_tool("Myś","eun1","europe",5)