import struct


def sendData(sock, data):
    if type(data) == str:
        data = data.encode('gbk')

    data = struct.pack('>I', len(data)) + data
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
    dataLength = recvAll(sock, 4)
    if dataLength is None:
        return None

    dataLength = struct.unpack('>I', dataLength)[0]
    result = recvAll(sock, dataLength).decode('gbk')
    return result
