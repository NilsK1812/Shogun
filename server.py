import socket
import threading
from time import sleep
import random as r
import pickle

clients = []
number_of_players = 0

def echo(conn, addr,name,number_of_players):
    print("Connected by", addr)
    data = "{} ist dem Spiel beigetreten!".format(name)

    print(data)
    
    #data wird an alle Clients die Verbunden sind weitergeschickt
    for users in clients:
        users.sendall(data.encode())

    while(number_of_players <= 2):
        if(number_of_players == 1):
            data = "eins"
            sleep(1)
            conn.sendall(data.encode())
            sleep(1)
            break

        else:
            data = "zwei"
            sleep(1)
            conn.sendall(data.encode())
            sleep(1)
            break

    if(number_of_players == 1):
        data = "{} du musst leider noch warten, weil da du alleine im Raum bist".format(name)
        conn.sendall(data.encode())
    
    else:
        data = "Huhu, ein zweiter Spieler ist da :)"
        clients[0].sendall(data.encode())
        sleep(1)

    try:
        while True:
            #gesendte Daten werden ermittelt
            data = conn.recv(1024)
            #wenn keine Daten gesendet werden, dann hat sich ein Client getrennt
            if not data:

                data = "{} hat das Spiel verlassen!".format(name)

                print(data)

                #Es wird der Client der die Verbindung getrennt hat aus den Listen geloescht
                clients.remove(conn)
                
                for users in clients:
                    users.sendall(data.encode())

                data = "Das Spiel ist vorbei!"

                for users in clients:
                    users.sendall(data.encode())

                break

            if(conn == clients[0]):
                clients[1].sendall(data)
            elif(conn == clients[1]):
                clients[0].sendall(data)
    
    except:
        print("Ein Client hat die Verbindungen zum Server getrennt.")



HOST = "127.0.0.1"
PORT = 61111

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

while True:
    conn, addr = s.accept()
    clients.append(conn)
    number_of_players = len(clients)
    
    #Das erste was empfangen wird ist der Name vom Client
    name = conn.recv(1024).decode()

    echo_thread = threading.Thread(target = echo, args = (conn, addr,name,number_of_players))
    echo_thread.start()