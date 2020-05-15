import sys
from PyQt5.QtWidgets import *
import HnExport

class pool():
    #静态ui
    BEFORE_DATE = 'before_date'
    AFTER_DATE = 'after_date'
    @staticmethod
    def set_UI(_objUI):
        pool.ui = _objUI
    @staticmethod
    def return_UI():
        return pool.ui
