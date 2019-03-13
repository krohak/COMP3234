#!/usr/bin/python3

import socket
import threading

def thd_func(client):
	new, who = client
	print("A_connection_with", who, "has_been_established")
	message = new.recv(50)
	print("\'"+message.decode("ascii")+"\'", "is received from", who)
	new.close()

sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd.bind( ("", 32341) )
print("I_am", socket.gethostname(), "and_I_am_listening_...")

sockfd.listen(5)

while (True):
	client = sockfd.accept()
	newthd = threading.Thread(target=thd_func, args=(client,))
	newthd.start()

sockfd.close()
