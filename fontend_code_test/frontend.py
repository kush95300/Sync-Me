import os
from tkinter import *
import tkinter
from PIL import Image, ImageTk
import threading


LARGE_FONT = ("Verdana", 12)
GEOMETRY = "900x450"
TEXT_FONT = "comicsansms"
FRAME_WIDTH = 900
FRAME_HEIGHT = 450

# Multipage GUI
class myAPP(tkinter.Tk):
    
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Multipage GUI")
        self.geometry(GEOMETRY)
        self.frames = {}
        for F in (StartPage, PageOne, ConsolePage):
            frame = F(self, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ConsolePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Start Page
class StartPage(tkinter.Frame):
    def __init__(self, parent, controller):
        full_output = True
        
        tkinter.Frame.__init__(self, parent,bg="white")
              
        # Logo image on Start Page
        photo = ImageTk.PhotoImage(Image.open("logo.jpg"))
        self.photo=photo
        self.can = Canvas(self , bg="white")
        self.can.grid(row=0, column=1, rowspan=2, columnspan=3)
        self.can.config(width=photo.width(), height=photo.height())  
        self.can.create_image(2, 2, image=photo, anchor=NW)

        # Buttons on Start Page
        self.image1 = PhotoImage(file="search1.png")
        self.image2 = PhotoImage(file="create1.png")
        self.image3 = PhotoImage(file="delete.png")    

        b1 = tkinter.Button(self, text="Details of Projects",command=lambda: controller.show_frame(PageOne),image=self.image1, compound=LEFT, padx=5, pady=5, font=("comicsansms", 20, "bold"), fg="black", bg="grey")
        b1.grid(row=3, column=2, pady=20,sticky="nsew")

        b2 = tkinter.Button(self, text="Create Project",command=lambda: controller.show_frame(PageOne) ,image=self.image2, compound=LEFT,padx=5, pady=5, font=("comicsansms", 20, "bold"), fg="black", bg="skyblue")
        b2.grid(row=4, column=0)

        b3 = tkinter.Button(self, text="Delete Project",image=self.image3, compound=LEFT, padx=5, pady=5, font=("comicsansms", 20, "bold"), fg="black", bg="skyblue")
        b3.grid(row=4, column=4)


class PageOne(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        label = tkinter.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tkinter.Button(self, text="Back to Home",
                                 command=lambda: controller.show_frame(StartPage))
        button1.pack()

class ConsolePage(tkinter.Frame):
    def __init__(self, parent, controller):
        global full_output
        full_output = False
        tkinter.Frame.__init__(self, parent, background="white")
        # Frame for the console box
        self.frame = Frame(self, bg="white", width=FRAME_WIDTH-20, height=FRAME_HEIGHT-100)
        self.frame.grid(row=0, column=0, columnspan=2,sticky="nsew")

        # Console box
        self.console = Canvas(self.frame,background="black",width=FRAME_WIDTH-20, height=FRAME_HEIGHT-100,scrollregion=(0,0,2000,5000))
        self.hscroll = Scrollbar(self.frame, orient=HORIZONTAL, command=self.console.xview)
        self.vscroll = Scrollbar(self.frame, orient=VERTICAL, command=self.console.yview)
        self.console['xscrollcommand'] = self.hscroll.set
        self.console['yscrollcommand'] = self.vscroll.set
        self.console.grid(row=0, column=0, sticky=N+S+E+W)
        self.hscroll.grid(row=1, column=0, sticky=E+W)
        self.vscroll.grid(row=0, column=1, sticky=N+S)
        print(self.console.xview)
        self.console.create_text(10, 10, anchor=NW, text="Console", fill="Red", font=(TEXT_FONT, 20, "bold"))
        
        
        self.console.create_text(50, 50, anchor=NW, text=self.get_data(file="data.txt"), fill="white", font=(TEXT_FONT, 12, "bold"))
        self.refresh()

        # Buttons for goto home page
        b1 = Button(self, text="Go to Main Page",command=lambda: controller.show_frame(StartPage) , padx=5, pady=5, font=(TEXT_FONT, 15), fg="black", bg="sky blue")
        b1.grid_configure(row=1, column=0, pady=20)

        b2 = Button(self, text="Go to Detail Page",command=lambda: controller.show_frame(StartPage) , padx=5, pady=5, font=(TEXT_FONT, 15), fg="black", bg="sky blue")
        b2.grid_configure(row=1, column=1, pady=20)

    # Get data from file
    def get_data(self, file):
        with open(file, "r") as f:
            data = f.read()
        return data
    
    # Refresh the console box
    def refresh(self):
        fulloutput=get_full_output()
        print("refreshing output")
        self.console.delete(ALL)
        self.console.create_text(10, 10, anchor=NW, text="Console", fill="Red", font=("comicsansms", 20, "bold"))
        self.console.create_text(50, 50, anchor=NW, text=self.get_data(file="data.txt"), fill="white", font=("comicsansms", 12, "bold"))
        if fulloutput=="False" or fulloutput=="":
            self.after(3000, self.refresh)
        else:
            return
    
    
def get_full_output():
    try:
        with open("full_output.txt", "r") as f:
            full_output = f.read()
    except:
        full_output = True
    return full_output


         





app = myAPP()
app.title("Sync Me")
app.mainloop()

