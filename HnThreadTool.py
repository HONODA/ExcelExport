from PyQt5.QtCore import pyqtSignal,QRunnable,QObject,QThreadPool
from Export_Service import Service
from pool import pool
from tool import tool
import time
class HnQTObjectThreadPool():
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str)
    thread_list = []

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.threadpool.globalInstance()
        poolnum = tool.loadJsons(tool.setting_address)[0]['pool_num']
        self.threadpool.setMaxThreadCount(int(poolnum))
    
    def addThread(self,_thread):
        self.thread_list.append(_thread)
    def Start(self):
        for i in self.thread_list:
            self.threadpool.start(i)
class HnSignal(QObject):
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()


class HnThreadForExcel_Argv(QRunnable):
    '''
        为Excel生成提供PYQT线程类
    '''
    def __init__(self,_suplier,fs,_before_date,_after_date,_Hnsignal=None):
        super().__init__()
        self._suplier =_suplier
        self.fs = fs
        self._before_date = _before_date
        self._after_date = _after_date
        self.signal = _Hnsignal
    def run(self):
        mresult = Service.insertStatement(self._suplier,self.fs,self._before_date,self._after_date)
        self.signal.result_signal.emit(mresult)
        self.signal.progress_signal.emit(1)
    def __del__(self):
        pass
