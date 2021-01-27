""" Realizado por Arturo Alcaniz Guijarro (DNI: 04634824W) """
#!/usr/bin/env python3
import os
import time
import struct
import socket
import select
import hashlib
import base64
import requests
from urllib.parse import unquote
from threading import Thread
from sys import *
from socket import *
from multiprocessing import Process, current_process

""" Web Server Get """
def iniciarWebServer(puerto):
	WebServerSocket = socket(AF_INET, SOCK_STREAM)
	WebServerSocket.bind(('', puerto))
	print("Web Server iniciado en el puerto {}".format(puerto))
	listenRequestWebServer(WebServerSocket)
	WebServerSocket.close()

def listenRequestWebServer(WebSocket):

	begin = time.time()
	threads = []
	while True:
		WebSocket.listen(1)
		time.sleep(0.1)
		client, address = WebSocket.accept()
		client.settimeout(10)
		msg = client.recv(65000)

		try:
			t = Thread(target=manejarRequestWebServer, args=(msg, client, ))
			t.start()
			""" guardamos el thread para luego esperar que termine """
			threads.append(t)
		except:
			print("Error en la creacion de thread. Reintentando creacion...")
			tim.sleep(1)
			t = Thread(target=manejarRequestWebServer, args=(msg, client, ))
			t.start()
			threads.append(t)

	""" Esperamos a que todos los thread hayan terminado """
	for x in threads:
		x.join()
	WebSocket.close()

def manejarRequestWebServer(msg, client):
	data = msg.decode()
	if not data:
		exit()
	peticion = data.split(' ')[0]
	if peticion == "GET":
		fichero = data.split(' ')[1]
		if fichero[0:8] == "/submit?":
			reto7(unquote(fichero[8:]))
		else:
			request = requests.get('https://uclm-arco.github.io/ietf-clone/rfc' + fichero)
			hora_actual = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
			if request.status_code == 200:
				print(str(client.getsockname()) + " pide " + fichero + " -> 200OK")
				header = 'HTTP/1.1 200 OK\n'
				header += 'Date: {}\n'.format(hora_actual)
				header += 'Server: Web Server Request\n'
				header += 'Connection: close\n'
				client.send(header.encode())
				client.close()
			elif request.status_code == 404:
				print(str(client.getsockname()) + " pide " + fichero + " -> 404 Not Found")
				header = 'HTTP/1.1 404 Not Found\n'
				header += 'Date: {}\n'.format(hora_actual)
				header += 'Server: Web Server Request\n'
				header += 'Connection: close\n'
				client.send(header.encode())
				client.close()

""" Funciones proporcionadas para el checksum """
def sum16(data):
	if len(data) % 2:
		data = b'\0' + data
	return sum(struct.unpack('!%sH' % (len(data) // 2), data))

def cksum(data):
	sum_as_16b_words = sum16(data)
	sum_1s_complement = sum16(struct.pack('!L', sum_as_16b_words))
	_1s_complement = ~sum_1s_complement & 0xffff
	return _1s_complement



def encontrarPuertoLibre():
	sockn = socket(AF_INET, SOCK_DGRAM)
	sockn.bind(('', 0))
	puerto = sockn.getsockname()[1]
	sockn.close()
	return puerto

def recibirMensaje():
	msg = sock.recv(1024)
	texto = msg.decode("utf-8")
	print(texto)
	return texto.split("\n")

def inicio():
	sock.sendall("arturo.alcaniz1".encode())

def reto1(puerto):
	process = Process(target=serverUDP, args=(puerto,))
	processes.append(process)
	process.start()

def contarNumeros(socknumbers):
	cantidad = 0
	texto = ""
	zeroEncontrado = False

	while zeroEncontrado == False:
		data = socknumbers.recv(512)
		texto = texto + data.decode("utf-8")

		if(texto[len(texto)-1:len(texto)] == " "):
			numeros = texto[0:len(texto)-1].split()
			texto = texto[len(texto)-1:len(texto)]

		elif(texto[len(texto)-2:len(texto)-1] == " "):
			numeros = texto[0:len(texto)-2].split()
			texto = texto[len(texto)-2:len(texto)]

		elif(texto[len(texto)-3:len(texto)-2] == " "):
			numeros = texto[0:len(texto)-3].split()
			texto = texto[len(texto)-3:len(texto)]

		elif(texto[len(texto)-4:len(texto)-3] == " "):
			numeros = texto[0:len(texto)-4].split()
			texto = texto[len(texto)-4:len(texto)]

		for num in numeros:

			if num == "0":
				zeroEncontrado = True
				break

			cantidad += 1

	return cantidad

def handle(sock, msg, client, n):
	print("Nueva peticion", n, client)
	time.sleep(1)
	mensaje = msg.decode("utf-8")
	print(mensaje)

	if n == 1:
		texto = mensaje.split("\n")
		linea = texto[0]
		codigo = linea[5:]
		socknumbers = socket(AF_INET, SOCK_STREAM)
		socknumbers.connect(('node1', 4001))
		cantidad = contarNumeros(socknumbers)
		info = codigo + " " + str(cantidad)
		socknumbers.sendall(info.encode())
		time.sleep(1)
		respuesta = socknumbers.recv(50024)
		respuestadeco = respuesta.decode("utf-8")
		print(respuestadeco)
		time.sleep(0.1)
		reto3(respuestadeco)

def getCode(texto):
	posInicial = 0
	for i in range(0, len(texto)):
		if(texto[i:i+5] == "code:"):
			posInicial = i+5
			break
	posFinal = posInicial
	for i in range(posInicial, len(texto)):
		if(texto[i:i+1] == "\n") or (texto[i:i+1] == " "):
			posFinal = i
			break
	return texto[posInicial:posFinal]

def reto3(texto):
	texto = getPosInicioReto(texto)
	posInicial = 0
	for i in range(0, len(texto)):
		if(texto[i:i+5] == "code:"):
			posInicial = i+5
			break
	posFinal = posInicial
	for i in range(posInicial, len(texto)):
		if(texto[i:i+1] == "\n") or (texto[i:i+1] == " "):
			posFinal = i
			break

	codigo = "--" + texto[posInicial:posFinal] + "--"
	sockPalindromos = socket(AF_INET, SOCK_STREAM)
	sockPalindromos.connect(('node1', 6000))
	texto = ""
	textoEntero = ""
	palindromoEncontrado = False
	time.sleep(1)
	texto = getAllInfo(sockPalindromos, 0.5)
	textoPartido = texto.split()

	for i in range(0, len(textoPartido)-1):
		if (textoPartido[i].isdigit() == False and textoPartido[i] == alReves(textoPartido[i]) and len(textoPartido[i])>1):
			break

		else:
			if i == 0:
				if textoPartido[i].isdigit():
					textoEntero += textoPartido[i]
				else:
					textoEntero += alReves(textoPartido[i])
			else:
				if textoPartido[i].isdigit():
					textoEntero += " " + textoPartido[i]
				else:
					textoEntero += " " + alReves(textoPartido[i])

	sockPalindromos.sendall((textoEntero + codigo).encode())
	msgResponse = getAllInfo(sockPalindromos, 0.6)
	reto4(msgResponse)

def reto4(msgResponse):
	print(msgResponse)
	lineas = msgResponse.split("\n")
	linea = lineas[0]
	codigo = linea[5:]
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect(('node1', 10001))
	sock.sendall(codigo.encode())
	time.sleep(2)
	msgResponse = sock.recv(12)
	size = getSizeReto4(msgResponse)
	fichero = msgResponse[len(size)+1:]
	while int(size) > len(fichero):
		fichero = fichero + sock.recv(65000)
		time.sleep(0.2)
	ficherohashed = hashlib.sha1(fichero).digest()
	sock.sendall(ficherohashed)
	time.sleep(1)
	msgResponse = sock.recv(10000).decode()
	reto5(msgResponse)
	sock.recv(65000)

def reto5(msgResponse):
	print(msgResponse)
	magicNumber = b'YAP'
	header = magicNumber + struct.pack('!2bH', 0, 0, 0)
	codigo = getCode(msgResponse)
	print(codigo)
	codigo_bytes = codigo.encode('utf-8')
	base64_codigo_bytes = base64.b64encode(codigo_bytes)
	base64_codigo = base64_codigo_bytes.decode('utf-8')
	payload = struct.pack('q', 0) + base64_codigo_bytes
	m = header + payload
	checksum = cksum(m)
	head = magicNumber + struct.pack('!2bH', 0, 0, checksum)
	datagrama = head + payload
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.connect(('node1', 7000))
	sock.sendall(datagrama)
	time.sleep(1)
	msgResponse = sock.recv(65000)
	reto6(base64.b64decode(msgResponse[getPosInicioReto6(msgResponse):]).decode('utf-8'))

def getPosInicioReto(msgResponse):
	i=0
	while i<len(msgResponse):
		if(msgResponse[i:i+4] == "code"):
			break
		i += 1
	return msgResponse[i:]

def getPosInicioReto6(msgResponse):
	PosicionFinal = 0
	i = 0
	inicioReto6 = bytearray()
	inicioReto6.extend(b"Y29")

	while i<len(msgResponse):

		if msgResponse[i:i+3] == inicioReto6:
			PosicionFinal = i
			break

		i+=1

	return PosicionFinal

def reto7(msgResponse):
	print('\n')
	print(msgResponse)
	codigo = getCode(msgResponse)
	s = socket(AF_INET, SOCK_STREAM)
	s.connect(('node1', 33333))
	s.sendall(codigo.encode())
	time.sleep(1)
	print(s.recv(65000).decode())
	os._exit(1)

def reto6(msgResponse):
	print(msgResponse)
	codigo = getCode(msgResponse)
	puertoLibre = encontrarPuertoLibre()
	process = Process(target=iniciarWebServer, args=(puertoLibre,))
	processes.append(process)
	process.start()
	time.sleep(0.4)
	s = socket(AF_INET, SOCK_STREAM)
	s.connect(('node1', 8002))
	Mensaje = codigo + " " + str(puertoLibre)
	s.sendall(Mensaje.encode())
	s.close()

def getSizeReto4(msgResponse):
	size = ""
	indice = 0

	while indice < len(msgResponse):

		try:
			if msgResponse[indice:indice+1].decode() == ":":
				break

			size = size + msgResponse[indice:indice+1].decode()
		except:
			break

		indice += 1

	return size

def getAllInfo(sock, timeout):

	sock.setblocking(0)
	texto = ""
	begin = time.time()

	while True:

		if (time.time()-begin > timeout):
			break
		try:
			msg = sock.recv(65024)
			if msg:
				texto = texto + msg.decode("utf-8")
			else:
				time.sleep(0.01)
		except:
			pass

	return texto

def alReves(texto):
	nuevotexto = ""

	i = len(texto)

	while i>0:
		nuevotexto = nuevotexto + texto[i-1]
		i = i-1

	return nuevotexto

def serverUDP(puerto):
	sockserver = socket(AF_INET, SOCK_DGRAM)
	sockserver.bind(('', puerto))

	n = 0
	while 1:
		msg, client = sockserver.recvfrom(1024)
		n += 1
		handle(sockserver, msg, client, n)
		if (n == 1):
			break

if __name__ == '__main__':
	processes = []
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect(('node1', 2000))
	recibirMensaje()
	inicio()
	linea = recibirMensaje()[0]
	puerto = encontrarPuertoLibre()
	reto1(puerto)
	informacionServerUDP = str(puerto) + " " + linea
	sock.close()
	time.sleep(2)
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.sendto(informacionServerUDP.encode(), ('node1', 3000))
	msg, server = sock.recvfrom(1024)
	print("Reply is '%s'" % msg.decode())
	sock.close()
