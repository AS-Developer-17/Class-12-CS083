matrixA=[[1,2],[4,5]]
matrixB=[[3,54,2],[2334,455,5]]

def Order(matrix): 
    (len(matrix),len(matrix[0]))
 
def Trace(matrix):
    TraceVal = 0
    if len(matrix) == len(matrix[0]):
        for index in range(0,len(matrix)):
            TraceVal += matrix[index][index]
        print("Trace of the matrix is : ",TraceVal )

def Addition(ma, mb):
   
    sMatrix=[]
    for _ in range(0,len(ma)):
        column= []
        for _ in range(0,len(ma[0])):
                column.append(0)
        sMatrix.append(column)
    
    for r in range(0,len(ma)):
        for c in range(0,len(ma[0])):
            sMatrix[r][c] = ma[r][c] +mb[r][c]# Swap With Minus to obtain 
    print(sMatrix)
    
def MatrixMultiplication(ma, mb):
    if len(ma[0])== len( mb):

        #Matrix 
        sMatrix=[]
        for _ in range(0,len(ma)):
            column= []
        for _ in range(0,len(mb[0])):
                column.append(0)
        sMatrix.append(column)

# Addition of Mechanism:
        for _ in range(0,len(ma)):
            column= []
        for _ in range(0,len(mb[0])):
                column.append(0)
        sMatrix.append(column)

        
    else :
        raise("Please Enter a Valid Matrix... ")

def Det2(matrix):
    if len(matrix)and len(matrix[0])==2 :
        detVal = (int(matrix[0][1])*int(matrix[0][1]))-(int(matrix[0][1])*int(matrix[0][1]))
    else: 
        raise("Please enter a valid matrix... ")
    print("The Value of Determinant is : ",detVal)

def Det3(matrix ):
    
    ...
    
    
    
#Constraint Satisfaction Problem
