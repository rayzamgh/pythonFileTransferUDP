import socket
import sys
import os

# TYPE (4 bits)
# ID (4 bits)
# SEQUENCE NUMBER (16 bits)
# LENGTH (16 bits)
# Checksum (16 bits)
# DATA (32KB/32768 bytes max)


def sendfile(filepath, port):
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    s.connect(("localhost",port))
    f = open (filepath, "rb")

    n = 0
    
    while(not EOF):
        n = n + 1

        packetData = f.read(32768)
        packetID = bin()
        packetLength = os.path.getsize(filepath)
        packetSequenceNumber = n
        packetChecksum = checksum(packetData, packetLength, packetSequenceNumber, packetData)

        sendpacket()

    l = f.read(1024)
    
def checksum(packetData, packetLength, packetSequenceNumber, packetData):


def sendpacket(packetType, packetSequenceNumber, packetLength, packetChecksum, packetData)

while (l):
    print(l)
    s.send(l)
    n = n + 1
    l = f.read(1024)
    print("Sent iteration" + str(n))
s.close()