import os,sys
from tkinter import *
import tkinter
from tkinter import ttk
from tkinter.font import BOLD
from PIL import Image, ImageTk

PATH =os.path.dirname(sys.modules['__main__'].__file__)
IMAGE_PATH = "{}/images/".format(PATH)
LARGE_FONT = ("Verdana", 12)
TEXT_FONT = "comicsansms"
FRAME_WIDTH = 1200
FRAME_HEIGHT = 650
GEOMETRY = "{}x{}".format(FRAME_WIDTH, FRAME_HEIGHT)
delete_project = False

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
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Start Page
class StartPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent,bg="white")
              
        # Logo image on Start Page
        photo = ImageTk.PhotoImage(Image.open(IMAGE_PATH+"logo3.png"))
        self.photo=photo
        self.can = Canvas(self , bg="white")
        self.can.grid(row=0, column=1, rowspan=2, columnspan=3)
        self.can.config(width=photo.width(), height=photo.height())  
        self.can.create_image(2, 2, image=photo, anchor=NW)

        # Buttons on Start Page
        self.image1 = PhotoImage(file=IMAGE_PATH+"detail.png")
        self.image2 = PhotoImage(file=IMAGE_PATH+"create.png")
        self.image3 = PhotoImage(file=IMAGE_PATH+"delete.png")    

        b1 = tkinter.Button(self, text="Details of Projects",command=lambda: controller.show_frame(DetailPage),image=self.image1, compound=LEFT, padx=5, pady=5, font=("comicsansms", 20, "bold"), fg="black", bg="light green")
        b1.grid(row=3, column=2, pady=25,sticky="nsew")

        b2 = tkinter.Button(self, text="Create Project",command=lambda: controller.show_frame(ProjectPage) ,image=self.image2, compound=LEFT,padx=5, pady=5, font=("comicsansms", 20, "bold"), fg="black", bg="skyblue")
        b2.grid(row=4, column=0, padx=30)

        b3 = tkinter.Button(self, text="Delete Project",command=lambda: self.go_to_delete(controller),image=self.image3, compound=LEFT, padx=5, pady=5, font=("comicsansms", 20, "bold"), fg="black", bg="skyblue")
        b3.grid(row=4, column=4)
    
    def go_to_delete(self,controller):
        global delete_project
        delete_project=True
        controller.show_frame(ConfigurationPage)


class DetailPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent,bg="white")
        
        # Back button
        self.back_img = ImageTk.PhotoImage(Image.open(IMAGE_PATH+"back.png"))
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
        self.img = ImageTk.PhotoImage(Image.open(IMAGE_PATH+"detail-big.jpg"))
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
        photo = ImageTk.PhotoImage(Image.open(IMAGE_PATH+"logo2.png"))
        self.photo=photo
        self.can = Canvas(self , bg="white")
        self.can.grid(row=0, column=1, rowspan=2, columnspan=3,sticky="nsew")
        self.can.config(width=photo.width(), height=photo.height())  
        self.can.create_image(2, 2, image=photo, anchor=NW)

        # Buttons on Start Page
        self.image1 = PhotoImage(file=IMAGE_PATH+"configure.png")
        self.image2 = PhotoImage(file=IMAGE_PATH+"create.png")
        self.image3 = PhotoImage(file=IMAGE_PATH+"upload.png")    
        self.image4 = PhotoImage(file=IMAGE_PATH+"home.png") 
        b1 = tkinter.Button(self, text="Create Website",command=lambda: controller.show_frame(ConsolePage),image=self.image2, compound=LEFT, padx=5, pady=5, font=("comicsansms", 20, "bold"), fg="black", bg="orange")
        b1.grid(row=4, column=2,sticky="nsew")

        b2 = tkinter.Button(self, text="Configure Project",command=lambda: controller.show_frame(ConfigurationPage) ,image=self.image1, compound=LEFT,padx=5, pady=5, font=("comicsansms", 15, "bold"), fg="black", bg="skyblue")
        b2.grid(row=3, column=0,  pady=25,padx=30,sticky="nsew")

        b3 = tkinter.Button(self, text="Upload Website",image=self.image3, compound=LEFT, padx=5, pady=5, font=("comicsansms", 15, "bold"), fg="black", bg="skyblue")
        b3.grid(row=3, column=4,sticky="nsew",pady=25,padx=30,)

        # Back button
        self.back_img = ImageTk.PhotoImage(Image.open(IMAGE_PATH+"back.png"))
        Button(self, text="Back",image=self.back_img, command=lambda: controller.show_frame(StartPage)).place(x=10,y=10)
        

    # open upload folder
    def open_upload_folder(self,path):
        os.startfile(path)

class ConfigurationPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent,bg="white")

        # Back button
        self.back_img = ImageTk.PhotoImage(Image.open(IMAGE_PATH+"back.png"))
        Button(self, text="Back",image=self.back_img, command=lambda: self.back_button(controller)).place(x=10,y=10)
        
        # Page Title
        Label(self, text = 'Website Configuration', font =('Verdana', 35,"bold"),bg="white",fg="blue").pack(side = TOP, pady = 20)
        
        # Side Image
        self.img = ImageTk.PhotoImage(Image.open(IMAGE_PATH+"setting.png"))
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
        self.sub_img= PhotoImage(file=IMAGE_PATH+"submit.png")
        b3 = tkinter.Button(self, text="Upload Variable",image=self.sub_img, compound=LEFT,padx=5, font=("comicsansms", 15, "bold"),command=lambda: self.submit(controller), fg="black", bg="white").place( y = FRAME_HEIGHT-100, x = FRAME_WIDTH/2-400)
    
    # Submit Button Function
    def submit(self,controller):
        global delete_project
        if delete_project == True:
            delete_project = False
            controller.show_frame(ConsolePage)
        else:
            controller.show_frame(ProjectPage)
    
    # Back Button Function
    def back_button(self,controller):
        global delete_project
        if delete_project == True:
            delete_project = False
            controller.show_frame(StartPage)
        else:
            controller.show_frame(ProjectPage)
        
class ConsolePage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent, background="white")
        # Frame for the console box
        put_full_output(0)
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
        self.console.create_text(10, 10, anchor=NW, text="Console", fill="Red", font=(TEXT_FONT, 20, "bold"))
        
        
        self.console.create_text(50, 50, anchor=NW, text=get_data(file=PATH+"\\dependencies\\"+"data.txt"), fill="white", font=(TEXT_FONT, 12, "bold"))
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
        self.console.create_text(50, 50, anchor=NW, text=get_data(file=PATH+"\\dependencies\\"+"data.txt"), fill="white", font=("comicsansms", 12, "bold"))
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
    return data


# get full output  
def get_full_output():
    try:
        with open(PATH+"\\dependencies\\"+"full_output.txt", "r") as f:
            full_output = f.read()
    except:
        full_output = True
    return full_output

# Put full output in file
def put_full_output(x):
    if x==1:
        #print(x)
        with open(PATH+"\\dependencies\\"+"full_output.txt", "w") as f:
            f.write("True")
    else:
        with open(PATH+"\\dependencies\\"+"full_output.txt", "w") as f:
            f.write("False")

full_output =get_full_output()



         





