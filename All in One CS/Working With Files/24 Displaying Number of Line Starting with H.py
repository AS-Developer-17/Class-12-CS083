# Particular Solution
def particularSolution():
    with open("24.txt","r")as rFile:
        countVal = 0 
        for me in rFile :
            if me[0].upper()== "H":
                countVal+=1
                print(countVal)

# Generalized Solution
def genSolution():
    countval = 0
    with open("24.txt", "r")as rFile:

        inpVal = input("Type the letter to be the first one>>> ")
        for me in rFile:
            if inpVal.upper()==me[0].upper():
                countVal+=1 
    reader= rfile.readline()
    print(reader)   
    print()
    return countVal
print(genSolution())