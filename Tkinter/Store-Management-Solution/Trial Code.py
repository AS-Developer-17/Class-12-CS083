# Login Function
admDic= {"Aradhya":"1234", "admin":"1234"}
usnInp= input("User: ")
pasInp= input("Pass: ")


if admDic.get(usnInp)== pasInp:
    print("Enter")
else:
    print("Kick Off")