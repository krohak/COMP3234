#!/usr/bin/python3

import socket
import sys

sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# "localhost" means the loopback device of this machine, 
# which uses the IP addr 127.0.0.1
try:
	sockfd.connect( ("localhost", 32341) )
except socket.error as err:
	print("Connection error: ", err)
	sys.exit(1)

print("The_connection_with", sockfd.getpeername(), \
"has_been_established")

# Get input for sending
try:
	msg = input("Enter your message --> ")
except:
	print("Terminated abnormally!!")
	sockfd.close()
	sys.exit(1)

sockfd.send(msg.encode("ascii"))

sockfd.close()
