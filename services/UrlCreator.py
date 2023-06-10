from typing import final

import urllib3
from urllib import parse

class UrlCreator:
    
    def __init__(self):
        self.URLs = {
        'PlayerDataByName':"https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/",
        'MorePlayerDataByName':'https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/',# id :) 
        'GetMatchesHistoryByPuuid':'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/',
        'GetMatchData':'https://europe.api.riotgames.com/lol/match/v5/matches/' #tu matchid

    }
    
    def nicknameCodec(self,nickname):
        return parse.quote(nickname)

    def addApiKeyAtTheEnd(self,url, first):
       #FIRST FALSE JEST PO, ŻE PRZY WIĘKSZEJ ILOŚCI ARGUMENTÓW INACZEJ WYGLĄDA URL :) 
       if(first): 
         return url + '?api_key=' + 'RGAPI-f00bd7c6-e730-44f0-849d-6ae3f8f8bc6e'
       else:
         return url + '&api_key=' + 'RGAPI-f00bd7c6-e730-44f0-849d-6ae3f8f8bc6e'  
    
    def addPathVariableToUrl(self,urlname, value):
       if(urlname == 'PlayerDataByName'):
        return self.addApiKeyAtTheEnd(self.URLs.get(urlname) + self.nicknameCodec(value), True)
       elif(urlname == 'MorePlayerDataByName'):
          #value to id - z requesta wyzej 
          return self.addApiKeyAtTheEnd(self.URLs.get(urlname) + value, True) 
       elif(urlname == 'GetMatchesHistoryByPuuid'):
          #value to puuid 
         return self.addApiKeyAtTheEnd(self.URLs.get(urlname) + value + '/fdunuMVkmI7EqS9FU1T3odegnteyPdY76QeNPSIwNLcOex6lJXp-CrT-bEH9QYVkUDGSonGBtvWwZg/ids?start=0&count=100', False)
       elif(urlname == 'GetMatchData'):
         return self.addApiKeyAtTheEnd(self.URLs.get(urlname) + value, True)
       else:
          return self.addApiKeyAtTheEnd(self.URLs.get(urlname) + value)
    