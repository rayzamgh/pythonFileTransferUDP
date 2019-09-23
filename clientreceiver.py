import socket
import sys


def receivefile():
    soc = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    soc.bind(("localhost",9999))

    n = 0
    f = open("niggerreceivenew.txt",'wb')
    
    for _ in range(3):       
        l = soc.recv(40000)
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