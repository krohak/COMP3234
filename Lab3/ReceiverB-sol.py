#!/usr/bin/python3

import socket
import struct
import sys

def main(argv):

	# create socket and connect to Comm_pipe
	try:
		sockfd = socket.socket()
		sockfd.connect((argv[1], int(argv[2])))
	except socket.error as emsg:
		print("Socket error: ", emsg)
		sys.exit(1)

	# once the connection is established; print out
	# the socket addresses of your local socket and
	# the Comm_pipe
	print("Connection established.")
	print("My socket address is", sockfd.getsockname())
	print("Comm_pipe socket address is", sockfd.getpeername())

	# receive the message
	rmsg = sockfd.recv(32)

	# print out the message contents
	print("The received message (raw):", rmsg)
	message_format = struct.Struct('cBi')
	(val1, val2, val3) = message_format.unpack(rmsg)
	print("The value in the char field: ", val1)
	print("The value in the unsigned char field: ", val2)
	print("The value in the int field: ", socket.ntohl(val3))

	# close connection
	sockfd.close()
	
	print("[Completed]")


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Usage: ReceiverB.py <Comm_pipe IP> <Comm_pipe port>")
		sys.exit(1)
	main(sys.argv)
