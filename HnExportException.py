
class HnExportException(Exception):
    path = "log.txt"

    def __init__(self,place, arg):
        self.place = place
        self.arg = arg
        mstr = ''
        for i in arg :
            mstr += str(i)
        
        self.WriteLog(place+mstr)
    
    def WriteLog(self,_str):
       file =  open(self.path,"a+",encoding='utf-8')
       file.writelines(_str+"\n")
       file.close()