import random as r
nList = list()
solutions= list()
for _ in range(0,int(input("How many numbers in the array you want>>> "))):
    randVal= r.randint(0,100)
    if randVal not in nList:
        nList.append(randVal)
print(f"The array is {nList}", sep="\t")
sumInp = int(input("Type the number you want (less than 200)>>>"))
for mainInt in range(0, int(len(nList))) :
    for subInt in range(mainInt,len(nList)):
        if mainInt+ subInt==sumInp:
            soln=(mainInt, subInt)  
            solutions.append(soln)
print(solutions)
