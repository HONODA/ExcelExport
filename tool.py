import json
class tool():

    db_address = 'Settings\\db.json'
    sql_address = 'Settins\\sql.json'
    @staticmethod
    def loadJson():
        f = open(tool.db_address, encoding='utf-8')  
        setting = json.load(f)
        content = setting
        return content
    @staticmethod
    def loadSqlJson():
        f = open(tool.sql_address, encoding='utf-8')  
        setting = json.load(f)
        content = setting
        return content
