#!/usr/bin/python

import socket
import sys

def main(argv):
	# set port number
	# default is 32341 if no input argument


	# create socket and bind


	# listen and accept new connection


	# print out peer socket address information


	# receive file name, file size; and create the file


	# send acknowledge - e.g., "OK"


	# receive the file contents
	print("Start receiving . . .")


	# close connection
	print("[Completed]")


if __name__ == '__main__':
	if len(sys.argv) > 2:
		print("Usage: FTserver [<Server_port>]")
		sys.exit(1)
	main(sys.argv)