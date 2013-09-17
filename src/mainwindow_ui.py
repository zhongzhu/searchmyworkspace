# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon Sep 16 15:41:28 2013
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(615, 486)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_search = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.horizontalLayout.addWidget(self.lineEdit_search)
        self.pushButton_search = QtGui.QPushButton(self.centralwidget)
        self.pushButton_search.setAutoDefault(True)
        self.pushButton_search.setDefault(True)
        self.pushButton_search.setObjectName("pushButton_search")
        self.horizontalLayout.addWidget(self.pushButton_search)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.treeView_facet = QtGui.QTreeView(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView_facet.sizePolicy().hasHeightForWidth())
        self.treeView_facet.setSizePolicy(sizePolicy)
        self.treeView_facet.setObjectName("treeView_facet")
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_searchResult = QtGui.QLabel(self.widget)
        self.label_searchResult.setObjectName("label_searchResult")
        self.verticalLayout.addWidget(self.label_searchResult)
        self.listView_result = QtGui.QListView(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_result.sizePolicy().hasHeightForWidth())
        self.listView_result.setSizePolicy(sizePolicy)
        self.listView_result.setObjectName("listView_result")
        self.verticalLayout.addWidget(self.listView_result)
        self.verticalLayout_2.addWidget(self.splitter)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 615, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.lineEdit_search, QtCore.SIGNAL("returnPressed()"), self.pushButton_search.click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Search:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_search.setText(QtGui.QApplication.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.label_searchResult.setText(QtGui.QApplication.translate("MainWindow", "Search Results:", None, QtGui.QApplication.UnicodeUTF8))

