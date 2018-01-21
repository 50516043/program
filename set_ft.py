# -*- coding: utf-8 -*-
# client3.py
# python3 client3.py HostName PortNumber

from socket import *
import time
import sys
ft_port = 54900

def main():#main

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(('pbl1, ft_port))
    client_socket.send('BANDWIDTH CALCULATION \n'.encode())
    client_socket.close()
            
if __name__ == '__main__':
     main()