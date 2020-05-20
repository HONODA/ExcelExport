import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QModelIndex
import HnExport
from pool import pool
from tool import tool
from Export_Service import Service

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
    
    #ui.Supliertable.clicked.connect()
def before_DateChanged():
    if check() == False:
        ui.after_date.setDate(ui.before_date.date())

def after_DateChange():
    if check() == False:
        ui.before_date.setDate(ui.after_date.date())

def account_List_dblclick(index):
    data = index.data()
    row = index.row()
    ui.Supliertable.clear()
    print(Service.getAccountDatabaseName(index.row(),index.data()))
    Service.showSuplier(Service.getAccountDatabaseName(row,data))
    ui.Supliertable.resizeColumnToContents(0)
    ui.Supliertable.resizeColumnToContents(1)


def select_all_button_click(event):
    ui.Supliertable.selectAll()

def clear_all_button_click(event):
    ui.Supliertable.clearSelection()

def export_excel(event):
    if ui.Supliertable.rowCount() == 0:
        return
    items = ui.Supliertable.selectedItems()
    if len(items) == 0:
        return#TODO 如果找不到供应商，请选择
    print(items[0].text())
    before_date = ui.before_date.date().toString('yyyy-MM-dd')
    after_date = ui.after_date.date().toString('yyyy-MM-dd')
    state = Service.insertStatement(items[0].text(),before_date,after_date)
    if state == "-1":
        return
    #print("sss")
    
    
def suplier_select_row(modelindex):
    #print(modelindex.data())

    pass
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = HnExport.Ui_Dialog()
    ui.setupUi(MainWindow)
    pool.set_UI(ui)
    hideCalendar()
    init()
    MainWindow.show()
    sys.exit(app.exec_())