python -m venv .\venv
cd .\python_Scripts
copy get_last_games.py ..\venv\get_data.py
cd ..
cd \venv

pip3 install json

pip3 install riotwatcher