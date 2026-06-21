import random
with open("Data1.txt",mode="w")as file:
    print(f'''
File Opening Mode is {file.mode}
Name of the file is {file.name}
File is closed or not {file.closed} 
Is the following file readable {file.readable}
Is the following file writable {file.writable}
''')

# MailMerge Idea
def MailMergeFunction():
    date =input("Type Date in DD/Month/YYYY ")
    event=input("Event: ")
    
    invPersons=list() 

    for _ in range(0,int(input("How Many People are Invited: "))):
        invPersons.append(str(input("Type their name: ")))
        
    for nameVal in invPersons:
        with open(f"{nameVal}Invitation.txt", mode="w") as file:
            file.write(f'''To
    {nameVal}
    
    I joyfully invite you for our {event}!
    Kindly join us on our special day.
    {date}
    Please Save The Date.
    
    Your Lovingly
    AS.Developer
    ''')

#Reciept Generator
def RecieptGenerator():
    goods=list()
    while True:
        code = input("Type the Item Code: ")
        if code ==".":
            break
        quantity =int(input("Type Quantity: "))
        cost = int(input("Type the Cost of Good."))
        value = cost*quantity
        goods.append((code, quantity, cost,value ))
        print(goods)
    with open ("reciept.txt",mode="w")as reciept:
        totalAmount=0
        reciept.write('''       
                               Reliance Retail Limited 
                                 RELIANCE SMART POINT
                      GF Ujjain Khata No. 645 (140-1425 Fasan) 
                      Khasra No 293, Mauza Ujjain Tehsil Kashipur
                      ---------------------------------------------
                      |  Code  |    Qty    |    Cost    |   Value   |
                      --------------------------------------------- ''')
        for gval in goods:
            reciept.write(f'''
                      |  {gval[0]} | {gval[1]}  |  {gval[2]}   |  {gval[3]} |''')
            totalAmount+= int(gval[3])
        reciept.write(f'''
                      ---------------------------------------------
                               You have saved Rs.{random.randint(int(totalAmount/10),int(totalAmount*0.2))} 
                      ---------------------------------------------
                               Total Amount : {totalAmount}
                      ---------------------------------------------                      
                      ''')

