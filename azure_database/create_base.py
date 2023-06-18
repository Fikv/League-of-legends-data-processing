import pyodbc


# Konfiguracja połączenia do bazy danych
server = 'domino403.database.windows.net'
database = 'lol-data-analise'
username = 'domino403'
password = 'Debica2001'
driver = '{ODBC Driver 18 for SQL Server}'  # Upewnij się, że masz zainstalowany sterownik ODBC odpowiedni dla Twojego systemu, jeśli nie to pobierz go z linku poniżej
# https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15
# Tworzenie łańcucha połączenia
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# Nawiązanie połączenia z bazą danych
conn = pyodbc.connect(connection_string)

# Utworzenie kursora
cursor = conn.cursor()


with open('..\\Datebase_scritps\\dodanie_tabeli_player.sql', 'r') as file:
    create_table_query = file.read()

# Wykonanie zapytania
cursor.execute(create_table_query)
print("Tabela została utworzona")

conn.commit()
with open('..\\Datebase_scritps\\dodanie_tabeli_riot_account.sql', 'r') as file:
    create_table_query = file.read()

# Wykonanie zapytania
cursor.execute(create_table_query)
print("Tabela została utworzona")

conn.commit()
with open('..\\Datebase_scritps\\dodanie_tabeli_matches.sql', 'r') as file:
    create_table_query = file.read()

# Wykonanie zapytania
cursor.execute(create_table_query)
print("Tabela została utworzona")

conn.commit()
with open('..\\Datebase_scritps\\dodanie_tabeli_player_lp_gains.sql', 'r') as file:
    create_table_query = file.read()

# Wykonanie zapytania
cursor.execute(create_table_query)
print("Tabela została utworzona")

conn.commit()
# Zakończenie połączenia
cursor.close()
conn.close()