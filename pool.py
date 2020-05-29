import sys
from PyQt5.QtWidgets import *
import HnExport

class pool():
    #静态ui
    BEFORE_DATE = 'before_date'
    AFTER_DATE = 'after_date'
    export_address = 'Export\\'
    template_address = 'templates\\对账单模板.xlsx'
    max_progress_value = 0
    error_message =""
    NowAccountName =""
    #全局当前账套名称 NowAccountName
    #全局线程池线程 threadpool
   
    @staticmethod
    def set_UI(_objUI):
        pool.ui = _objUI
    @staticmethod
    def return_UI():
        return pool.ui
