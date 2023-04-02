from datetime import datetime

from PyQt5.QtCore import QTextEncoder
class log:
    def __init__(self,myWin = None):
        self.logs = ""
        self.window = myWin
        if myWin:
            self.logable = True
        else:
            self.logable = False

    def setmyWin(self,myWin):
        self.window = myWin
        if myWin:
            self.logable = True
        else:
            self.logable = False

logger = log()

def put_text(objects,arg="nothing",color="no"):
    global logger
    colorn = ""
    types ="INFO"
    if color =="green":
        colorn="#32CD32"
        types ="<font color =\"{}\"> OK </font>".format(colorn)
    elif color =="blue":
        colorn="#0000FF"
        types ="<font color =\"{}\"> TRY </font>".format(colorn)
    elif color =="yellow":
        colorn="#FF8303"
        types ="<font color =\"{}\"> REPLY </font>".format(colorn)
    elif color =="red":
        colorn="#DC143C"
        types ="<font color =\"{}\"> ERROR </font>".format(colorn)

    if type(objects) is bytes:
        print(objects.decode("utf-8"))
        objects=objects.decode("utf-8")
    else:
        print(objects)
    if arg != "noshow":
            if color != "no":
                log_new = "\n" + "<font color =\"{}\">".format(colorn) + objects + "</font>"
                logger.logs += log_new
            else:
                log_new = "\n"+objects
                logger.logs += log_new
    if logger.logable and arg != "noshow":
        try:
            if color != "no":
                logger.window.logEdit.appendHtml(log_new)
            else:
                logger.window.logEdit.appendHtml(log_new)

            time_str = str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
            with open("log.html",'a',encoding='utf-8') as f:
                f.write("[{}][time:{}]:{} <br>".format(types,time_str,str(log_new)))
            f.close()
        except Exception as e:
            print(str(e))
        
