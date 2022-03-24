# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindows.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(795, 377)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("scientist.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.twClient = QtWidgets.QTableWidget(self.centralwidget)
        self.twClient.setFocusPolicy(QtCore.Qt.NoFocus)
        self.twClient.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.twClient.setFrameShape(QtWidgets.QFrame.Panel)
        self.twClient.setFrameShadow(QtWidgets.QFrame.Raised)
        self.twClient.setLineWidth(0)
        self.twClient.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twClient.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.twClient.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.twClient.setShowGrid(False)
        self.twClient.setGridStyle(QtCore.Qt.CustomDashLine)
        self.twClient.setRowCount(0)
        self.twClient.setObjectName("twClient")
        self.twClient.setColumnCount(6)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setUnderline(False)
        item.setFont(font)
        self.twClient.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.twClient.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.twClient.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.twClient.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.twClient.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.twClient.setHorizontalHeaderItem(5, item)
        self.twClient.horizontalHeader().setVisible(True)
        self.twClient.horizontalHeader().setCascadingSectionResizes(False)
        self.twClient.horizontalHeader().setDefaultSectionSize(100)
        self.twClient.horizontalHeader().setHighlightSections(False)
        self.twClient.horizontalHeader().setMinimumSectionSize(10)
        self.twClient.horizontalHeader().setSortIndicatorShown(False)
        self.twClient.horizontalHeader().setStretchLastSection(True)
        self.twClient.verticalHeader().setVisible(False)
        self.twClient.verticalHeader().setCascadingSectionResizes(False)
        self.twClient.verticalHeader().setDefaultSectionSize(20)
        self.twClient.verticalHeader().setHighlightSections(False)
        self.twClient.verticalHeader().setMinimumSectionSize(20)
        self.twClient.verticalHeader().setStretchLastSection(False)
        self.horizontalLayout.addWidget(self.twClient)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 795, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PythonRAT"))
        item = self.twClient.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Id"))
        item = self.twClient.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ComputerName"))
        item = self.twClient.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "UserName"))
        item = self.twClient.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Lan"))
        item = self.twClient.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Wan"))
        item = self.twClient.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "OS"))