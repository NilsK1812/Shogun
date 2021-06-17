from tkinter import *

class MyApp(Frame):
    def __init__(self, master):
        super().__init__(master)
        #self.pack(fill=BOTH, expand=True)
        master.geometry("800x800")
        #frame to hold the playing field
        '''
        self.f1 = Frame(master=master)
        self.f1.pack(fill=BOTH, expand=True)
        '''
        self.f2 = Canvas(master=master)
        self.f2.pack(fill=BOTH, expand=True)

        self.grid_length = 8
        
        #Variabeln um Feld zu erstellen
        self.count = 1
        self.x0 = 0
        self.y0 = 0
        self.x1 = 100
        self.y1 = 100
        self.farbe = 'black'

        self.black_first()
        self.grey_first()
        self.black_first()
        self.grey_first()
        self.black_first()
        self.grey_first()
        self.black_first()
        self.grey_first()

        '''
        for x in range(self.grid_length):
            self.f1.columnconfigure(x, weight = 1) 
            self.f1.rowconfigure(x, weight = 1)
        '''

    def Feld(self,x0, y0, x1, y1, farbe):
        self.f2.create_rectangle(x0, y0, x1, y1, fill=farbe)

    def black_first(self):
        while(1):
            if(self.count == 10):
                self.count = 1
                self.x0 = 0
                self.y0 = self.y0 + 100
                self.x1 = self.x1 + 100
                self.y1 = self.y1 + 100
                self.farbe = 'grey'
                print("geht")
                break
            if(self.count % 2):
                self.Feld(self.x0, self.y0, self.x1, self.y1, self.farbe)
                self.x0 = self.x0 + 100
                self.x1 = self.x1 + 100
                self.farbe = 'grey'
                self.count = self.count + 1
            else:
                self.Feld(self.x0, self.y0, self.x1, self.y1, self.farbe)
                self.x0 = self.x0 + 100
                self.x1 = self.x1 + 100
                self.farbe = 'black'
                self.count = self.count + 1
    
    def grey_first(self):
        while(1):
            if(self.count == 10):
                self.count = 1
                self.x0 = 0
                self.y0 = self.y0 + 100
                self.x1 = self.x1 + 100
                self.y1 = self.y1 + 100
                break
            if(self.count % 2):
                self.Feld(self.x0, self.y0, self.x1, self.y1, self.farbe)
                self.x0 = self.x0 + 100
                self.x1 = self.x1 + 100
                self.farbe = 'black'
                self.count = self.count + 1
            else:
                self.Feld(self.x0, self.y0, self.x1, self.y1, self.farbe)
                self.x0 = self.x0 + 100
                self.x1 = self.x1 + 100
                self.farbe = 'grey'
                self.count = self.count + 1

    '''
    def board(self):
        
        for x in range(self.grid_length):
            for y in range(self.grid_length):
                b = Button(master=self.f1)
                b.bind("<ButtonPress-1>", self.clicked)
                b.grid(row=y, column=x,sticky=N+S+E+W)

    def clicked(self,event):
        print("Klick")
    '''

tk_window = Tk()
tk_window.title('Shongu')
app = MyApp(tk_window)
app.mainloop()