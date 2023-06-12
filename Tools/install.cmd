python -m venv .\venv
cd .\python_Scripts
copy get_last_games.py ..\venv\get_data.py
cd ..
cd \venv

pip3 install json

pip3 install riotwatcher

pip3 install SQLAlchemy

pip install dataclasses

pip install psycopg2

pip install jproperties

pip install requests