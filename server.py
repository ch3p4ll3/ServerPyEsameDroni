#!/usr/bin/python

#-*- coding:UTF-8 -*-

import socket, time, subprocess, datetime, mysql.connector


def timeShutDown(time):
	# Verifica orario attività server
	print("Ora: "+str(time))
	today8pm=time.replace(hour=20, minute=0, second=0, microsecond=0)
	today6am=time.replace(hour=6, minute=0, second=0, microsecond=0)

	return time>today8pm or time<today6am


def isAllAtHome(droneList):
	# Verifica se tutti i droni sono all'Hub
	if(len(droneList)==0):
		return True
	else:
		return False


def listCheck(hostname, ip):
	# Aggiunge il drone se non è in lista
	check=False
	for x in droniConnessi:
		if(x==str(hostname)):
			check=True

	if(check==False):
		droniConnessi.append(str(hostname))


def parser(stringclient):
	# Variabili drone
	x=stringclient.split("#")
	latitudine=x[0]
	longitudine=x[1]
	stato=x[2]
	hostname=x[3]
	ip=x[4]
	print("Dati drone: "+str(hostname)+" "+str(ip))
	# Funzione che verifica se è in lista
	listCheck(hostname, ip)
	# Rimozione se all'hub
	if(stato=="hub"):
		droniConnessi.remove(str(hostname))
	# Risposta
	reply="server_"+stringclient+"_server"

	return reply


# Avvio Server
host="127.0.0.1"
port=12555
subprocess.Popen("fuser -k "+str(port)+"/tcp", shell=True)
print("Porta di servizio libera")
time.sleep(3)
print("Server avviato")
# Server
s=socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(100)
# Query Database
mydb=mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="dbVeniceDrone"
)

mycursor=mydb.cursor()
mycursor.execute("SELECT idDrone FROM tblDroni")
myresult=mycursor.fetchall()

print("Lista dei droni:")
for x in myresult:
  print(x)
# Variabili
shutdown=False
drone=False
droniConnessi=[]

while(shutdown==False or drone==False):
	# Connessione client
	c, addr=s.accept()
	print("Connessione stabilita con "+str(addr))
	# Ricezione
	inputmessage=c.recv(1024).decode()
	print("Messaggio dal client: "+inputmessage)
	# Invio
	outputmessage=parser(inputmessage)
	c.send(outputmessage.encode())
	print("Messaggio dal server: "+outputmessage)
	# Chiusura
	c.close
	print("Connessione interrotta con  "+str(addr))
	# Spegnimento
	shutdown=timeShutDown(datetime.datetime.now())
	drone=isAllAtHome(droniConnessi)
	# Droni fuori dall'Hun
	print("Droni in viaggio: ")
	print(*droniConnessi, sep = "\n")

print("Terminato")
