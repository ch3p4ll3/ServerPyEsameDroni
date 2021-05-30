#!/usr/bin/python

#-*- coding:UTF-8 -*-

import socket, time, random


def checkConsegna():
    # La funzione dovrebbe rilevare il drone che atterra e 
    # quindi si abbassa di quota ma  non avendo modo di 
    # emularla utilizziamo un random
    if(random.randint(0, 9)<=2):
        return True
    else:
        return False


def getGPS():
    # Generazione casuale del GPS
    latitudine=str(round(random.uniform(-90.000001, +90.000001), 6))
    longitudine=str(round(random.uniform(-180.000001, +180.000001), 6))
    # Hostname e ip
    hostname=socket.gethostname()
    ip_address=socket.gethostbyname(hostname)
    # Condizioni per la localizzazione
    if(latitudine>="45.443513" and latitudine<="45.443928"):
        if(longitudine>="12.318577" and longitudine<="12.319442"):
            reply=latitudine+"#"+longitudine+"#"+"hub"+"#"+str(hostname)+"#"+str(ip_address)
        else:
            reply=latitudine+"#"+longitudine+"#"+"viaggio"+"#"+str(hostname)+"#"+str(ip_address)
    else:
        reply=latitudine+"#"+longitudine+"#"+"viaggio"+"#"+str(hostname)+"#"+str(ip_address)
    # Controllo consegna
    if(checkConsegna()==True):
        reply=latitudine+"#"+longitudine+"#"+"consegnato"+"#"+str(hostname)+"#"+str(ip_address)

    return reply


host="127.0.0.1"
port=12555

reply=""

while(reply!="Spegni"):
    # Connessione
    s=socket.socket()
    s.connect((host, port))
    # Invio
    s.send(getGPS().encode())
    # Ricezione
    reply=s.recv(1024).decode()
    print(reply)
    # Chiusura
    s.close()
    # Time out
    time.sleep(100)

print("Terminato")