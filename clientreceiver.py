import socket
import sys
import threading

MAXPACKETSIZE = 40000

def xorBytes(xorMaterial):
    returnXor = xorMaterial[0]
    for x in range(0, len(xorMaterial) - 2, 2):
        returnXor = returnXor ^ xorMaterial[x+2]
    return returnXor


def checksum(xorMaterial):
    return (bytes([xorBytes(xorMaterial)]) + bytes([xorBytes(xorMaterial[1:len(xorMaterial)])]) ) 

def receivefile(inputPort):
    soc = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    soc.bind(('', inputPort))

    obtainedFiles = []
    allRecvPacket = []
    fileArrays = []

    notFin = True

    print("ASSIGNED IP ADDRESS IS :" )
    print(socket.getfqdn())

    while True:
        while notFin:       
            receivedPacket, senderaddress = soc.recvfrom(MAXPACKETSIZE)
            print("PACKET RECEIVED!")
            print(receivedPacket[0:8])
            print(soc.getsockname())

            receivedPacketType = receivedPacket[0] >> 4
            receivedPacketID = receivedPacket[0] - receivedPacketType*16

            print("RECEIVED PACKET TYPE")
            print(receivedPacketType)
            print("RECEIVED PACKET ID")
            print(receivedPacketID)

            if receivedPacketID not in obtainedFiles:
                obtainedFiles.append(receivedPacketID)
                while len(fileArrays) <= receivedPacketID:
                    sublist = []
                    fileArrays.append(sublist)
            if receivedPacket[5:7] == checksum(receivedPacket[0:5] + receivedPacket[7:len(receivedPacket)]):
                allRecvPacket.append(receivedPacket)
                responsePacket = bytes([receivedPacketType + 16])
                responsePacket += receivedPacket[1:len(receivedPacket)]
                
                # soc2.send(responsePacket)
                soc.sendto(responsePacket, senderaddress)
                print('RESPONSE SENT')
                print(responsePacket[0:8])

                print('FILE ARRAYS LEN: ' + str(len(fileArrays)))
                print('PACKET ID: ' + str(receivedPacketID))
                fileArrays[receivedPacketID].append(receivedPacket)

                if receivedPacketType == 1:
                    # FIN
                    packetForCurrentID = []
                    
                    writetofile = bytearray([])
                    f = open ("Response" + str(receivedPacketID), "wb")
                    for packet in fileArrays[receivedPacketID]:
                        packetForCurrentID.append((packet, int.from_bytes(packet[1:3], 'big')))
                    
                    sortedPacketForCurrentID = Sort_Tuple(packetForCurrentID)
                    for packet in sortedPacketForCurrentID:
                        print(len(packet[0]))
                        writetofile += packet[0][7:len(packet[0])]
                    print("EL DATO:")
                    f.write(writetofile)
                    f.close()
            else:
                print('CHECKSUM ERROR')
    soc.close()
    # soc2.close()

def Sort_Tuple(tup):  
    tup.sort(key = lambda x: x[1])  
    return tup
    
def main():
    inputPort = input("Masukan PORT :")
    receivefile(int(inputPort))

main()