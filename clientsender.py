import socket
import sys
import os
import time
import threading

# TYPE (4 bits)
# ID (4 bits)
# SEQUENCE NUMBER (16 bits)
# LENGTH (16 bits)
# Checksum (16 bits)
# DATA (32KB/32768 bytes max)

TIMEOUT = 10
PACKETSIZE = 32768
# sys.setrecursionlimit(150000)
# UDP_IP_ADDRESS = "127.0.0.1"
# UDP_PORT_NO = 9999

def sendfile(filepath, fileid, ipaddress, inputPort):
    # r = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    senderaddress = ipaddress

    # SET TIME OUT HERE
    s.settimeout(TIMEOUT)

    f = open (filepath, "rb")

    n = 0
    send1 = True

    nextData = f.read(PACKETSIZE)

    while(send1):
        n = n + 1
        # print('sent packet number' + str(n))
        currentData = nextData
        nextData    = f.read(PACKETSIZE)

        if nextData == b'':
            typ = b'\x10'
            send1 = False
        else:
            typ = b'\x00'

        # print("DATA SIZE:")
        # print(len(currentData))

        packetIDandType = bytearray(1)
        packetIDandType[0] = typ[0] + fileid
        packetLength = (len(currentData)).to_bytes(2, byteorder='big')
        packetSequenceNumber = n.to_bytes(2, byteorder='big')
        packetChecksum = checksum(packetIDandType + packetSequenceNumber + packetLength + currentData)

        # print("TYPE AND ID:")
        # print(packetIDandType)

        # print("SEQUENCE NUMBER:")
        # print(packetSequenceNumber)

        recursiveSend(packetIDandType, packetSequenceNumber, packetLength, packetChecksum, currentData, s, n, senderaddress, inputPort)

    s.close()
    
def recursiveSend(packetIDandType, packetSequenceNumber, packetLength, packetChecksum, currentData, s, n, senderaddress, inputPort):
    try:
        data = packetIDandType + packetSequenceNumber + packetLength + packetChecksum + currentData
        # print("DATA:")
        # print(data[0:8])
        sendpacket(data, s, senderaddress, inputPort)
        returnedPacket, senderaddress = s.recvfrom(40000)
        # print("RESPONSE RECEIVED")
        if (returnedPacket[0] >> 4) != 1 and (returnedPacket[0] >> 4) != 3:
            raise Exception('Packet received was not an acknowledgement packet')
        else:
            # print('ACKNOWLEDGED' + str(returnedPacket[0] >> 4))
    except Exception as inst:
        # print(inst.args)
        # print('RESENT PACKET NUMBER: ' + str(n))
        recursiveSend(packetIDandType, packetSequenceNumber, packetLength, packetChecksum, currentData, s, n, senderaddress, inputPort)
    

# def xorBytes(xorMaterial):
#     # print(len(xorMaterial))
#     if len(xorMaterial) <= 2:
#         return (xorMaterial[0])
#     else:
#         return (xorMaterial[0] ^ xorBytes(xorMaterial[2:len(xorMaterial)]))

def xorBytes(xorMaterial):
    returnXor = xorMaterial[0]
    for x in range(0, len(xorMaterial) - 2, 2):
        returnXor = returnXor ^ xorMaterial[x+2]
    return returnXor

def checksum(xorMaterial):
    return (bytes([xorBytes(xorMaterial)]) + bytes([xorBytes(xorMaterial[1:len(xorMaterial)])]) ) 

def sendpacket(data, socket, senderaddress, inputPort):
    socket.sendto(data, (senderaddress, inputPort))

def main():
    threads = []
    filenames = []
    inputAddr = input("Input Address :")
    inputPort = input("Input Port : ")
    for _ in range(0, int(input("Berapa filenya? "))):
        filenames.append(input("File name : "))
    for i in range(0, len(filenames)):
        t = threading.Thread(target=sendfile, args=(filenames[i] ,i,inputAddr, int(inputPort)))
        threads.append(t)
        t.start()
    # sendfile(fileName, 0, inputAddr, int(inputPort))


main()