# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testcaseviewer.ui'
#
# Created: Tue Sep 24 17:09:33 2013
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow_TestCaseViewer(object):
    def setupUi(self, MainWindow_TestCaseViewer):
        MainWindow_TestCaseViewer.setObjectName("MainWindow_TestCaseViewer")
        MainWindow_TestCaseViewer.resize(690, 574)
        self.centralwidget = QtGui.QWidget(MainWindow_TestCaseViewer)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit_viewer = QtGui.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.textEdit_viewer.setFont(font)
        self.textEdit_viewer.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textEdit_viewer.setObjectName("textEdit_viewer")
        self.verticalLayout.addWidget(self.textEdit_viewer)
        MainWindow_TestCaseViewer.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow_TestCaseViewer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 690, 20))
        self.menubar.setObjectName("menubar")
        MainWindow_TestCaseViewer.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow_TestCaseViewer)
        self.statusbar.setObjectName("statusbar")
        MainWindow_TestCaseViewer.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_TestCaseViewer)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_TestCaseViewer)

    def retranslateUi(self, MainWindow_TestCaseViewer):
        MainWindow_TestCaseViewer.setWindowTitle(QtGui.QApplication.translate("MainWindow_TestCaseViewer", "Test Case Viewer", None, QtGui.QApplication.UnicodeUTF8))

