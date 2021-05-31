#!/usr/bin/python

# -*- coding:UTF-8 -*-

import datetime
import socket
import subprocess
import time

from db_manager import select
from config import SERVER_HOST, SERVER_PORT


def timeShutDown(time):
    # Verifica orario attività server
    print(f"Ora: {time}")
    today8pm = time.replace(hour=20, minute=0, second=0, microsecond=0)
    today6am = time.replace(hour=6, minute=0, second=0, microsecond=0)

    return time > today8pm or time < today6am


def isAllAtHome(droneList):
    # Verifica se tutti i droni sono all'Hub
    if len(droneList) == 0:
        return True
    else:
        return False


def listCheck(hostname, stato, droniConnessi):
    # Aggiunge il drone se non è in lista
    for x in droniConnessi:
        if x == str(hostname) and stato == 'viaggio':
            droniConnessi.remove(str(hostname))


def parser(stringclient, droniConnessi):
    # Variabili drone
    x = stringclient.split("#")
    stato = x[2]
    hostname = x[3]
    ip = x[4]
    print(f"Dati drone: {hostname} {ip}")
    # Funzione che verifica se è in lista
    listCheck(hostname, stato, droniConnessi)
    # Rimozione se all'hub
    if stato == "hub":
        try:
            droniConnessi.index(str(hostname))
        except ValueError:
            droniConnessi.append(str(hostname))
    # Risposta
    reply = "server_" + stringclient + "_server"

    return reply


# Avvio Server
subprocess.Popen(f"fuser -k {SERVER_PORT}/tcp", shell=True)
print("Porta di servizio libera")
time.sleep(3)
print("Server avviato")
# Server
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(100)
# Query Database

droniConnessi = []
print("Lista dei droni:")
for idDrone in select("SELECT idDrone FROM tblDroni"):
    print(idDrone)
    droniConnessi.append(idDrone)

shutdown = False
drone = False

while shutdown is False or drone is False:
    # Connessione client
    c, addr = s.accept()
    print(f"Connessione stabilita con {addr}")
    # Ricezione
    inputmessage = c.recv(1024).decode()
    print(f"Messaggio dal client: {inputmessage}")
    # Invio
    outputmessage = parser(inputmessage, droniConnessi)
    c.send(outputmessage.encode())
    print(f"Messaggio dal server: {outputmessage}")
    # Chiusura
    c.close()
    print(f"Connessione interrotta con {addr}")
    # Spegnimento
    shutdown = timeShutDown(datetime.datetime.now())
    drone = isAllAtHome(droniConnessi)
    # Droni disponibili
    print("Droni disponibili: ")
    print(droniConnessi, sep="\n")
    time.sleep(.5)

print("Terminato")
