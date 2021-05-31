#!/usr/bin/python

# -*- coding:UTF-8 -*-

import random
import socket
import time
from config import SERVER_HOST, SERVER_PORT


def checkConsegna():
    # La funzione dovrebbe rilevare il drone che atterra e 
    # quindi si abbassa di quota ma  non avendo modo di 
    # emularla utilizziamo un random
    if random.randint(0, 9) <= 2:
        return True
    else:
        return False


def getGPS():
    # Generazione casuale del GPS
    latitudine = str(round(random.uniform(-90.000001, +90.000001), 6))
    longitudine = str(round(random.uniform(-180.000001, +180.000001), 6))
    # Hostname e ip
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    # Condizioni per la localizzazione
    if "45.443513" <= latitudine <= "45.443928":
        if "12.318577" <= longitudine <= "12.319442":
            reply = f"{latitudine}#{longitudine}#hub#{hostname}#{ip_address}"
        else:
            reply = f"{latitudine}#{longitudine}#viaggio#{hostname}#{ip_address}"
    else:
        reply = f"{latitudine}#{longitudine}#viaggio#{hostname}#{ip_address}"
    # Controllo consegna
    if checkConsegna() is True:
        reply = f"{latitudine}#{longitudine}#consegnato#{hostname}#{ip_address}"

    return reply


reply = ""

while reply != "Spegni":
    # Connessione
    s = socket.socket()
    s.connect((SERVER_HOST, SERVER_PORT))
    # Invio
    s.send(getGPS().encode())
    # Ricezione
    reply = s.recv(1024).decode()
    print(reply)
    # Chiusura
    s.close()
    # Time out
    time.sleep(10)

print("Terminato")
