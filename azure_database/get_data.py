import sys
from riotwatcher import LolWatcher, ApiError

class GET_DATA:
    def __init__(self, key, region, server):
        self.key = key
        self.server = server
        self.region = region
        self.watcher = LolWatcher(key)

    def user_by_name(self, name):
        try:
            me = self.watcher.summoner.by_name(self.region, name)
        except:
            print(f"While getting user data for {name} user, some error happend:\n",sys.exc_info()[0])
            return False
        else:
            return me

    def ranks_by_id(self, id):
        try:
            me = self.watcher.league.by_summoner(self.region, id)
        except:
            print(f"While getting ranks data for {id}, some error happend:\n",sys.exc_info()[0])
            return False
        else:
            return me

    def match_list_by_puuid(self, puuid, volume=10):
        try:
            me = self.watcher.match.matchlist_by_puuid(self.server, puuid, count=volume)
        except:
            print(f"While getting games list for {puuid}, some error happend:\n",sys.exc_info()[0])
            return False
        else:
            return me

    def get_match_data(self,id):
        try:
            me = self.watcher.match.by_id(self.server, id)
        except:
            print(f"While getting game for {id}, some error happend:\n",sys.exc_info()[0])
            return False
        else:
            return me