#!/usr/bin/python3

import socket
import struct
import sys

def main(argv):

	# compose the message
	# The message should consists of three components in the following order:
	# struct {
	#	char val1
	#	unsigned char val2
	#	int val3
	# }
	#
	# Assign 'A' to val1, 10 to val2, and 4444 to val3
	message_format = struct.Struct('cBi')
	msg = message_format.pack(b'A', 10, socket.htonl(4444))
	print("The message (raw):", msg)

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

	# send the message
	sockfd.send(msg)

	# close connection
	sockfd.close()
	
	print("[Completed]")


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Usage: SenderA.py <Comm_pipe IP> <Comm_pipe port>")
		sys.exit(1)
	main(sys.argv)
