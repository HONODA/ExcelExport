import json
from shutil import copyfile
from shutil import SameFileError
import xlwings
import re
import math
from HnExportException import HnExportException
import datetime

class tool():

    db_address = 'Settings\\db.json'
    sql_address = 'Settings\\sql.json'
    setting_address = 'Settings\\settings.json'
    template_address = 'templates\\对账单模板.xlsx'
    log_address ='sql_log.txt'
    #allow_log = tool.loadJson(tool.setting_address)[0]["write_log"]
    @staticmethod
    def loadJson():
        fi = open(tool.db_address, encoding='utf-8')  
        setting = json.load(fi)
        content = setting
        return content
    @staticmethod
    def loadSqlJson():
        f = open(tool.sql_address, encoding='utf-8')  
        setting = json.load(f)
        content = setting
        return content
    @staticmethod
    def loadJsons(path):
        f = open(path, encoding='utf-8')  
        setting = json.load(f)
        content = setting
        return content
    @staticmethod
    def Copy(path = ''):
        try:
            copyfile(tool.template_address,path)
        except IOError as e:
            raise HnExportException("拒绝访问文件：路径："+path,e.args)
            return '拒绝访问'    #拒绝访问
        except SameFileError as e:
            raise HnExportException("存在相同名称文件"+path,e.args)
            return '存在相同文件'   #存在相同文件
        except Exception as e:
            raise HnExportException("未知异常"+path,e.args)
            return e.with_traceback()

    @staticmethod
    def replace_Excel_Argv(_argvlist,_list,_path,_title = '',_insert_row = False,_before_date =None,_after_date =None):
        '''
            与replace_Excel_Argv1相比，单次打开相应文件
           :param _argvlist: 传入对比表参数
        '''
        try:
            visi = tool.loadJsons(tool.setting_address)[0]["show_exccel_windows"]
            if visi == "True":
                app = xlwings.App(visible=True,add_book=False)#避免显示Excel 且多文件打开
            else:
                app = xlwings.App(visible=False,add_book=False)#避免显示Excel 且多文件打开
            wk = app.books.open(_path)
        except IOError as e:
            mstr = ''
            for i in e.args:
                mstr += str(i)
            wk.close()
            app.quit()
            raise HnExportException("replace_Excel_Argv:","拒绝访问，检查是否以打开该文件")
            return "拒绝访问，检查是否以打开该文件："+mstr
        if tool.replace_Excel_Argv2(_argvlist,_list,wk,_path,_title,len(_list),_insert_row=_insert_row,
        _before_date=_before_date,_after_date =_after_date) == "-1":
            wk.close()
            app.quit()
            raise HnExportException("replace_Excel_Argv:","处理过程出现错误 返回 -1")

        wk.save(_path)
        wk.close()
        app.quit()
    @staticmethod
    def replace_Excel_Argv1(_argv,_list,_wk,_path,_title = '',_times = 1,_insert_row = False):
        """
        根据 _argv 的参数查找excel表中存在的 _argv 并替换成_content
        excel 有三种结构，表头、表单、表尾
        表单内容需要根据list 无限扩增，表头表尾需要根据实际情况扩增
        表格类型：1表头 2 表体 3 表尾
        表体只插入一次多行数
        表头表尾允许覆盖，但不允许插入行
        :param _argv: 替换参数 eg: 在excel中存在 &argv1
        :param _list : 一个list
        :param _wk : wlwings中Work_book类 
        :param _path: 是excel文件路径
        :param _title: WrokSheet 中的标题名称
        :param _times: 带入填充次数，次数还受Rule约束，若表格中包含次数*times*则以*times*为准
        :rtype: :string
        """
        ws = _wk.sheets.active
        
        if _title != '':
            ws.name = _title
        maxrow = ws.api.usedRange.Rows.count
        maxcol = ws.api.usedRange.Columns.count
        for row in range(maxrow):
            for col in range(maxcol):
                ncolcode = tool.max_A_Z(col +1)
                value = ws.range(ncolcode+str(row+1))
                if  value.value != None and str(value.value).find(_argv) >= 0:
                        rule = Rule()
                        mdict = rule.get_rulelist(value.value)
                        for g in mdict.keys():
                            if g == '名称':
                               content = mdict.get(g,None)
                               continue
                            if g == '次数':
                                times = mdict.get(g,None)
                            if g == '表格类型':
                                mtypes = mdict.get(g,None)
                            tool.clear_argv(ws,row+1,col+1,Rule.rulelist[g],1) #清空除【名称】外的规则
                                               
                        for _i in range(len(content)):    #返回tuple
                            if _insert_row  and mtypes != None  and tool.inserted == False and len(mtypes) > _i and mtypes[_i] == '2' :
                                tool.insert_new(ws,row+1,_times)
                                tool.inserted = True
                            for con in _list :
                                for lens in range(len(_list)):
                                    newcontent = con[content[_i]]
                                    if times != None and len(times) > 0:
                                        if tool.replace_argv(ws,row +1,col +1,_argv,newcontent,times[_i]) == False:
                                            return "-1"
                                    else:
                                        if tool.replace_argv(ws,lens +1,col +1,_argv,newcontent) == False:
                                            return "-1"
                                
                            
                        

        
        return "1"
    @staticmethod
    def replace_Excel_Argv2(_argvlist,_list,_wk,_path,_title = '',_times = 1,_insert_row = False,_before_date =None,_after_date =None):
        inserted = False
        print("开始填充Excel数据")
        ws = _wk.sheets.active
        print("获取work_sheet状态")
        print("title名称{}".format(_title))
        if _title != '':
            if len(_title) > 30:
                _title = _title[:30]
            ws.name = _title
            print("设置名称")
        rows = ws.api.usedRange.Rows()  #所有行的数据
        maxcol = ws.api.usedRange.Columns.count #最大列数
        print("获取最大行列数，更改标题")
        argvdict = {}
        for argv in _argvlist:# O(_argvlist*len(rows)*col)
            row = 0
            for rowvalues in rows:
                for col in range(maxcol):
                    value = rowvalues[col]
                    if  value != None and str(value).find(argv) >= 0:
                        argvdict[argv] = tool.max_A_Z(col+1)+str(row+1)
                        break
                row +=1
        #遍历参数集中包含对应参数的单元格并记录在 argvdict 字典中
        print("遍历参数集中包含对应参数的单元格并记录在 argvdict 字典中")
        for argv in _argvlist:
            is_times = False
            if argv not in argvdict.keys():
                continue
            cellname = argvdict[argv]
            cellvalue = []
            cellvalue1 = ws[cellname].value
            row = ws[cellname].row
            col = ws[cellname].column
            rule = Rule()
            mdict = rule.get_rulelist(cellvalue1)
            for g in mdict.keys():
                if g == '名称':
                    content = mdict.get(g,None)
                    continue
                if g == '次数':
                    times = mdict.get(g,None)
                if g == '表格类型':
                    mtypes = mdict.get(g,None)
                if g == 'mnext':
                    nexts = mdict.get(g,None)
                #if mtypes != None and len(mtypes) > 0 and mtypes[0] == '2':
                tool.clear_argv(ws,row,col,Rule.rulelist[g],1) #清空除【名称】外的规则
            print("开始遍历数据库取到的数据")
            for colvalue in _list:#数据库取到的数据
                #每个单元格对应的规则                
                if _insert_row  and mtypes != None  and inserted == False and len(mtypes) > 0 and mtypes[0] == '2' :
                    tool.insert_new(ws,row,_times -1)
                    inserted = True
                    print("插入行数")
                #插入设置


                lastvalue = ''
                for ct in content:
                    if ct =='前时间' and _before_date != None:
                        colname = tool.max_A_Z(col)
                        ws[cellname].value = tool.replace_argv2(ws[cellname].value,argv,_before_date)#_before_date
                        break
                    if ct =='后时间' and  _after_date != None:
                        colname = tool.max_A_Z(col)
                        ws[cellname].value = tool.replace_argv2(ws[cellname].value,argv,_after_date)
                        break                
                        #ws[cellname].formula = "SUM("+cellname+":"+colname+str(_times)+")"
                    #else:
                    try:
                        lastvalue  = tool.replace_argv2(ws[cellname].value,argv,colvalue[ct])
                    except Exception as e:
                        raise HnExportException("replace_Excel_Argv2异常：key="+ct+"lastvalue =" +lastvalue,e.args)
                        return "-1"
                #名称配置
                print("名称配置")
                if times != None and len(times) > 0 and not is_times:
                    for t in range(int(times[0])):#只有一次
                        cellvalue.append(lastvalue)
                    is_times = True
                elif mtypes != None and len(mtypes) > 0 and mtypes[0]=='2':
                    cellvalue.append(lastvalue)
                    #填充次数配置

            ws[cellname].options(transpose=True).value = cellvalue     #纵列全赋值
            print("纵列全赋值")
    @staticmethod
    def replace_argv2(_source,_argv,_value,_times = 1):
            for i in range(int(_times)):
                if  _source != None and _source != "" :
                    _source = str(_source).replace(_argv,str(_value))
                else:
                    if _source != None:
                        _source += str(_value)
                    else:
                        _source = str(_value)
            print("替换单元格数据")
            return _source 

    @staticmethod
    def replace_argv(_work_sheet,_row,_col,_old,_content,_times = 1):
            for i in range(int(_times)):
                try:
                    mcell = _work_sheet.cells(_row + i,_col)
                except Exception as e:
                        raise HnExportException("replace_argv()出现异常:"+"第("+str(_row + i)+","+str(_col)+")单元格",e.args)
                        return False
                if  mcell.value != None and mcell.value != "" :
                    try:
                        mcell.value = str(mcell.value).replace(_old,str(_content))
                    except Exception as e:
                        raise HnExportException("replace_argv()出现异常:"+"单元格"+mcell.value+"_old ="+ str(type(_old))+"_content ="+str(type(_content)),e.args)
                        return False
                else:
                    if mcell.value != None:
                        mcell.value += str(_content)
                    else:
                        mcell.value = str(_content)
            return True    
    @staticmethod
    def clear_argv(_work_sheet,_row,_col,_argv,_times = 1):
            
            for i in range(int(_times)):
                try:
                    mcell = _work_sheet.cells(_row + i,_col)
                except Exception as e:
                        raise HnExportException("clear_argv()出现异常:"+"第("+str(_row + i)+","+str(_col)+")单元格",e.args)
                        return False
                if mcell.value != "" and mcell.value != None:
                    if type(mcell.value) == str:
                        mcell.value = re.sub(_argv + '(.*)'+ _argv,'',mcell.value,int(_times))
            return True    
    @staticmethod
    def insert_new(_work_sheet,_row,_times):
        for i in range(_times):
            _work_sheet.api.Rows(_row+1).Insert()

    @staticmethod
    def max_A_Z(_value):
        '''
        将最大列数转换为英文字母
        _value为获取到的单元格最大数
        _offest为最大列位数如： ZZZ 为 4
        '''
        _next = [0,0,0,0]
        _offset = len(_next)
        no_num = True
        mstr = ''
        for i in range(_offset):
            j = _offset - i -1
            if _value > 26:
                l_num = math.floor(_value / 26)
                n_num = _value - 26 * l_num 
                _value = l_num
                if n_num == 0 :
                    _next[j] = 26 + j - 1
                    _value -= 1
                else:
                    _next[j] = n_num + j  -1# 数值 + 位数 避免 出现 [0,3,0]
            else:
                _next[j] = _value + j -1   #数值 +j -1 当 总数为 1 应为A 不为 B
                break
        for _i in range(_offset):
            j = _offset - _i -1
            if _next[_i] != 0 :
                no_num = False 
            if no_num ==False:
                    mstr = mstr + chr(65 + _next[_i] - _i)
        return mstr

class Rule(object):

    rulelist = {'名称':'&','次数':'@times@','表格类型':'!type!','next':'mnext'}

    @staticmethod
    def add_rule(_key,_value):
        Rule.rulelist[_key,_value]
    @staticmethod
    def return_search(_argv,_str,_islist=False):
        '''
            根据所给参数返回查询到的中间内容
            :param islist 为 False 则返回为tuple
        '''
        mlist = []
        if type(_str) == str:
            mlist = re.findall(_argv + '(.*?)'+ _argv,_str)
        if _islist :
            return mlist
        else:
            return tuple(mlist)
 
    def get_rulelist(self,_str):
        rlist ={}
        for i in Rule.rulelist:
            v = Rule.return_search(Rule.rulelist[i],_str)
            rlist[i] = v
        return rlist

if __name__ == "__main__":
        app = xlwings.App(visible=True,add_book=False)#避免显示Excel 且多文件打开
        wk = app.books.open(r'J:\\pythonWorkPlace\\ExcelExport\\ExcelExport\\templates\\对账单模板.xlsx')
        ws = wk.sheets.active
        rows = ws.api.usedRange.Rows
        print(rows)
    # for i in range(1,1000):
    #     print(i)
    #     s = tool.max_A_Z(i)
    #     print(s)
    #print(s)
