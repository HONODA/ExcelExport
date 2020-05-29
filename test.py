from PyQt5.QtCore import QThreadPool,QThread,QRunnable
from tool import tool
from shutil import copyfile

class mythread(QRunnable):
    def __init__(self,argv):
        super().__init__()
        self.argv =argv
        self.setAutoDelete(True)
    def run(self):
        tool.doSomeThin1(self.argv)

class methodClass():
    mnum = 0
    @staticmethod
    def doSomeThine(num):
        methodClass.mnum = methodClass.mnum+num
        print("{}".format(methodClass.mnum))

if __name__ == "__main__":
    pool = QThreadPool()
    pool.globalInstance()
    num = 1
    for i in range(10):
        thread = mythread(i)
        pool.start(thread,priority=i)