from sql import sql as sq
from tool import tool
#import sql as sq
class command :
    @staticmethod
    def get_KdAccount():
        dat = sq.DATABASE 
        command.changeDataBase()
        conn = sq.conn()
        sql = "select FACCtNumber as 账套序号,FAcctName as 账套名称,FDBName as 数据库名称 from t_ad_kdAccount_gl"
        #sql = sql.replace('-itemname',itemname)
        cursor = conn.cursor() #创建游标
        cursor.execute(sql)
        rows = cursor.fetchone()
        list = []
        while rows:
            list.append(rows)
            rows = cursor.fetchone()
        conn.close()
        command.changeDataBase(_database=dat)
        return list
    @staticmethod
    def toJsonSource(list):
        l = []
        floor1 = 0
        strs = "["
        for i in list:
            strs = strs +"{"
            floor2 = 0
            for j in i:
                if floor2 == len(list[floor1])-1:
                    a = "\""+str(floor2)+"\""
                    strs = strs +a+":\""+ str(j) +"\""
                else:
                    a = "\""+str(floor2)+"\""
                    strs = strs + a +":\""+ str(j) +"\","
                floor2 = floor2 + 1
            if floor1 == len(list)-1:
                strs = strs + "}"
            else:
                strs = strs + "},"
            floor1 = floor1 + 1
        strs = strs + "]"
        return strs
    @staticmethod
    def changeDataBase(_database =''):
        if _database == '':
            sq.change()
        else:
            sq.change(database=_database)
    @staticmethod
    def getSuplier(id = ""):
        where  = ""
        if id != "":
            where = "where FITEMID ='" + id +"'"
        conn = sq.conn()
        sql = "select FItemID , Fname as 供应商名称, FNumber as 编码 from t_Supplier" + where 
        cursor = conn.cursor() #创建游标
        cursor.execute(sql)
        rows = cursor.fetchone()
        list = []
        while rows:
            list.append(rows)
            rows = cursor.fetchone()
        conn.close()
        return list
    @staticmethod
    def getStatement(_suplier,_before_date,_after_date):
        where  = ""
        where = " where FSupplyID ='" + _suplier +"' and Fdate >= '"+_before_date +"' and Fdate <='"+_after_date+"'"
        conn = sq.conn()
        sql = tool.loadSqlJson()[0]['select_statement']+ where 
        print(sql)
        cursor = conn.cursor() #创建游标
        cursor.execute(sql)
        rows = cursor.fetchone()
        list = []
        while rows:
            list.append(rows)
            rows = cursor.fetchone()
        conn.close()
        return list

if __name__ == '__main__':
    list = command.getBomMotherByBomNo('BOM000009')
    num =[1,8,11,27]
    list1 =[]
    
    for l in list:
        list2 =[]
        for n in num:
            list2.append(l[n])
        list1.append(list2)
    print(list[0][1])
    list = command.getBomCild(list[0][1])
    print(command.toJsonSource(list))
