'''
To-Do:
    Zug definieren, Spieler kann nur Zahl im Button gehen
'''
from tkinter import *
import tkinter.messagebox
import random as r

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
        #self.knoepfe = []
        #self.knoepfe_farbe = []
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
        #Spannt die Figuren an den Richtigen stellen
        self.Spieler1_Figuren = 0
        self.Spieler2_Figuren = 7
        #Farbe des ersten Buttons
        self.first_button_farbe = ''
        self.create_buttons()

        #make the grid layout expand 
        for x in range(self.grid_length):
            self.f1.columnconfigure(x, weight = 1) 
            self.f1.rowconfigure(x, weight = 1)
        
    #Buttons fuer den Spieler 1
    def create_buttons(self):
        self.first_button_farbe = 'black'
        self.black_first()
        self.grey_first()
        self.black_first()
        self.grey_first()

        self.black_first()
        self.grey_first()
        self.black_first()
        self.grey_first()
    
    #Buttons fuer den Spieler 2
    def create_buttons2(self):
        self.first_button_farbe = 'grey'
        self.grey_first()
        self.black_first()
        self.grey_first()
        self.black_first()

        self.grey_first()
        self.black_first()
        self.grey_first()
        self.black_first()

    def clicked(self, event):
        print("Es geht!")
        print(self.farbe)

        if((event.widget["highlightbackground"] == "#565656" or event.widget["highlightbackground"] == "#000000") and self.farbe == ''):
            tkinter.messagebox.showwarning("Warning","Auf dem Feld ist keine Figur")

        elif((self.farbe == 'red' or self.farbe == 'snow') and (event.widget["highlightbackground"] == "red" or event.widget["highlightbackground"] == 'snow')):
            tkinter.messagebox.showwarning("Warning","Du kannst dich nicht selber schmeißen")

        elif(self.farbe != ''):
            grid_info = event.widget.grid_info()
            self.x_Achse2 = grid_info["column"]
            self.y_Achse2 = grid_info["row"]
            print("x-Achse: {}; Y-Achse: {}".format(self.x_Achse2, self.y_Achse2))
            self.spielzug_checker()
            self.event1["highlightbackground"] = self.aktuelle_farbe
            self.event1["text"] = ''
            event.widget["highlightbackground"] = self.farbe
            if(self.event1["fg"] == '#ffd700'):
                random_zahl = r.randint(1,2)
                event.widget["text"] = random_zahl
                event.widget["fg"] = "#ffd700"
            else:
                random_zahl = r.randint(1,4)
                event.widget["text"] = random_zahl
            self.event1 = ''
            self.aktuelle_farbe = ''
            self.farbe = ''
            
        else:
            grid_info = event.widget.grid_info()
            print("{}/{}".format(grid_info["column"],grid_info["row"]))
            self.x_Achse = grid_info["column"]
            self.y_Achse = grid_info["row"]
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
            
            if((self.row == self.Spieler1_Figuren)or(self.row == self.Spieler2_Figuren)):
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

                self.Spieler1_Figuren = 7
                self.Spieler2_Figuren = 0

            #self.knoepfe.append(b)
    
    def grey_first(self):
        count = 0
        random_zahl = 0
        for x in range(self.grid_length):
            b = Button(master=self.f1)
            
            if((self.row == self.Spieler1_Figuren)or(self.row == self.Spieler2_Figuren)):
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

            #self.knoepfe.append(b)
            #self.knoepfe_farbe.append(b["highlightbackground"])
    
    def black_grey_checker(self):
        print("x-Achse: {}; Y-Achse: {}".format(self.x_Achse, self.y_Achse))
        if(self.x_Achse % 2):
            if(self.y_Achse % 2):
                if(self.first_button_farbe == 'black'):
                    self.aktuelle_farbe = '#000000'
                else:
                    self.aktuelle_farbe = '#565656'
            else:
                if(self.first_button_farbe == 'black'):
                    self.aktuelle_farbe = '#565656'
                else:
                    self.aktuelle_farbe = '#000000'
        else:
            if(self.y_Achse % 2):
                if(self.first_button_farbe == 'black'):
                    self.aktuelle_farbe = '#565656'
                else:
                    self.aktuelle_farbe = '#000000'
            else:
                if(self.first_button_farbe == 'black'):
                    self.aktuelle_farbe = '#000000'
                else:
                    self.aktuelle_farbe = '#565656'

    def spielzug_checker(self):
        print("Hi")

tk_window = Tk()
tk_window.title("Shmong-Shmong")
app = MyApp(tk_window)
app.mainloop()