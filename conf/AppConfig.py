from jproperties import Properties

def load_api_key():
    configs = Properties()
    with open('conf/app.properties', 'rb') as config_file:
        configs.load(config_file)
    return configs.get('API_KEY')