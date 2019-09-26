import socket
import sys
import os
import time
import threading
import platform
import math

# TYPE (4 bits)
# ID (4 bits)
# SEQUENCE NUMBER (16 bits)
# LENGTH (16 bits)
# Checksum (16 bits)
# DATA (32KB/32768 bytes max)

TIMEOUT = 2
PACKETSIZE = 32768
# sys.setrecursionlimit(150000)
# UDP_IP_ADDRESS = "127.0.0.1"
# UDP_PORT_NO = 9999

def sendfile(filepath, fileid, ipaddress, inputPort):
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    senderaddress = ipaddress

    s.settimeout(TIMEOUT)

    f = open (filepath, "rb")

    n = 0
    send1 = True

    nextData = f.read(PACKETSIZE)

    totalPackets = os.path.getsize(filepath) / PACKETSIZE
    totalSent = n


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

        packetIDandType = bytearray(1)
        packetIDandType[0] = typ[0] + fileid
        packetLength = (len(currentData)).to_bytes(2, byteorder='big')
        packetSequenceNumber = n.to_bytes(2, byteorder='big')
        packetChecksum = checksum(packetIDandType + packetSequenceNumber + packetLength + currentData)

        recursiveSend(packetIDandType, packetSequenceNumber, packetLength, packetChecksum, currentData, s, n, senderaddress, inputPort)
        totalSent = n
        printprogress(totalSent, totalPackets, fileid)

    s.close()
    
def recursiveSend(packetIDandType, packetSequenceNumber, packetLength, packetChecksum, currentData, s, n, senderaddress, inputPort):
    try:
        data = packetIDandType + packetSequenceNumber + packetLength + packetChecksum + currentData

        sendpacket(data, s, senderaddress, inputPort)
        returnedPacket, senderaddress = s.recvfrom(40000)
        if (returnedPacket[0] >> 4) != 1 and (returnedPacket[0] >> 4) != 3:
            raise Exception('Packet received was not an acknowledgement packet')
        
            # print('ACKNOWLEDGED' + str(returnedPacket[0] >> 4))
    except Exception as inst:
        # print(inst.args)
        # print('RESENT PACKET NUMBER: ' + str(n))
        recursiveSend(packetIDandType, packetSequenceNumber, packetLength, packetChecksum, currentData, s, n, senderaddress, inputPort)
    
def xorBytes(xorMaterial):
    returnXor = xorMaterial[0]
    for x in range(0, len(xorMaterial) - 2, 2):
        returnXor = returnXor ^ xorMaterial[x+2]
    return returnXor

def checksum(xorMaterial):
    return (bytes([xorBytes(xorMaterial)]) + bytes([xorBytes(xorMaterial[1:len(xorMaterial)])]) ) 

def sendpacket(data, socket, senderaddress, inputPort):
    socket.sendto(data, (senderaddress, inputPort))

def clearscreen():
    if platform.system() == "Linux" or platform.system() == "Darwin":
        os.system('clear')
    if platform.system() == "Windows":
        os.system('cls')

def printprogress(current, total, fileid):
    clearscreen()

    prog = math.floor(current/total * 100)

    for _ in range(0, fileid*5):
        print()
    print("TOTAL PACKET: " + str(total))
    print("CURRENT PACKET: " + str(current))
    print("PERCENTAGE SENT: " + str(prog))


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

main()