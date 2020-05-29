import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDate
from sql import sql 
from pool import pool
from tool import tool
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
            if Service.checkWhetherAccount(i['数据库名称']):
                ui.Accountlist.addItem(i['账套名称'])
    @staticmethod
    def showSuplier(_databasename):
        ui = pool.return_UI()
        command.changeDataBase(_database=_databasename)
        mlist = command.getSuplier()
        Service.suplier_list = mlist
        count = len(mlist)
        ui.Supliertable.setRowCount(count)
        _i = 0
        for i in mlist:
            ui.Supliertable.setItem(_i,0,QTableWidgetItem(str(i['编码'])))
            ui.Supliertable.setItem(_i,1,QTableWidgetItem(str(i['供应商名称'])))
            _i +=1
            #ui.Suplierlist.addItem(i['供应商名称'])
        
    @staticmethod
    def getSuplierName(_str):
        if Service.suplier_list.count == 0:
            return None
        for i in Service.suplier_list:
            if i['编码'] == _str:
                return i['供应商名称']
        return None

    
    @staticmethod
    def getAccountDatabaseName(_index,_str):
        if Service.account_list.count == 0:
            return None
        for i in Service.account_list:
            if i['账套名称'] == _str:
                return i['数据库名称']
        return None
    @staticmethod
    def checkWhetherAccount(_str_account_name):
        for i in tool.loadJson():
            if i['DATABASE'] == _str_account_name:
                return True
        return False

    @staticmethod
    def getStatement(_suplier,_before_date,_after_date):
        mlist = command.getStatement(_suplier,_before_date,_after_date)
        return mlist 
    @staticmethod
    def insertStatement(_suplier,fs,_before_date,_after_date):
        _before_date_ = _before_date.replace("年","-").replace("月",'-').replace('日','')
        _after_date_ = _after_date.replace("年","-").replace("月",'-').replace('日','')
        mlist = Service.getStatement(_suplier,_before_date_,_after_date_)
        supliername = Service.getSuplierName(_suplier)
        fs = fs +"\\"+ supliername + _before_date +"-"+_after_date+".xlsx"
        print(fs)
        
        after_list =[]
        if mlist != None and len(mlist) != 0:
            tool.Copy(fs)
            for i in mlist[0]:
                after_list.append("&"+i+"&")
            after_list.append("&前时间&")
            after_list.append("&后时间&")

            tool.replace_Excel_Argv(after_list,mlist,fs,_title=supliername+"对账单",_insert_row=True,_before_date=_before_date,_after_date=_after_date)
        else:
            return "无"+supliername+"公司的数据。"