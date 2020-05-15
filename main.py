import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QModelIndex
import HnExport
from pool import pool
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
     ui.calendar1.setVisible(False)
     ui.calendar_yes_button.setVisible(False)
     ui.calendar_cancal_button.setVisible(False)
def showCalendar(_value = ""):
    ui = pool.return_UI()
    ui.calendar1.setVisible(True)
    ui.calendar_yes_button.setVisible(True)
    ui.calendar_cancal_button.setVisible(True)
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
    ui = pool.return_UI()
    ui.after_date.keyPressEvent = after_datekeyPressEvent#value="after_date"
    ui.before_date.keyPressEvent = before_datekeyPressEvent#value="before_date"
    ui.before_date.setDate(QDate.currentDate())
    ui.after_date.setDate(QDate.currentDate())
    ui.before_date.dateChanged.connect(before_DateChanged)
    ui.after_date.dateChanged.connect(after_DateChange)
    Service.showAccount()
    ui.Accountlist.doubleClicked.connect(account_List_dblclick)
    ui.select_all_button.clicked.connect(select_all_button_click)
    ui.clear_all_button.clicked.connect(clear_all_button_click)
def before_DateChanged():
    if check() == False:
        ui.after_date.setDate(ui.before_date.date())
def after_DateChange():
    if check() == False:
        ui.before_date.setDate(ui.after_date.date())

def account_List_dblclick(index):
    data = index.data()
    row = index.row()
    ui.Suplierlist.clear()
    print(Service.getAccountDatabaseName(index.row(),index.data()))
    Service.showSuplier(Service.getAccountDatabaseName(row,data))

def select_all_button_click(event):
    ui.Suplierlist.selectAll()
def clear_all_button_click():
    #qindex = QModelIndex()
    ui.Suplierlist.clearSelection()
    #ui.Suplierlist.setCurrentIndex(qindex)

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