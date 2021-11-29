import os
from tkinter import *
import tkinter
from tkinter import ttk
from tkinter.font import BOLD
from PIL import Image, ImageTk
import threading


LARGE_FONT = ("Verdana", 12)
TEXT_FONT = "comicsansms"
FRAME_WIDTH = 1200
FRAME_HEIGHT = 650
GEOMETRY = "{}x{}".format(FRAME_WIDTH, FRAME_HEIGHT)

# Multipage GUI
class myAPP(tkinter.Tk):
    
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Multipage GUI")
        self.geometry(GEOMETRY)
        self.maxsize(FRAME_WIDTH, FRAME_HEIGHT)
        self.frames = {}
        for F in (StartPage, DetailPage, ConsolePage,ProjectPage,ConfigurationPage):
            frame = F(self, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(DetailPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Start Page
class StartPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent,bg="white")
              
        # Logo image on Start Page
        photo = ImageTk.PhotoImage(Image.open("logo3.png"))
        self.photo=photo
        self.can = Canvas(self , bg="white")
        self.can.grid(row=0, column=1, rowspan=2, columnspan=3)
        self.can.config(width=photo.width(), height=photo.height())  
        self.can.create_image(2, 2, image=photo, anchor=NW)

        # Buttons on Start Page
        self.image1 = PhotoImage(file="detail.png")
        self.image2 = PhotoImage(file="create.png")
        self.image3 = PhotoImage(file="delete.png")    

        b1 = tkinter.Button(self, text="Details of Projects",command=lambda: controller.show_frame(DetailPage),image=self.image1, compound=LEFT, padx=5, pady=5, font=("comicsansms", 20, "bold"), fg="black", bg="light green")
        b1.grid(row=3, column=2, pady=25,sticky="nsew")

        b2 = tkinter.Button(self, text="Create Project",command=lambda: controller.show_frame(ProjectPage) ,image=self.image2, compound=LEFT,padx=5, pady=5, font=("comicsansms", 20, "bold"), fg="black", bg="skyblue")
        b2.grid(row=4, column=0, padx=30)

        b3 = tkinter.Button(self, text="Delete Project",image=self.image3, compound=LEFT, padx=5, pady=5, font=("comicsansms", 20, "bold"), fg="black", bg="skyblue")
        b3.grid(row=4, column=4)


class DetailPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent,bg="white")
        
        # Back button
        self.back_img = ImageTk.PhotoImage(Image.open("back.png"))
        Button(self, text="Back",image=self.back_img, command=lambda: controller.show_frame(StartPage)).place(x=10,y=10)

        # Project Details
        Label(self, text = "Select Project :",font = (TEXT_FONT, 20, "bold"),bg="white").place(x=100,y=100)
        n = StringVar()
        monthchoosen =ttk.Combobox(self, width = 27, textvariable = n,font = (TEXT_FONT, 20, "bold"))
        
        # Adding combobox drop down list
        monthchoosen['values'] = ("default")
        
        monthchoosen.place(x = 350, y =100)
        monthchoosen.current()
        # Label(self, text = "Project Details",font = (TEXT_FONT, 25, "bold"),bg="White",fg="black").place(x=FRAME_WIDTH/2-150,y=190)
        # self.can = Canvas(self,bg="black",width=FRAME_WIDTH/2+100,height=FRAME_HEIGHT/2+30).place(x=FRAME_WIDTH/2-200,y=250)
        # self.can.create_text(self.can,text="Project Name :",font=(TEXT_FONT,15,"bold"),fill="white",anchor="nw",width=FRAME_WIDTH/2+100,height=FRAME_HEIGHT/2+30,tags="text")
        self.img = ImageTk.PhotoImage(Image.open("detail-big.jpg"))
        Label(self, text="",image=self.img,bd=0 ).place(x=50,y=FRAME_HEIGHT/2-130)

        # Frame for the console box
        self.frame = Frame(self, bg="grey",width=FRAME_WIDTH/2+100,height=FRAME_HEIGHT/2+30)
        self.frame.place(x=FRAME_WIDTH/2-200,y=250)

        # Console box
        self.Label = Label(self, text = "Project Details",font = (TEXT_FONT, 25, "bold"),bg="White",fg="black").place(x=FRAME_WIDTH/2-150,y=190)
        self.console = Canvas(self.frame,background="black",width=FRAME_WIDTH/2+100,height=FRAME_HEIGHT/2+30)
        self.console.place(x=0,y=0)
        self.console.create_text(10, 10, anchor=NW, text="Output", fill="Red", font=(TEXT_FONT, 20, "bold"))
        self.console.create_text(50, 50, anchor=NW, text=get_data(file="{}.txt".format(monthchoosen.current)), fill="white", font=(TEXT_FONT, 12, "bold"))
        

        

class ProjectPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent,bg="white")

        # Logo image on Start Page
        photo = ImageTk.PhotoImage(Image.open("logo2.png"))
        self.photo=photo
        self.can = Canvas(self , bg="white")
        self.can.grid(row=0, column=1, rowspan=2, columnspan=3,sticky="nsew")
        self.can.config(width=photo.width(), height=photo.height())  
        self.can.create_image(2, 2, image=photo, anchor=NW)

        # Buttons on Start Page
        self.image1 = PhotoImage(file="configure.png")
        self.image2 = PhotoImage(file="create.png")
        self.image3 = PhotoImage(file="upload.png")    
        self.image4 = PhotoImage(file="home.png") 
        b1 = tkinter.Button(self, text="Create Website",command=lambda: controller.show_frame(ConsolePage),image=self.image2, compound=LEFT, padx=5, pady=5, font=("comicsansms", 20, "bold"), fg="black", bg="orange")
        b1.grid(row=4, column=2,sticky="nsew")

        b2 = tkinter.Button(self, text="Configure Project",command=lambda: controller.show_frame(ConfigurationPage) ,image=self.image1, compound=LEFT,padx=5, pady=5, font=("comicsansms", 15, "bold"), fg="black", bg="skyblue")
        b2.grid(row=3, column=0,  pady=25,padx=30,sticky="nsew")

        b3 = tkinter.Button(self, text="Upload Website",image=self.image3, compound=LEFT, padx=5, pady=5, font=("comicsansms", 15, "bold"), fg="black", bg="skyblue")
        b3.grid(row=3, column=4,sticky="nsew",pady=25,padx=30,)

        # Back button
        self.back_img = ImageTk.PhotoImage(Image.open("back.png"))
        Button(self, text="Back",image=self.back_img, command=lambda: controller.show_frame(StartPage)).place(x=10,y=10)
        

    # open upload folder
    def open_upload_folder(self,path):
        os.startfile(path)

class ConfigurationPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent,bg="white")

        # Back button
        self.back_img = ImageTk.PhotoImage(Image.open("back.png"))
        Button(self, text="Back",image=self.back_img, command=lambda: controller.show_frame(ProjectPage)).place(x=10,y=10)
        
        # Page Title
        Label(self, text = 'Website Configuration', font =('Verdana', 35,"bold"),bg="white",fg="blue").pack(side = TOP, pady = 20)
        
        # Side Image
        self.img = ImageTk.PhotoImage(Image.open("setting.png"))
        Label(self, image=self.img).place( y=100, x=FRAME_WIDTH/2+50)

        # Project Form

        # Project Title Labels
        label1 = Label(self,text = "Project Name",font=("comicsansms", 16, "bold"),bg="white").place(x = FRAME_WIDTH/4-50,y = FRAME_HEIGHT/2-200)  
        label2 = Label(self,text = "AWS Secret Key",font=("comicsansms",  16, "bold"),bg="white").place(x = FRAME_WIDTH/4-70,y = FRAME_HEIGHT/2-100)
        label3 = Label(self,text = "AWS Access Key",font=("comicsansms",  16, "bold"),bg="white").place(x = FRAME_WIDTH/4-70,y = FRAME_HEIGHT/2) 
        label4 = Label(self,text = "AWS Region",font=("comicsansms",  16, "bold"),bg="white").place(x = FRAME_WIDTH/4-50,y = FRAME_HEIGHT/2+100) 
                            
        # Entry Boxes                    
        label1_input_area = Entry(self,width = 40,font=("comicsansms",16, "bold"),bg="white").place(x = FRAME_WIDTH/4-220,y = FRAME_HEIGHT/2-160)
        label2_input_area1 = Entry(self,width = 40,font=("comicsansms", 16, "bold"),bg="white").place(x = FRAME_WIDTH/4-220,y = FRAME_HEIGHT/2-60)
        label3_input_area2 = Entry(self,width = 40,font=("comicsansms", 16, "bold"),bg="white").place(x = FRAME_WIDTH/4-220,y = FRAME_HEIGHT/2+40)
        label4_input_area3 = Entry(self,width = 40,font=("comicsansms",16, "bold"),bg="white").place(x = FRAME_WIDTH/4-220,y = FRAME_HEIGHT/2+140)

        # Submit Button
        self.sub_img= PhotoImage(file="submit.png")
        b3 = tkinter.Button(self, text="Upload Variable",image=self.sub_img, compound=LEFT,padx=5, font=("comicsansms", 15, "bold"),command=lambda: controller.show_frame(ProjectPage), fg="black", bg="white").place( y = FRAME_HEIGHT-100, x = FRAME_WIDTH/2-400)
        

class ConsolePage(tkinter.Frame):
    def __init__(self, parent, controller):
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
        
        
        self.console.create_text(50, 50, anchor=NW, text=get_data(file="data.txt"), fill="white", font=(TEXT_FONT, 12, "bold"))
        self.refresh()

        # Buttons for goto home page
        b1 = Button(self, text="Go to Main Page",command=lambda: self.go_home(controller=controller,detail=False), padx=5, pady=5, font=(TEXT_FONT, 15), fg="black", bg="sky blue")
        b1.grid_configure(row=1, column=0, pady=20)

        b2 = Button(self, text="Go to Detail Page",command=lambda: self.go_home(controller=controller,detail=True) , padx=5, pady=5, font=(TEXT_FONT, 15), fg="black", bg="sky blue")
        b2.grid_configure(row=1, column=1, pady=20)
    
    # goto home page
    def go_home(self,controller,detail):
        put_full_output(1)
        if detail:
            controller.show_frame(DetailPage)
        else:
            controller.show_frame(StartPage)

    
    # Refresh the console box
    def refresh(self):
        fulloutput=get_full_output()
        self.console.delete(ALL)
        self.console.create_text(10, 10, anchor=NW, text="Console", fill="Red", font=("comicsansms", 20, "bold"))
        self.console.create_text(50, 50, anchor=NW, text=get_data(file="data.txt"), fill="white", font=("comicsansms", 12, "bold"))
        if fulloutput=="False" or fulloutput=="":
            self.after(3000, self.refresh)
        else:
            print("Refreshing Stop. Full Output Done")
            return
    
# Get data from file
def get_data( file):
    try:
        with open(file, "r") as f:
            data = f.read()
    except:
        data = "Data not found"
        print(file)            
    return data


# get full output  
def get_full_output():
    try:
        with open("full_output.txt", "r") as f:
            full_output = f.read()
    except:
        full_output = True
    return full_output

# Put full output in file
def put_full_output(x):
    if x==1:
        #print(x)
        with open("full_output.txt", "w") as f:
            f.write("True")
    else:
        with open("full_output.txt", "w") as f:
            f.write("False")
    


         



full_output =get_full_output()

app = myAPP()
app.title("Sync Me")
app.mainloop()

