from tkinter import *
from ttkbootstrap import *
from PIL import Image,ImageTk
import mysql.connector

db= mysql.connector.connect(user = "root",password="Aru@1234",host = "localhost",database = "lms")
csr= db.cursor()
# First Screen to be displayed after opening.
def Login():
    # Window Decleration
    LoginWindow= Window("Log In" ,themename="darkly")
    LoginWindow.geometry("600x225")
    LoginWindow.maxsize(600,225)

    # Adding Widgets
    adminInputFrame = Frame(LoginWindow)
    passValFrame    = Frame(LoginWindow)
    Label(LoginWindow,text="Log In",font=("bold",20)).pack(pady=10)

    Label(master=adminInputFrame,text="Admin Id",width=15).pack(side="left",pady=15)
    adminIdVal = Entry(adminInputFrame)
    adminIdVal.pack(side="left",padx=10)

    Label(master=passValFrame,text="Password",width=15).pack(side="left",pady=15)
    passVal = Entry(passValFrame,show="*")
    passVal.pack(side="left",padx=10)

    adminInputFrame.pack()
    passValFrame.pack()
    
    
    def LogIn():
        csr.execute("Select Admin_Control_ID,Password from admindata")
        passwordAdminKeyVal= csr.fetchall()
        idValue  = str(adminIdVal.get())
        passValue= str(passVal.get())
        if (idValue,passValue) in passwordAdminKeyVal:
            LoginWindow.destroy()
            MainWindow()
        else:
            LoginWindow.bell()
            

    Button(LoginWindow,text="Log In",command=LogIn).pack(pady=10)
    LoginWindow.mainloop()

# Main Home Screen
def MainWindow():
    # Window Configuration
    MainWin= Window("Shreyos Library Management System",themename="darkly" )
    # MainWin.minsize(MainWin.winfo_screenwidth(),MainWin.winfo_screenheight())
    MainWin.maxsize(MainWin.winfo_screenwidth(),MainWin.winfo_screenheight())
    
    # Adding Widgets 
    
    Label(MainWin,text="Shreyos Library Management System",font=("regular",25)).pack()
    
    flexButtonFrame = tk.Frame(MainWin)
    subLenderFrame= tk.Frame(flexButtonFrame)
    subBooksFrame = tk.Frame(flexButtonFrame)
    subRulesFrame = tk.Frame(flexButtonFrame)
    subExportFrame= tk.Frame(flexButtonFrame)
    
    img   = Image.open("dbms.jpg")
    tkImg = ImageTk.PhotoImage(img.resize((50,50)))    
    Label(subLenderFrame, image=tkImg).pack()
    Label(subLenderFrame,text="Borrower's Data",font=(16),foreground="lightblue").pack()
    Label(subLenderFrame,wraplength=175,text="Allow us to maintain borrower's record from the member's table.",justify="center").pack(padx=10)
    Button(subLenderFrame,text= "CheckIt").pack(pady=10)

    Label(subBooksFrame, image=tkImg).pack()
    Label(subBooksFrame,text="Book Collection",font=(16),foreground="lightblue").pack()
    Label(subBooksFrame,wraplength=175,text="Allow us to maintain books availiable in Library.",justify="center").pack(padx=10)
    Button(subBooksFrame,text= "CheckIt").pack(pady=10)

    Label(subRulesFrame, image=tkImg).pack()
    Label(subRulesFrame,text="Terms and Condition ",font=(16),foreground="lightblue").pack()
    Label(subRulesFrame,wraplength=175,text="Provide us with the instruction manual for using this software.",justify="center").pack(padx=10)
    Button(subRulesFrame,text= "CheckIt").pack(pady=10)

    Label(subExportFrame, image=tkImg).pack()
    Label(subExportFrame,text="Export Data",font=(16),foreground="lightblue").pack()
    Label(subExportFrame,wraplength=175,text="Allow us to export library data in csv or pdf format.",justify="center").pack(padx=10)
    Button(subExportFrame,text= "CheckIt").pack(pady=10)

    subLenderFrame.pack(padx=20 ,side=LEFT)
    subBooksFrame.pack( padx=20 ,side=LEFT)
    subRulesFrame.pack( padx=20 ,side=LEFT)
    subExportFrame.pack(padx=20 ,side=LEFT)


    Label(MainWin,text="This software is developed and managed by AS.Developer and Company.").pack(anchor=S,side=BOTTOM)
    flexButtonFrame.pack(pady=100)
    MainWin.mainloop()
    ...

def memberData():
    memberWindow= Window("Member Window")
    memberWindow.mainloop()
    
    ...
Login()