# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 00:23:54 2021

@author: Correct
"""

# client
import socket
import numpy as np
import struct

hostIp = '192.168.0.101' # Use ip address from the server
hostPort = 2000 # Use pc port from the server
serverAddress = (hostIp, hostPort) # create (tuple)

print()
print("ip address: ", hostIp)
print("pc poort: ", hostPort)
print()

# Create TCP socket & connect to host
tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSocket.connect(serverAddress)

hoek = 300.58
hoek_plaats = 45.09
yPos = 2.223
xPos = 1.4
yPos_2 = 3.5
xPos_2 = 1.3
bakje_klaar = True 
message = [hoek_plaats,xPos, yPos, hoek, xPos_2, yPos_2]
data = struct.pack(">ffffff", *message)
messageLength = tcpSocket.send(data)
#messageLength = tcpSocket.send(data.encode())
 
serverReply = tcpSocket.recv(2048) # Deze regel moet veranderen
c_new = struct.unpack(">f", serverReply)
print(c_new)
c_array = np.asarray(c_new)


print("Answer from server:", c_array)
print()
tcpSocket.close() # the complete tcpSocket is deleted
print("connection closed")

# end of client program