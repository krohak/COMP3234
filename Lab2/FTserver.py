#!/usr/bin/python

import socket
import sys

def main(argv):
	# set port number
	# default is 32341 if no input argument
	if len(argv) == 2:
		port = int(argv[1])
	else:
		port = 32341


	# create socket and bind
	sockfd = socket.socket()
	sockfd.settimeout(1)
	try:
		sockfd.bind(('', port))
	except socket.error as emsg:
		print("Socket bind error: ", emsg)
		sys.exit(1)

	# listen and accept new connection
	sockfd.listen(5)

	while True:
		try:
			conn, addr = sockfd.accept()
		except socket.timeout:
			print("Still waiting for connection request!")
			continue
		except socket.error as emsg:
			print("Socket accept error: ", emsg)
			sys.exit(1)
		else:
			break

	# print out peer socket address information
	print("Connection established. Here is the remote peer info:", addr)

	sockfd.settimeout(None)

	# receive file name, file size; and create the file
	try:
		rmsg = conn.recv(100)
	except socket.error as emsg:
		print("Socket recv error: ", emsg)
		sys.exit(1)
	if rmsg == b'':
		print("Connection is broken")
		sys.exit(1)
	
	fname, filesize = rmsg.split(b':')
	print("Open a file with name \'%s\' with size %s bytes" % (fname.decode("ascii"), filesize.decode("ascii")))
	try:
		fd = open(fname, "wb")
	except IOerror as emsg:
		print("File open error: ", emsg)
		sys.exit(1)

	# send acknowledge - e.g., "OK"
	conn.send(b"OK")

	# receive the file contents
	print("Start receiving . . .")
	remaining = int(filesize)
	while remaining > 0:
		rmsg = conn.recv(1000)
		if rmsg == b"":
			print("Connection is broken")
			sys.exit(1)
		fd.write(rmsg)
		remaining -= len(rmsg)

	# close connection
	print("[Completed]")
	sockfd.close()
	conn.close()
	fd.close()

if __name__ == '__main__':
	if len(sys.argv) > 2:
		print("Usage: FTserver [<Server_port>]")
		sys.exit(1)
	main(sys.argv)