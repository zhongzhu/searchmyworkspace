import sys
from PySide import QtCore
from PySide import QtGui
import mainwindow

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    
    app.setApplicationName("Search My Workspace")
    mainwindow = mainwindow.MainWindow()
    mainwindow.show()
    
    sys.exit(app.exec_())