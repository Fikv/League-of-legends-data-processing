import os
import riotwatcher
import sys
import subprocess
import optparse
import json
from riotwatcher import LolWatcher, ApiError


parser = optparse.OptionParser()
parser.add_option("-k", "--key", dest="api_key",
                  help="Provide Riot key for connection to riot api")
parser.add_option("-s", "--server", dest="server_name",
                  help="Provide Riot server name which you want connect to")

(options, args) = parser.parse_args()

current_dir = os.path.dirname(os.path.abspath(__file__))


if options.api_key is None:
    print("Please provide Riot key")
    os.system("python .\get_last_games.py -h")
    sys.exit()

key = str(options.api_key)

if options.server_name is None:
    print("Please provide Riot server name")
    os.system("python .\get_last_games.py -h")
    sys.exit()

server = str(options.server_name)

print("Create connection to Riot API Server")
watcher = LolWatcher(key)
challenger_list = watcher.league.challenger_by_queue(server,"RANKED_SOLO_5x5")
print(f"\n\n\n{challenger_list['entries'][:10]}")