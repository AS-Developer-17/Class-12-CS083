import numpy, random
# Array Generation
def ArrayGenNumpy(): 
    rng= numpy.random.default_rng()
    aVal = rng.random(55) 
    print(aVal)

def ArrayGenRan():
    arrayVal = list()
    iVal = int(input('Type the maximum value in the array'))
    for me in range(0,int(input("Type the array length"))):
        rInt = random.randint(0,iVal)
        arrayVal.append(rInt)
        print(arrayVal)
ArrayGenRan()
print(random.randrange(0, 100 , 2))