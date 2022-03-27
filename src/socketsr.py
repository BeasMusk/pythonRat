import os
import struct


def sendData(sock, data, fileId=11):
    if type(data) == str:
        data = data.encode('gbk')

    data = struct.pack('>2I', len(data), fileId) + data
    sock.send(data)


def recvAll(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def receiveData(sock):
    receivePack = recvAll(sock, 8)
    if receivePack is None:
        return None

    receivePack = struct.unpack('>2I', receivePack)
    dataLength = receivePack[0]
    fileId = receivePack[1]
    result = recvAll(sock, dataLength).decode('gbk')
    if fileId == 22:
        savePath = result
        try:
            with open(savePath, 'wb') as f:
                while True:
                    receivePack = recvAll(sock, 8)
                    receivePack = struct.unpack('>2I', receivePack)
                    dataLength = receivePack[0]
                    result = recvAll(sock, dataLength)
                    if result == b'end000000':
                        f.close()
                        return 1
                    f.write(result)

        except Exception as e:
            return 1

    if fileId == 33:
        FilePath = result.split('\'')
        localFilePath = FilePath[0]
        savePath = FilePath[2]
        uploadFile(sock, localFilePath, savePath)

    if fileId == 11:
        return result


def uploadFile(sock, uploadFileName, savePath, statusBarShowSignal=None):
    fileSize = os.path.getsize(uploadFileName)
    data = f'{savePath}'
    sendData(sock, data, fileId=22)
    with open(uploadFileName, 'rb') as f:
        res = f.read(4096)
        while len(res):
            sendData(sock, res)
            res = f.read(4096)
        f.close()
        sendData(sock, b'end000000')
        if statusBarShowSignal:
            statusBarShowSignal.emit('send done', 1)


def downFile(sock, remoteFilePath, savePath, statusBarShowSignal=None):
    data = f'{remoteFilePath}\'{savePath}'
    sendData(sock, data, fileId=33)
    receiveData(sock)
    if statusBarShowSignal:
        statusBarShowSignal.emit('download done', 1)
