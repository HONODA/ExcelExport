#!usr/bin/python
# -*-coding: utf-8 -*-
import pymssql #引入pymssql模块
from tool import tool

class sql ():
        
    SERVER = tool.loadJson()['SERVER']
    USER = tool.loadJson()['USER']
    PASSWORD =  tool.loadJson()['PASSWORD']
    DATABASE =  tool.loadJson()['DATABASE']

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
        
if __name__ == '__main__':
    conn = conn()