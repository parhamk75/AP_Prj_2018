import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import os



Form = uic.loadUiType(os.path.join(os.getcwd(),'TMP_1.ui'))[0]

def func_1():
    print("Hallo!!!")
#    app.closeAllWindows()
    

class Matplotlib(Form, QMainWindow):
    def __init__(self):
        Form.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.commandLinkButton.clicked.connect(func_1)


app = QApplication(sys.argv)
w = Matplotlib()
w.show()



sys.exit(app.exec_())