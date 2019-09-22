import socket
import sys


def receivefile():
    soc = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    soc.bind(("localhost",6969))

    n = 0
    f = open("niggerreceive.txt",'wb')
    
    while (True):       
        l = soc.recv(1024)
        # while (l):
        print(l)
        f.write(l)
        print("WRITTEN IN FILE :")
        print(f)
        # l = soc.recv(1024)
        n = n + 1
        print("Received iteration" + str(n))
        f.close()
    soc.close()

receivefile()