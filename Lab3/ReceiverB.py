#!/usr/bin/python3
""" Receiver B - this process first connects to the
    communication pipe and then waits for a message
	from the pipe. Once gets the message, print out
	the contents to the output display.
"""

import socket
import struct
import sys

def main(argv):

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


	# receive the message
	buf = sockfd.recv(1024)


	# print out the message contents
	msg = struct.unpack('cBi', buf)
	print("The value in the char field: ", msg[0])
	print("The value in the unsigned char field: ", msg[1])
	print("The value in the int field: ", socket.ntohl(msg[2]))


	# close connection
	sockfd.close()


	print("[Completed]")


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Usage: ReceiverB.py <Comm_pipe IP> <Comm_pipe port>")
		sys.exit(1)
	main(sys.argv)
