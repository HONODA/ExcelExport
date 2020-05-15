import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDate
from sql import sql 
from pool import pool
from HnCommand import command
import HnExport

class Service():

    #展现金蝶账套
    @staticmethod
    def showAccount():
        ui = pool.return_UI()
        mlist = command.get_KdAccount()
        Service.account_list = mlist
        for i in mlist:
            ui.Accountlist.addItem(i['账套名称'])
    @staticmethod
    def showSuplier(_databasename):
        ui = pool.return_UI()
        command.changeDataBase(_database=_databasename)
        mlist = command.getSuplier()
        Service.suplier_list = mlist
        for i in mlist:
            ui.Suplierlist.addItem(i['供应商名称'])
    def getSuplier(_row,_index):
        if Service.account_list.count == 0:
            return None
        for i in Service.account_list:
            if i['账套名称'] == _str:
                return Service.account_list[_index]['数据库名称']
        return None
        
    @staticmethod
    def getAccountDatabaseName(_index,_str):
        if Service.account_list.count == 0:
            return None
        for i in Service.account_list:
            if i['账套名称'] == _str:
                return Service.account_list[_index]['数据库名称']
        return None
