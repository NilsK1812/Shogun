import socket
from time import sleep
import pickle
from tkinter import *
import tkinter.messagebox
import random as r
import threading

recive_var = ''
player = 0
zahlen = []
data_rec = []
destroy = 0

HOST = '127.0.0.1' 
PORT = 61111      
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#Name wird abgefragt
name = input("Wie soll dein Username sein -> ")

#Name wird an den Server geschickt
s.sendall(name.encode())

class MyApp(Frame):
    def __init__(self, master):
        super().__init__(master)
        #self.pack(fill=BOTH, expand=True)
        master.geometry("600x600")
        #frame to hold the playing field
        self.f1 = Frame(master=master)
        self.f1.pack(fill=BOTH, expand=True)

        #frame to hold additional buttons (quit)
        '''
        self.f2 = Frame(master=master)
        self.f2.pack()
        restart = Button(master=self.f2, text="Fertig", command=quit)
        restart.pack(side="left")
        '''
        #parameter fuer die grid groesse
        self.grid_length = 8
        self.row = 0
        self.Spieler = 0
        self.knoepfe = []
        self.augenzahlen = []
        self.count_augenzahlen = 0
        self.farbe = ''
        self.number_in_button = 0
        self.aktueller_player = 1
        self.aktuelle_farbe = ''
        self.event1 = ''
        self.event2 = ''
        self.x_Achse = 0
        self.y_Achse = 0
        #Fuer den zweiten Button den der Spieler drueckt um seine Figur zu bewegen
        self.x_Achse2 = 0
        self.y_Achse2 = 0
        #Check Variable
        self.first_round = 0
        #Kordinaten die versendet werden
        self.first_klick = 0
        self.second_klick = 0
        #Liste mit den Daten die versendet werden
        self.Daten_senden = []
        
        if(player == 1):
            self.create_buttons()

        elif((player == 2)):
            self.first_round = 1
            self.create_buttons()
            self.refresh_buttons()

        #make the grid layout expand 
        for x in range(self.grid_length):
            self.f1.columnconfigure(x, weight = 1) 
            self.f1.rowconfigure(x, weight = 1)

    def create_buttons(self):
        self.black_first()
        self.grey_first()
        self.black_first()
        self.grey_first()

        self.black_first()
        self.grey_first()
        self.black_first()
        self.grey_first()
    
    def clicked(self, event):
        if((event.widget["highlightbackground"] == "#565656" or event.widget["highlightbackground"] == "#000000") and self.farbe == ''):
            tkinter.messagebox.showwarning("Warning","Auf dem Feld ist keine Figur")

        elif((self.farbe == 'red') and (event.widget["highlightbackground"] == "red")):
            tkinter.messagebox.showwarning("Warning","Du kannst dich nicht selber schmeißen")
        
        elif((self.farbe == 'snow') and (event.widget["highlightbackground"] == "snow")):
            tkinter.messagebox.showwarning("Warning","Du kannst dich nicht selber schmeißen")

        elif(self.farbe != ''):
            grid_info = event.widget.grid_info()
            self.x_Achse2 = grid_info["column"]
            self.y_Achse2 = grid_info["row"]
            self.event2 = event.widget
            self.event1["highlightbackground"] = self.aktuelle_farbe
            self.event1["text"] = ''
            self.event2["highlightbackground"] = self.farbe
            print("1")
            if(self.event1["fg"] == '#ffd700'):
                random_zahl = r.randint(1,2)
                self.event2["text"] = random_zahl
                self.event2["fg"] = "#ffd700"
            else:
                random_zahl = r.randint(1,4)
                self.event2["text"] = random_zahl
            self.send()
            self.event1 = ''
            self.event2 = ''
            self.aktuelle_farbe = ''
            self.aktueller_player = 3
            self.farbe = ''
            recive_thread = threading.Thread(target = self.recive)
            recive_thread.start()

        elif(self.aktueller_player == 3):
            tkinter.messagebox.showinfo("Info","Bitte warte bis dein Gegner mit dem Zug fertig ist!")

        else:
            grid_info = event.widget.grid_info()
            self.x_Achse = grid_info["row"]
            self.y_Achse = grid_info["column"]
            if(self.aktueller_player == 1):
                if(event.widget["highlightbackground"] == "snow"):
                    self.black_grey_checker()
                    self.farbe = event.widget["highlightbackground"]
                    self.event1 = event.widget  
                    self.aktueller_player = 2
                else:
                    tkinter.messagebox.showwarning("Spieler1","Du bist weiß und nicht rot :)")
            else:
                if(event.widget["highlightbackground"] == "red"):
                    self.black_grey_checker()
                    self.farbe = event.widget["highlightbackground"]
                    self.event1 = event.widget
                    self.aktueller_player = 1
                else:
                    tkinter.messagebox.showwarning("Spieler2","Du bist rot und nicht weiß :)")

    def black_first(self):
        count = 0
        random_zahl = 0
        for x in range(self.grid_length):
            b = Button(master=self.f1)
            if(self.row == 0):
                if(player == 1):
                    r.seed()
                    b["highlightbackground"] = 'red'
                    if(count == 4):
                        random_zahl = r.randint(1,2)
                        b["fg"] = '#ffd700'
                        b["text"] = random_zahl
                    else:
                        random_zahl = r.randint(1,4)
                        b["text"] = random_zahl
                    count = count + 1
                
                elif(player == 2):
                    b["highlightbackground"] = 'red'
                    if(count == 4):
                        random_zahl = zahlen[self.count_augenzahlen]
                        b["fg"] = '#ffd700'
                        b["text"] = random_zahl
                    else:
                        random_zahl = zahlen[self.count_augenzahlen]
                        b["text"] = random_zahl
                    count = count + 1
                    self.count_augenzahlen = self.count_augenzahlen + 1
            
            elif(count % 2):
                b["highlightbackground"] = '#565656'
                count = count + 1 
            else:
                 b["highlightbackground"] = '#000000'
                 count = count + 1 

            b.bind("<ButtonPress-1>", self.clicked)
            b.grid(row=self.row, column=x, sticky=N+S+E+W)

            if(count == 8):
                count = 0
                self.row = self.row + 1

            if(random_zahl > 0):
                self.augenzahlen.append(random_zahl)
            
            self.knoepfe.append(b)

    def grey_first(self):
        count = 0
        random_zahl = 0
        for x in range(self.grid_length):
            b = Button(master=self.f1)
            
            if(self.row == 7):
                if(player == 1):
                    r.seed()
                    b["highlightbackground"] = 'snow'
                    if(count == 3):
                        random_zahl = r.randint(1,2)
                        b["fg"] = '#ffd700'
                        b["text"] = random_zahl
                    else:
                        random_zahl = r.randint(1,4)
                        b["text"] = random_zahl
                    count = count + 1 

                elif(player == 2):
                    b["highlightbackground"] = 'snow'
                    if(count == 3):
                        random_zahl = zahlen[self.count_augenzahlen]
                        b["fg"] = '#ffd700'
                        b["text"] = random_zahl
                    else:
                        random_zahl = zahlen[self.count_augenzahlen]
                        b["text"] = random_zahl
                    count = count + 1
                    self.count_augenzahlen = self.count_augenzahlen + 1 

            elif(count % 2):
                b["highlightbackground"] = '#000000'
                count = count + 1 

            else:
                 b["highlightbackground"] = '#565656'
                 count = count + 1 

            b.bind("<ButtonPress-1>", self.clicked)
            b.grid(row=self.row, column=x, sticky=N+S+E+W)

            if(count == 8):
                count = 0
                self.row = self.row + 1

            if(random_zahl > 0):
                self.augenzahlen.append(random_zahl)

            self.knoepfe.append(b)
    
    def black_grey_checker(self):
        if(self.x_Achse % 2):
            if(self.y_Achse % 2):
                self.aktuelle_farbe = '#000000'
               
            else:
                self.aktuelle_farbe = '#565656'
               
        else:
            if(self.y_Achse % 2):
                self.aktuelle_farbe = '#565656'
               
            else:
                self.aktuelle_farbe = '#000000'
    
    def send(self):
        if(self.first_round == 0):
            
            print("send")

            data = "jetzt"

            s.sendall(data.encode())

            sleep(0.5)

            zahlen = pickle.dumps(self.augenzahlen)

            s.sendall(zahlen)
                
            self.x_y_Achse_rechner()

            changes = pickle.dumps(self.Daten_senden)

            s.sendall(changes)
                
            self.first_round = 1
        
        else:
            
            print("send")

            self.x_y_Achse_rechner()

            changes = pickle.dumps(self.Daten_senden)

            s.sendall(changes)


    def x_y_Achse_rechner(self):
        
        for i in range(len(self.knoepfe)):
            x = self.knoepfe[i]
            if(x == self.event1):
                self.first_klick = i
                break
        
        for i in range(len(self.knoepfe)):
            x = self.knoepfe[i]
            if(x == self.event2):
                self.second_klick = i
                break

        self.Daten_senden.append(self.first_klick)
        self.Daten_senden.append(self.aktuelle_farbe)
        self.Daten_senden.append(self.second_klick)
        self.Daten_senden.append(self.event2["highlightbackground"])
        self.Daten_senden.append(self.event2["text"])
        self.Daten_senden.append(self.event2["fg"])
        self.Daten_senden.append(self.aktueller_player)

        print(self.Daten_senden)


    def refresh_buttons(self):
        self.knoepfe[data_rec[0]].configure(highlightbackground = data_rec[1])
        self.knoepfe[data_rec[0]].configure(text = '')
        self.knoepfe[data_rec[2]].configure(highlightbackground = data_rec[3])
        self.knoepfe[data_rec[2]].configure(text = data_rec[4])
        self.knoepfe[data_rec[2]].configure(fg = data_rec[5])
        self.aktueller_player = data_rec[6]    


    def recive(self):
        global data_rec

        data_rec = []

        print(data_rec)

        self.Daten_senden = []

        try:
            while(1):
                print("thread")
                '''
                data = s.recv(1024)
                data = data.decode()
                
                if(data == "jetzt"):
                '''
                data = s.recv(1024)

                data_rec = pickle.loads(data) 

                break
        
        except:
            print("Threads koennen in Python nicht beendent werden, deswegen wird die Fehlermeldung abgefangen, damit es uebersichtlicher Aussieht")
        
        self.refresh_buttons()

#Client empfaengt alle Daten die der Server schickt
def recive():
    global recive_var
        
    data = s.recv(1024)
    spieler = data.decode()

    if(spieler == "eins"):
        print("Du bist Spieler 1")

    elif(spieler == ("{} du musst leider noch warten, weil da du alleine im Raum bist".format(name))):
        print(spieler)

    elif(spieler == "zwei"):
        print("Du bist Spieler 2")
        recive_var = False
            
    elif(spieler == "Huhu, ein zweiter Spieler ist da :)"):
        print("Huhu, ein zweiter Spieler ist da :)")
        recive_var = True

while(1):
    recive()
    if(recive_var == True):
        player = 1
        break
    elif(recive_var == False):
        player = 2
        break

if(player == 1):
    tk_window = Tk()
    tk_window.title("Shmong-Shmong")
    app = MyApp(tk_window)
    app.mainloop()

else:
    while(1):
        data = s.recv(1024)

        data = data.decode()

        if(data == "jetzt"):

            rot = s.recv(1024)

            zahlen = pickle.loads(rot)
            
            sleep(1)

            data = s.recv(1024)

            data_rec = pickle.loads(data) 

            break

    tk_window = Tk()
    tk_window.title("Shmong-Shmong")
    app = MyApp(tk_window)
    app.mainloop()






