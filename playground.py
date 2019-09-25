import sys
import os
import threading
import time
import socket

y = bytearray([])
# for x in range(3):
#     y = y + bytearray([x])
y = y + bytearray([1, 2, 3, 4, 5, 6])

def xorBytes(xorMaterial):
    if len(xorMaterial) <= 2:
        return (xorMaterial[0])
    else:
        return (xorMaterial[0] ^ xorBytes(xorMaterial[2:len(xorMaterial)]))

def xorPer2(xorMaterial):
    return (bytes([xorBytes(xorMaterial)]) + bytes([xorBytes(xorMaterial[1:len(xorMaterial)])]) ) 

# print(y)
# print(xorBytes(y))
# print(xorBytes(y[1:len(y)]))
# print(xorPer2(y))
# print(int.from_bytes(y, 'big'))

# for x in bytearray(b'\x14\x00\x04\x00\x03_\rALL'):
#     print(x)


def timeoutTimer(timeoutTime):
    time.sleep(timeoutTime)
    print('pepeg')
    return True

timeoutTime = 1
packetReturned = False
timeout = False

soc = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)    
soc.bind(("localhost",9999))
soc.settimeout(1)

try:
    rec = soc.recv(1000)
except:
    print('pepeg')

soc.close()
