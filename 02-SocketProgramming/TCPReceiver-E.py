#!/usr/bin/python3

import socket

sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# use "" means listening to all adapters in this machine
# only valid for IPv4
sockfd.bind( ("", 32341) )

print("I_am", socket.gethostname(), "and_I_am_listening_...")

sockfd.listen(5)
new, who = sockfd.accept() # Return the TCP connection

print("A_connection_with", who, "has_been_established")

try:
	message = new.recv(50)
except socket.error as err:
	print("Recv error: ", err)
	
if message:
	print("\'"+message.decode("ascii")+"\'", "is received from", who)
else:
	print("Connection is broken")

new.close()
sockfd.close()
