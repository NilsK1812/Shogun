import socket
from time import sleep
import pickle
from tkinter import *
import tkinter.messagebox
import random as r

recive_var = ''
player = 0
zahlen = []
data_rec1 = ''
data_rec2 = ''

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

        #frame to hold additional buttons (restart and quit)
        self.f2 = Frame(master=master)
        self.f2.pack()
        restart = Button(master=self.f2, text="exit", command=self.quit)
        restart.pack(side="left")

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
        if(player == 1):
            self.create_buttons()

        elif((player == 2)):
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
        print("Es geht!")
        print(self.augenzahlen)

        if((event.widget["highlightbackground"] == "#565656" or event.widget["highlightbackground"] == "#000000") and self.farbe == ''):
            tkinter.messagebox.showwarning("Warning","Auf dem Feld ist keine Figur")

        elif((self.farbe == 'red' or self.farbe == 'snow') and (event.widget["highlightbackground"] == "red" or event.widget["highlightbackground"] == 'snow')):
            tkinter.messagebox.showwarning("Warning","Du kannst dich nicht selber schmeißen")

        elif(self.farbe != ''):
            grid_info = event.widget.grid_info()
            self.x_Achse2 = grid_info["column"]
            self.y_Achse2 = grid_info["row"]
            self.event2 = event.widget
            print("x-Achse: {}; Y-Achse: {}".format(self.x_Achse2, self.y_Achse2))
            self.event1["highlightbackground"] = self.aktuelle_farbe
            self.event1["text"] = ''
            self.event2["highlightbackground"] = self.farbe
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
            self.farbe = ''
        
        else:
            grid_info = event.widget.grid_info()
            print("{}/{}".format(grid_info["column"],grid_info["row"]))
            self.x_Achse = grid_info["row"]
            self.y_Achse = grid_info["column"]
            if(self.aktueller_player == 1):
                if(event.widget["highlightbackground"] == "snow"):
                    self.black_grey_checker()
                    self.farbe = event.widget["highlightbackground"]
                    print(self.farbe)
                    self.event1 = event.widget 
                    print(self.event1) 
                    self.aktueller_player = 2
                else:
                    tkinter.messagebox.showwarning("Spieler1","Du bist weiß und nicht rot :)")
            else:
                if(event.widget["highlightbackground"] == "red"):
                    self.black_grey_checker()
                    self.farbe = event.widget["highlightbackground"]
                    print(self.farbe)
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
        print("x-Achse: {}; Y-Achse: {}".format(self.x_Achse, self.y_Achse))
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
            data = "jetzt"

            print(data)

            s.sendall(data.encode())

            sleep(0.5)

            zahlen = pickle.dumps(self.augenzahlen)

            s.sendall(zahlen)

            self.x_y_Achse_rechner()
            
            print(self.first_klick)
            print(self.second_klick)

            data = str(self.first_klick)

            s.sendall(data.encode())

            sleep(1)
            
            data = str(self.second_klick)

            s.sendall(data.encode())

            self.first_round = 1

    def x_y_Achse_rechner(self):
        
        self.x_Achse = self.x_Achse + 1
        self.x_Achse2 = self.x_Achse2 + 1
        self.y_Achse = self.y_Achse + 1
        self.y_Achse2 = self.y_Achse2 + 1
        
        print("x-Achse")
        print(self.x_Achse)
        print(self.x_Achse2)
        print("Y-Achse")
        print(self.y_Achse)
        print(self.y_Achse2)
        print("Länge der Liste")
        print(len(self.knoepfe))

        for x in range(self.x_Achse):
            for y in range(self.y_Achse):
                self.first_klick = self.first_klick + 1
        
        for x in range(self.x_Achse2):
            for y in range(self.y_Achse2):
                self.second_klick = self.second_klick + 1
        
        self.first_klick = self.first_klick - 1
        self.second_klick = self.second_klick - 1

    def refresh_buttons(self):
        first = self.knoepfe(data_rec1)
        second = self.knoepfe(data_rec2)

        
                
            
#Client empfaengt alle Daten die der Server schickt
def recive():
    global recive_var
        
    data = s.recv(1024)
    spieler = data.decode()
    print(spieler)

    if(spieler == "eins"):
        print("Du bist Spieler 1")
                
    elif(spieler == "zwei"):
        print("Du bist Spieler 2")
        recive_var = False
            
    elif(spieler == "Huhu, ein zweiter Spieler ist da :)"):
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

            print(rot)

            zahlen = pickle.loads(rot)
            
            sleep(1)

            data = s.recv(1024)
            
            data = data.decode()

            data_rec1 = int(data)

            sleep(1)

            data = s.recv(1024)
            
            data = data.decode()

            data_rec2 = int(data)
                    
            print(data_rec1)
            print(data_rec2)

            break

    tk_window = Tk()
    tk_window.title("Shmong-Shmong")
    app = MyApp(tk_window)
    app.mainloop()



