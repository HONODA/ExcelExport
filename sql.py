#!usr/bin/python
# -*-coding: utf-8 -*-
import pymssql #引入pymssql模块
from tool import tool

class sql ():
        
    SERVER = tool.loadJson()[0]['SERVER']
    USER = tool.loadJson()[0]['USER']
    PASSWORD =  tool.loadJson()[0]['PASSWORD']
    DATABASE =  tool.loadJson()[0]['DATABASE']
    LOG = tool.loadJsons(tool.setting_address)[0]["write_sql_log"]
    @staticmethod
    def conn():
        try:
            #connect = pymssql.connect('192.168.1.220', 'sa', 'Fang85558048', 'AIS20200308203304') #服务器名,账户,密码,数据库名
            connect = pymssql.connect(server = sql.SERVER, user = sql.USER, password= sql.PASSWORD, database = sql.DATABASE,port='61307',as_dict= True) #服务器名,账户,密码,数据库名
            if connect:
                print("连接成功!")
        except Exception as e:
            print("连接失败" + str(e))
            return None
        return connect
    @staticmethod
    def change(server = SERVER, user = USER, password= PASSWORD, database = DATABASE):
        sql.SERVER = server
        sql.USER =user
        sql.PASSWORD = password
        sql.DATABASE = database
        sql.WriteLog("切换数据库："+database)
    @staticmethod
    def excute(conn,_sql):
        cursor = conn.cursor() #创建游标
        if sql.LOG == "True":
            sql.WriteLog(_sql)
        cursor.execute(_sql)
        rows = cursor.fetchone()
        list = []
        while rows:
            list.append(rows)
            rows = cursor.fetchone()
        conn.close()
        return list
    @staticmethod
    def WriteLog(_str):
       file =  open(tool.log_address,"a+",encoding='utf-8')
       file.writelines(_str+"\n")
       file.close()
if __name__ == '__main__':
    conn = conn()