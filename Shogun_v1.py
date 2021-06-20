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
        self.knoepfe = []
        self.knoepfe_farbe =  []
        self.farbe = ''
        self.create_buttons()

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
        print(self.farbe)

        if((event.widget["highlightbackground"] == "#565656" or event.widget["highlightbackground"] == "#000000") and self.farbe == ''):
            tkinter.messagebox.showwarning("Warning","Auf dem Feld ist keine Figur")
        
        elif(self.farbe != ''):
            event.widget["highlightbackground"] = self.farbe
            self.farbe = ''

        else:
            grid_info = event.widget.grid_info()
            print("{}/{}".format(grid_info["column"],grid_info["row"]))
            self.farbe = event.widget["highlightbackground"]
            print(self.farbe)


    def black_first(self):
        count = 0
        random_zahl = 0
        for x in range(self.grid_length):
            b = Button(master=self.f1)
            
            if(self.row == 0):
                r.seed()
                b["highlightbackground"] = 'red'
                if(count == 4):
                    random_zahl = r.randint(1,2)
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

            self.knoepfe.append(b)
    
    def grey_first(self):
        count = 0
        random_zahl = 0
        for x in range(self.grid_length):
            b = Button(master=self.f1)
            
            if(self.row == 7):
                r.seed()
                b["highlightbackground"] = 'snow'
                if(count == 4):
                    random_zahl = r.randint(1,2)
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

            self.knoepfe.append(b)
            self.knoepfe_farbe.append(b["highlightbackground"])


tk_window = Tk()
tk_window.title("Shongun")
app = MyApp(tk_window)
app.mainloop()