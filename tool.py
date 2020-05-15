import json
class tool():

    db_address = 'Settings\\db.json'

    @staticmethod
    def loadJson():
        f = open(tool.db_address, encoding='utf-8')  
        setting = json.load(f)
        content = setting[0]
        return content
    
