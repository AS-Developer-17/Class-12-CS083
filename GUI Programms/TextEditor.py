# Module Import 

from ttkbootstrap import *
from tkinter import *
import webbrowser
from random import choice

# Main Function for our Editor Window
def newWindow():

# Sub Function Decleration

    def webAbtUs(): # Opens Github
        webbrowser.open_new_tab("https://github.com/AS-Developer15")
       
        
    def documentation(): # Opens Documentation of the Project
        webbrowser.open_new_tab("https://github.com/AS-Developer15/TextEditor")
      
      
    def formattingWin(): # Opens a window like Notepad

        formattingWindow= Tk()
        formattingWindow.title("Change Style")
        formattingWindow.geometry('450x300')
        
        Label(formattingWindow,text="Change Configuration").pack(pady=10)
       
        mainFrame = Frame(formattingWindow)         
        fontValFrame =  Frame(mainFrame)
        fontSizeFrame=  Frame(mainFrame)
        fontStylFrame=  Frame(mainFrame)
        fontColrFrame=  Frame(mainFrame)
        windBackFrame=  Frame(mainFrame)
        
        Label(fontValFrame,text="Face Value",width=12,anchor="w").pack(side="left",pady=5)
        fontVal =  Entry(fontValFrame)
        fontVal.pack(side= "left",padx=3)
        fontValFrame.pack()
               
        Label(fontSizeFrame,text="Size Value",width=12,anchor="w").pack(side="left",pady=5)
        fontSizeVal =  Entry(fontSizeFrame)
        fontSizeVal.pack(side= "left",padx=3)
        fontSizeFrame.pack()
        
        Label(fontStylFrame,text="Style Value",width=12,anchor="w").pack(side="left",pady=5)
        fontStyleVal=  Entry(fontStylFrame)
        fontStyleVal.pack(side= "left",padx=3)        
        fontStylFrame.pack()
       
        Label(fontColrFrame,text="Color Value",width=12,anchor="w").pack(side="left",pady=5)
        fontColorVal=  Entry(fontColrFrame)
        fontColorVal.pack(side= "left",padx=3)        
        fontColrFrame.pack()
       
        Label(windBackFrame,text="Window Color",width=12,anchor="w").pack(side="left",pady=5)
        windColorVal=  Entry(windBackFrame)
        windColorVal.pack(side= "left",padx=3)        
        windBackFrame.pack()
       
        def changeConfig(): # Sub Function for regulating all those changes made by the user

            fontFaceValue   = str(fontVal.get()).lower()
            fontSizeValue   = fontSizeVal.get()
            fontWeightValue = str(fontStyleVal.get()).lower()
            fontColorValue  = str(fontColorVal.get())
            windowColorValue= str(windColorVal.get())
          
          
            if fontFaceValue == "":
                fontFaceValue="calibri"
            
            if fontSizeValue=='':
                fontSizeValue= int(12)

            if fontWeightValue == "":
                fontWeightValue="normal"
            
            if fontColorValue=="":
                fontColorValue= textEntryWindow.cget("foreground")
           
            if windowColorValue=="": 
                windowColorValue=textEntryWindow.cget("background")
        
                
            fontConfig= font.Font(family=fontFaceValue,size=fontSizeValue,weight=fontWeightValue)
            textEntryWindow.config(font=fontConfig)
            textEntryWindow.config(foreground=fontColorValue)
            textEntryWindow.config(background=windowColorValue)
        
            formattingWindow.bell()
            formattingWindow.destroy()
        mainFrame.pack()         
        Button(formattingWindow,text="Change Configuration",command=changeConfig).pack(pady=10)
        formattingWindow.mainloop()
    
    
    def fileSave(): # Saving File using open command 
        nameWindow= Tk()
        nameWindow.geometry("300x150")
        nameWindow.title("Save File" )
          
        Label(nameWindow,text="Choose File Name",font=(24)).pack(pady=20)
      
        fileSavingFrame = Frame(nameWindow)
        fileName = Entry(fileSavingFrame)
        fileName.pack(side="left")
        fileSavingFrame.pack() 
        def saveFile():
            savingName = fileName.get()   
            data = textEntryWindow.get(index1=1.0,index2="end")
            
            
            # File Path to be changed in later updates.
            
             
            with open(f"./{savingName}.txt","w") as file:
                file.write(data)
            nameWindow.bell()  
            nameWindow.destroy()  
        Button(fileSavingFrame,text="Save",command=saveFile).pack(side="left",padx=10)
        nameWindow.mainloop()


    def exitEditor(): # Destroying the window for exiting
        window.bell()
        window.destroy()
        

# Program Window Configuration

    themes=['cosmo', 'flatly', 'litera', 'minty', 'lumen', 'sandstone', 'yeti', 'pulse', 'united', 'morph', 'journal', 'darkly', 'superhero', 'solar', 'cyborg', 'vapor', 'simplex', 'cerculean']
   
    window = Window("Text Editor",themename=choice(themes))
    window.geometry("1000x500")
    window.maxsize(window.winfo_screenwidth(),window.winfo_screenheight())



# File Menu
    menuBar = Menu(window)
    fileMenu =Menu(menuBar,tearoff=0)
    fileMenu.add_command(label="New",command=newWindow)
    fileMenu.add_command(label="Save",command=fileSave)
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit",command=exitEditor)
    menuBar.add_cascade(label="File",menu=fileMenu)



# Editing Menu
    editingMenu= Menu(menuBar,tearoff=0)
    editingMenu.add_command(label="Edit",command=formattingWin)
    menuBar.add_cascade(label="Edit",menu=editingMenu)



# Help Menu
    helpMenu = Menu(menuBar,tearoff=0 )
    helpMenu.add_command(label="About Us",command=webAbtUs)
    helpMenu.add_command(label="Documentation",command=documentation) 
    menuBar.add_cascade(menu=helpMenu,label="Help")
    window.config(menu=menuBar)



# Actual Window
    textEntryWindow = ScrolledText(window,background="white",width=200,height=25)
    textEntryWindow.pack(fill= tk.BOTH , expand=True)
    window.mainloop()


       
newWindow()

"""
Future Updates Include 
>> File Saving Path
>> Word Wrapping
>> Opening a Text File
>> Cut, Copy, Paste, Menu
"""