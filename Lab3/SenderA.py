#!/usr/bin/python3
"""SenderA - this process composes a message with binary data
   and sends it to a communication pipe, which changes the
   contents before sends the updated message to Receiver B
"""

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
	msg = struct.pack('cBi', b'A', 10, socket.htonl(4444))

	# create socket and connect to Comm_pipe
	try:
		sockfd = socket.socket() # AF_INET, socket.SOCK_STREAM are default for socket.socket
		sockfd.connect((argv[1], int(argv[2])))
	except socket.error as emsg:
		print("Socket error: ", emsg)
		sys.exit(1)

	# once the connection is established; print out
	# the socket addresses of your local socket and
	# the Comm_pipe
	print("Connection established. My socket address is {} and Comm_pipe address is {}".format(sockfd.getsockname(), sockfd.getpeername()))

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
