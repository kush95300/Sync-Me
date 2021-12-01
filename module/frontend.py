import os,sys,shutil
from subprocess import check_call
import threading
from time import time
from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import BOLD
from PIL import Image, ImageTk
from module.backend import *

PATH =os.path.dirname(sys.modules['__main__'].__file__)
IMAGE_PATH = "{}/images/".format(PATH)
LARGE_FONT = ("Verdana", 12)
TEXT_FONT = "comicsansms"
FRAME_WIDTH = 1200
FRAME_HEIGHT = 650
GEOMETRY = "{}x{}".format(FRAME_WIDTH, FRAME_HEIGHT)
delete_project = False
ENV_VARS = []
CODE_Uploaded = False


# Multipage GUI
class myAPP(tkinter.Tk):
    def __del__(self):
        # cred = get_aws_credentials()
        # if cred == [] or cred == None or cred == "Credentials not exist" or cred == ("", "", ""):
        #     cre = set_aws_credentials_empty()
        #     shutil.rmtree("~/.aws/creditentials")
        # else:
        #     cre= set_aws_credentials(aws_access_key_id=cred[0], aws_secret_access_key=cred[1],aws_region=cred[2])

        # print("CRED :{}".format(cred))
        # print("Now Cred = {}".format(get_aws_credentials()))
        print("Destructor called")
    
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

# Detail Page
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

# Project Page
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
        b1 = tkinter.Button(self, text="Create Website",command=lambda: self.make_website(controller=controller),image=self.image2, compound=LEFT, padx=5, pady=5, font=("comicsansms", 20, "bold"), fg="black", bg="orange")
        b1.grid(row=4, column=2,sticky="nsew")

        b2 = tkinter.Button(self, text="Configure Project",command=lambda: controller.show_frame(ConfigurationPage)  ,image=self.image1, compound=LEFT,padx=5, pady=5, font=("comicsansms", 15, "bold"), fg="black", bg="skyblue")
        b2.grid(row=3, column=0,  pady=25,padx=30,sticky="nsew")

        b3 = tkinter.Button(self, text="Upload Website",command=lambda: self.create_project_folder(controller=controller),image=self.image3, compound=LEFT, padx=5, pady=5, font=("comicsansms", 15, "bold"), fg="black", bg="skyblue")
        b3.grid(row=3, column=4,sticky="nsew",pady=25,padx=30,)

        # Back button
        self.back_img = ImageTk.PhotoImage(Image.open(IMAGE_PATH+"back.png"))
        Button(self, text="Back",image=self.back_img, command=lambda: controller.show_frame(StartPage)).place(x=10,y=10)
    
    def create_project_folder(self,controller):
        # Checking Project Variable configuration
        global ENV_VARS
        print(ENV_VARS)
        if ENV_VARS== [] or ENV_VARS[0]=="" or ENV_VARS[0]==None :
            messagebox.showinfo("Error", "Please first Configure the Project")
        else:
            # Update code
            global CODE_Uploaded
            if CODE_Uploaded == True:
                update = messagebox.askyesno("Update", "Do you want to update the code?")
                if update == False:
                    return

            # creating Project folders
            try:
                os.mkdir(PATH+"/Projects/{}".format(ENV_VARS[0]))
                os.mkdir(PATH+"/Projects/{}/Code".format(ENV_VARS[0]))
            except:
                pass
            os.system("start "+PATH+"/Projects/{}/Code".format(ENV_VARS[0]))
            m = messagebox.askokcancel("Are you done with Code?", "Do you want to save the code in the Project Folder?")
            if m == True:
                messagebox.showinfo("Success", "Code Uploaded Successfully (Locally)")
                CODE_Uploaded = True
                create_file(file_name="{}_status.txt".format(ENV_VARS[0]),data="Project : {} \nStatus: Code Uploaded to Local Space but Website Not created".format(CODE_Uploaded),file_path=PATH+"/Projects/{}".format(ENV_VARS[0]))
            else:
                if CODE_Uploaded == True:
                    return
                # Delete Project Folder
                shutil.rmtree(PATH+"/Projects/{}".format(ENV_VARS[0],force=True))
                messagebox.showinfo("Inforamtion", "Project Not Saved. Code Deleted")
                ENV_VARS = []

    def make_website(self,controller):
        global CODE_Uploaded
        
        if CODE_Uploaded == False:
            messagebox.showwarning("Error", "Please Upload the Code First")
        else:
            thread = threading.Thread(target=create_website_thread, args=())
            thread.start()
            messagebox.showinfo("Info", "Website Creation Started, It may take 2-5 minutes to setup website")
            controller.show_frame(ConsolePage)              
            
        

    # open upload folder
    def open_upload_folder(self,path):
        os.startfile(path)

# Variable Configuration Page
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
        input1 = StringVar() 
        Entry(self,textvariable=input1,width = 40,font=("comicsansms",16, "bold"),bg="white").place(x = FRAME_WIDTH/4-220,y = FRAME_HEIGHT/2-160)
        input2 = StringVar()
        Entry(self,show="*",textvariable=input2,width = 40,font=("comicsansms", 16, "bold"),bg="white").place(x = FRAME_WIDTH/4-220,y = FRAME_HEIGHT/2-60)
        input3 = StringVar()
        Entry(self,show="*",textvariable=input3,width = 40,font=("comicsansms", 16, "bold"),bg="white").place(x = FRAME_WIDTH/4-220,y = FRAME_HEIGHT/2+40)
        input4 = StringVar()
        Entry(self,textvariable=input4,width = 40,font=("comicsansms",16, "bold"),bg="white").place(x = FRAME_WIDTH/4-220,y = FRAME_HEIGHT/2+140)

        # Submit Button
        self.sub_img= PhotoImage(file=IMAGE_PATH+"submit.png")
        b3 = tkinter.Button(self, text="Upload Variable",image=self.sub_img, compound=LEFT,padx=5, font=("comicsansms", 15, "bold"),
          command=lambda: self.submit(controller=controller,inputs=[input1.get(),input2.get(),input3.get(),input4.get()]), fg="black", bg="white").place( y = FRAME_HEIGHT-100, x = FRAME_WIDTH/2-400)
    
    # Submit Button Function
    def submit(self,controller,inputs):
        global ENV_VARS

        # Checking inputs are empty or not 
        for i in inputs:
            if i == "" or i == None:
                messagebox.showerror("Error","Please fill all the inputs")
                return

        # Warn user to create website as webcode already exists
        global delete_project
        global CODE_Uploaded
        if delete_project == False and CODE_Uploaded == True:
            messagebox.showwarning("Warning", "First Create Website of Uploaded Code")
            choice = messagebox.askyesno("Warning", "Do you still want to create the Project? \n\n Current Project Code will locally saved. You can set that up again from detail page. ")
            if choice == True:
                pass
            else:
                controller.show_frame(ProjectPage)
        
        # Checking Project already exists or not
        if os.path.exists(PATH+"/Projects/{}".format(inputs[0])):
            messagebox.showerror("Error","Project Already Exists. Choose other name.")
            return

        # Checking AWS CLI is installed or not
        x = test_aws()
        if x == False:
            messagebox.showerror("ERROR","Please Install AWS CLI \n\n Refer the link:\n  https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html")
            return

        # Checking AWS Credentials and  Region is valid or not
        y = test_aws_credentials(profile=inputs[0],aws_access_key_id= inputs[1],aws_secret_access_key= inputs[2],aws_region= inputs[3])
        if y == False:
            messagebox.showerror("Credentials Error","Please Enter the correct AWS Credentials")
            return


        # set the global variable
        ENV_VARS = inputs

        if delete_project == True:
            # Confirm to delete the project
            m=messagebox.askokcancel("Delete Project","Are you sure you want to delete the project?")
            if m == False:
                return
            else:
                # Delete the project and route to Console Page
                delete_project = False
                controller.show_frame(ConsolePage)
        else:
            # Route to Project Page
            messagebox.showinfo("Success","Project Variables Configured Successfully")
            controller.show_frame(ProjectPage)
    
    # Back Button Function
    def back_button(self,controller):
        global delete_project
        if delete_project == True:
            delete_project = False
            controller.show_frame(StartPage)
        else:
            controller.show_frame(ProjectPage)

# Console Page      
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
        
        
        self.console.create_text(50, 50, anchor=NW, text=get_data(file=PATH+"/dependencies/data.txt"), fill="white", font=(TEXT_FONT, 12, "bold"))
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
        global ENV_VARS
        fulloutput=get_full_output()
        self.console.delete(ALL)
        self.console.create_text(10, 10, anchor=NW, text="Console", fill="Red", font=("comicsansms", 20, "bold"))
        try:self.console.create_text(50, 50, anchor=NW, text=get_data(file=PATH+"/"+ENV_VARS[0]+"/output_data.txt"), fill="white", font=("comicsansms", 12, "bold"))
        except:pass
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

# Get ENV VARS
def get_env_vars():
    global ENV_VARS
    return ENV_VARS

# create the project thread
def create_website_thread():
    print("Starting Website Thread")
    global CODE_Uploaded
    global ENV_VARS

    # Create output file
    create_file(file_path=PATH+"/Projects/"+ENV_VARS[0], file_name="output_data.txt",data="",mode="w")

    # Create the project Website
    create_website(website_name=ENV_VARS[0],aws_region=ENV_VARS[3],aws_access_key_id=ENV_VARS[1],aws_secret_access_key=ENV_VARS[2],path=PATH+"/Projects/"+ENV_VARS[0])

    # Update the code uploaded status
    create_file(mode='w',file_name="{}_status.txt".format(ENV_VARS[0]),data="Project : {} \nStatus: Code Uploaded and Website Successfully created".format(CODE_Uploaded),file_path=PATH+"/Projects/{}".format(ENV_VARS[0]))
    
    # import time
    # time.sleep(5)
    
    # Notify the user that the project is created
    messagebox.showinfo("Success","Project Created Successfully")

    # Removing the project environment variables and credentials
    CODE_Uploaded = False
    status =set_aws_credentials_empty(profile_name=ENV_VARS[0])
    if status:
        print("Credentials Removed")
    ENV_VARS = []
    print("Thread Stopped")



# Create APP
def create_app():
    # img = Image.open(PATH+"\\images\\"+"logo.png")
    app = myAPP()
    app.iconbitmap(PATH+"\\images\\"+"logo.ico")
    app.title("Sync Me")
    app.mainloop()
