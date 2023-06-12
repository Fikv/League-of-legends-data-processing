import requests
from Mappers.UserDataMapper import UserDataMapper
from UrlCreator import UrlCreator

class DataFetcher:
    def __init__(self): 
        pass
        

    def getUserData(self):
        urlCreator = UrlCreator()
        print(urlCreator.addPathVariableToUrl('PlayerDataByName','UNDZIO'))
        requests.get(urlCreator.addPathVariableToUrl('PlayerDataByName','UNDZIO')) 
        reponse = requests.get(urlCreator.addPathVariableToUrl('PlayerDataByName','UNDZIO'))
        if reponse.status_code == 200:
            data1 = reponse.json() 
            print(data1)
        else:
            print('Error:', reponse.status_code)
        reponse2 = requests.get(urlCreator.addPathVariableToUrl('MorePlayerDataByName',"aQApcMlCiZhMlJyNGgGhfOxn6N73wwdrJgkXxA2iI8t16Wg"))    
        if reponse2.status_code == 200:
            data2 = reponse2.json()
            print(data2)
        else:
            print('Error:', reponse.status_code)    
        mapper = UserDataMapper() 
        mapper.mapUserDataToTable(data1, data2)

o = DataFetcher()
o.getUserData()
            
        