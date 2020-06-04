from PyQt5.QtCore import pyqtSignal,QRunnable,QObject,QThreadPool,QMutex,QThread
# from concurrent.futures import ThreadPoolExecutor,as_completed
from Export_Service import Service
from pool import pool
from tool import tool
import threading
from HnExportException import HnExportException
import traceback


class HnQtPoolThread(QThread):
    '''
    线程池线程，用于管理线程池
    '''
    def __init__(self):
        super().__init__()
        self.threadpool = HnQTThreadPool()
    def run(self):
        '''
        启动线程池
        '''
        self.threadpool.Start()
        # threadpool = QThreadPool()
        # threadpool.globalInstance()
        # threadpool.start(None)
        # threadpool.waitForDone()
    def addThread(self,_thread):
        self.threadpool.addThread(_thread)
class HnPyThreadPool():
    '''
    Py自身线程池（未用到）
    '''
    futurelist =[]
    
    def __init__(self,_suplier,fs,_before_date,_after_date,_Hnsignal=None):
        super().__init__()
        self._suplier =_suplier
        self.fs = fs
        self._before_date = _before_date
        self._after_date = _after_date
        self.signal = _Hnsignal
        self.poolnum = tool.loadJsons(tool.setting_address)[0]['pool_num']

    def addThread(self,_thread):
        self.futurelist.append(_thread)

    def start(self):
        pass

class HnQTThreadPool():
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
        self.threadpool.waitForDone()
        self.thread_list.clear()
class HnSignal(QObject):
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()


class HnThreadForExcel_Argv(QRunnable):
    '''
        为Excel生成提供PYQT线程类
    '''

    def __init__(self,_suplier,dfs,_before_date,_after_date,_Hnsignal=None):
        super().__init__()
        self._suplier =_suplier
        self.fs = dfs
        self._before_date = _before_date
        self._after_date = _after_date
        self.signal = _Hnsignal
        self.setAutoDelete(True)
    def run(self):
        try:
            mresult = Service.insertStatement(self._suplier,self.fs,self._before_date,self._after_date)
            self.signal.result_signal.emit(mresult)
            self.signal.progress_signal.emit(1)
        except Exception as e :
            tool.WriteLog(traceback.format_exc())
            raise HnExportException("inserstatement:"+traceback.format_exc())

    def __del__(self):
        pass
