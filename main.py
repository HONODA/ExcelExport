import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QIcon
#from concurrent.futures import ThreadPoolExecutor,as_completed
import HnExport
from pool import pool
from tool import tool
from HnThreadTool import  HnSignal, HnThreadForExcel_Argv,HnQtPoolThread
from HnExportException import HnExportException
from Export_Service import Service
import threading

def check():
    ui = pool.return_UI()
    beforestring = ui.before_date.date().toString(Qt.ISODate)
    afterstring = ui.after_date.date().toString(Qt.ISODate)
    _is = beforestring.split('-')
    _js = afterstring.split('-')
    _i = 0
    for i in _is :

        bf = float(i)
        af = float(_js[_i])
        if bf > af:
            return False
        elif bf == af:
            _i += 1
            continue
        else:
            return True
    # if i > j :
    #     print("")
def hideCalendar():
     ui =pool.return_UI()
     ui.calendar1.setHidden(True)
     ui.calendar_yes_button.setHidden(True)
     ui.calendar_cancal_button.setHidden(True)
     ui.verticalLayoutWidget_2.setHidden(True)
def showCalendar(_value = ""):
    ui = pool.return_UI()
    ui.calendar1.setHidden(False)
    ui.calendar_yes_button.setHidden(False)
    ui.calendar_cancal_button.setHidden(False)
    ui.verticalLayoutWidget_2.setHidden(False)
    #ui.buttonBox.accepted.connect(lambda : setDate(ui.calendar1.selectedDate(),_value))
    
    ui.calendar_yes_button.clicked.connect(lambda : setDate(ui.calendar1.selectedDate(),_value))
    ui.calendar_cancal_button.clicked.connect(hideCalendar)
def setDate(_date_value,dateedit):
    ui = pool.return_UI()
    if dateedit == pool.AFTER_DATE:
        ui.after_date.setDate(_date_value)
    elif dateedit == pool.BEFORE_DATE:
        ui.before_date.setDate(_date_value)
    ui.calendar_yes_button.clicked.disconnect()
    if check() == False:
        ui.after_date.setDate(ui.before_date.date())
    hideCalendar()
def after_datekeyPressEvent(event):
    if event.key() == Qt.Key_Space:
        showCalendar(pool.AFTER_DATE)
def before_datekeyPressEvent(event): 
    if event.key() == Qt.Key_Space:
        showCalendar(pool.BEFORE_DATE)
def init():
    #ui = HnExport.Ui_Dialog()
    #ui = pool.return_UI()
    ui.after_date.keyPressEvent = after_datekeyPressEvent#value="after_date"
    ui.before_date.keyPressEvent = before_datekeyPressEvent#value="before_date"
    ui.before_date.setDate(QDate.currentDate())
    ui.after_date.setDate(QDate.currentDate())
    ui.before_date.dateChanged.connect(before_DateChanged)
    ui.after_date.dateChanged.connect(after_DateChange)
    Service.showAccount()
    ui.Accountlist.setSelectionBehavior(QAbstractItemView.SelectRows)
    ui.Accountlist.doubleClicked.connect(account_List_dblclick)
    ui.select_all_button.clicked.connect(select_all_button_click)
    ui.clear_all_button.clicked.connect(clear_all_button_click)
    ui.export_button.clicked.connect(export_excel)
    ui.Supliertable.clicked.connect(suplier_select_row)
    ui.close_button.clicked.connect(colse_button)
    ui.search_suplier.returnPressed.connect(search_suplier)

    #定义生成一个进度条
    hideProgressbar()
    #ui.Supliertable.clicked.connect()

def before_DateChanged():
    if check() == False:
        ui.after_date.setDate(ui.before_date.date())

def after_DateChange():
    if check() == False:
        ui.before_date.setDate(ui.after_date.date())

def account_List_dblclick(index):
    if not ui.progressBar.isHidden():
        QMessageBox.information(ui.Supliertable,"错误","已有文件正在生成，请等待进程结束")
        return
    data = index.data()
    row = index.row()
    ui.Supliertable.clear()
    print(Service.getAccountDatabaseName(index.row(),index.data()))
    pool.NowAccountName = index.data()
    Service.showSuplier(Service.getAccountDatabaseName(row,data))
    ui.Supliertable.resizeColumnToContents(0)
    ui.Supliertable.resizeColumnToContents(1)

def select_all_button_click(event):
    ui.Supliertable.selectAll()

def clear_all_button_click(event):
    ui.Supliertable.clearSelection()

def export_excel(event):
    if not ui.progressBar.isHidden():
        QMessageBox.information(ui.Supliertable,"错误","已有文件正在生成，请等待进程结束")
        return
    if ui.Supliertable.rowCount() == 0:
        QMessageBox.information(ui.Supliertable,"错误","没有供应商内容")
        return
    items = ui.Supliertable.selectedItems()
    if len(items) == 0:
        QMessageBox.information(ui.Supliertable,"错误","没有选择供应商")
        return
    print(items[0].text())
    before_date = ui.before_date.date().toString('yyyy年MM月dd日')
    after_date = ui.after_date.date().toString('yyyy年MM月dd日')
    fs = QFileDialog.getExistingDirectory(directory=pool.export_address)
    if fs =="":
        return "选择文件夹路径为空"
    count = 0
    merror =""

    #执行excel生成任务，且放入进程池(旧方法，无使用PyQt线程池)
    # poolnum = tool.loadJsons(tool.setting_address)[0]['pool_num']
    # with ThreadPoolExecutor(int(poolnum)) as po:
    #     futurelist =[]
    #     for i in items:
    #         if count % 2 == 0:
    #             future = po.submit(Service.insertStatement,i.text(),fs,before_date,after_date)
    #             #state = Service.insertStatement(i.text(),fs,before_date,after_date)
    #             future.add_done_callback(message_call_back)
    #             futurelist.append(future)
    #         count +=1
    #     for f in as_completed(futurelist):
    #         if f.result() != None:
    #             merror += f.result()+"\n"

#新方法使用了PyQt线程池，但是直接运行会卡住
#--------------------------------------------
    maxlen = int(len(items)/2)
    ui.progressBar.setMaximum(maxlen)
    pool.max_progress_value = maxlen
    #poolnum = tool.loadJsons(tool.setting_address)[0]['pool_num']
    #threadpool.setMaxThreadCount(int(poolnum))
    #threadpool = HnQTObjectThreadPool()
    showProgressbar()
    pool.poolthread = HnQtPoolThread()#线程管理线程池
    try:
        for i in items:
            if count % 2 == 0 :
                threadsignal = HnSignal()
                thfs = fs
                mbedate = before_date
                mafdate = after_date
                mythread = HnThreadForExcel_Argv(i.text(),thfs,mbedate,mafdate,threadsignal)
                threadsignal.progress_signal.connect(progress_bar_callback)
                threadsignal.result_signal.connect(message_call_back)
                pool.poolthread.addThread(mythread)

            count +=1
        pool.poolthread.start()
    except Exception as e:
        print(e.with_traceback())
        QMessageBox.information(ui.Supliertable,"错误",e.with_traceback())
        raise HnExportException("导出位置",e.args)
    print("完成")
#------------------------------------------

def progress_bar_callback(step):
    value = ui.progressBar.value()
    ui.progressBar.setValue(value + step)
    if ui.progressBar.value() == pool.max_progress_value:
        hideProgressbar()
        progress_bar_all_done()
def progress_bar_all_done():
    if pool.error_message != "":
        QMessageBox.information(ui.Supliertable,"错误",pool.error_message)
    else:
        QMessageBox.information(ui.Supliertable,"成功","成功生成")
    pool.error_message = ""
def message_call_back(merror):
    if merror != "":
        pool.error_message = pool.error_message + merror +"\n"

def showProgressbar():
    ui.progressBar.setHidden(False)
    ui.progressBar.reset()
    ui.progressBar.setValue(0)
def hideProgressbar():
    ui.progressBar.setHidden(True)
    ui.progressBar.reset()
    ui.progressBar.setValue(0)
def suplier_select_row(modelindex):
    #print(modelindex.data())
    pass
def colse_button(event):
    if not ui.progressBar.isHidden():
        QMessageBox.information(ui.Supliertable,"错误","已有文件正在生成，请等待进程结束")
        return
    app.exit(0)

def search_suplier():
        _i = 0
        compare_value = ui.search_suplier.text()
        for i in Service.suplier_list:
            if str(i['编码']).find(compare_value) >= 0 or str(i['供应商名称']).find(compare_value) >= 0:
                ui.Supliertable.selectRow(_i)
            _i +=1
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        MainWindow = QMainWindow()
        ui = HnExport.Ui_Dialog()
        ui.setupUi(MainWindow)
        MainWindow.setWindowTitle("广州市天志软件科技有限公司")
        try:
            r = QIcon("Hn.ico")
            MainWindow.setWindowIcon(r)
        except:
            pass
        
        pool.set_UI(ui)
        hideCalendar()
        init()
        MainWindow.show()

        sys.exit(app.exec_())
    except Exception as e:
        raise HnExportException("main",e.args)