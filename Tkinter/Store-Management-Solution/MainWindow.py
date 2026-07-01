# Module Import
from tkinter import * 
from ttkbootstrap import *
import pandas

# Variable Decleration

# Admin Password Key Pairs
adm_pass_dict={"Aradhya":"1234","admin":"1234"}
# Current Admin
curAdm =""
 
def loginWin():
    lWin= Window("Login","darkly")
    lWin.geometry("600x250")
    lWin.maxsize(600,250)
    lWin.minsize(600,250)
   
    # Main Label
    Label(lWin,text="Log In").pack()
   
    # Admin 
    admInpFrame= Frame(lWin)
    Label(admInpFrame, text="User Name:").pack(side="left")
    admInp= Entry(admInpFrame)
    admInp.pack(side='right',padx=15 )

    #PassWord
    passValFrame= Frame(lWin)
    Label(passValFrame, text="Pass Code :").pack(side="left")
    pasInp= Entry(passValFrame)
    pasInp.pack(side='right',padx=15 )
   
    def loginAdm():
        adminVal= str(admInp.get())
        passCode= str(pasInp.get())
        if adm_pass_dict.get(adminVal) == passCode: 
            mainWindow()
            lWin.destroy()
            curAdm= adminVal
        else:
            lWin.bell()         
        ...

    admInpFrame.pack()
    passValFrame.pack()
    Button(lWin, command=loginAdm, text="Log In").pack(pady=10 )
   
    lWin.mainloop()
def dummyFunc():
    ...
def mainWindow():
    mWin= Window("Shreyos Inventory Management System ", themename='darkly')
    mWin.geometry("750x500")
    flexBoxFrame= Frame(mWin)
    
    flexBoxFrame.p()
    Label(mWin,text="Inventory Management System").pack()
    
    
    
loginWin()