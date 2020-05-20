import sys
from PyQt5.QtWidgets import *
import HnExport

class pool():
    #静态ui
    BEFORE_DATE = 'before_date'
    AFTER_DATE = 'after_date'
    export_address = 'Export\\'
    template_address = 'templates\\对账单模板.xlsx'
    @staticmethod
    def set_UI(_objUI):
        pool.ui = _objUI
    @staticmethod
    def return_UI():
        return pool.ui
