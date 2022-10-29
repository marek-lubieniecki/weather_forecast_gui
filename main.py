from mainWindow import *
from PyQt5 import QtGui

app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('main_icon.png'))
window = MainWindow()
window.show()
app.exec()
