import socket
import sys
import os

# TYPE (4 bits)
# ID (4 bits)
# SEQUENCE NUMBER (16 bits)
# LENGTH (16 bits)
# Checksum (16 bits)
# DATA (32KB/32768 bytes max)


def sendfile(filepath, fileid):
    f = open (filepath, "rb")

    n = 0
    send1 = True
    while(send1):
        n = n + 1

        packetData = f.read(10)
        packetID = bytearray(fileid, 'utf-8')
        packetLength = bytearray(str(os.path.getsize(filepath)), 'utf-8')
        packetSequenceNumber = bytearray(str(n), 'utf-8')
        packetType = bytearray('pepeg', 'utf-8')
        # packetChecksum = checksum(packetData, packetLength, packetSequenceNumber, packetData)

        sendpacket(packetType + packetID + packetSequenceNumber + packetLength + packetData)
        if n == 3:
            send1 = False
    
# def checksum(packetData, packetLength, packetSequenceNumber, packetData):


def sendpacket(data):
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    s.connect(("localhost",9999))

    s.send(data)
    print("Sent data :" + str(data))

sendfile("nigger.txt", "1")