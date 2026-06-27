import csv,random
with open("Questionaire.csv",mode="r") as qsFileL:
    reader=list(csv.reader(qsFileL))

    score = 0
    askedQuestions=set()
    while True:
        while True:
            print("HI ") 
            question= random.randint(0,len(reader))
            if question not in askedQuestions:
                askedQuestions.add(question)
                print(f''' 
Q){reader[question][0]}

A) {reader[question][1]}
B) {reader[question][2]}
C) {reader[question][3]}                      
D) {reader[question][4]}
                      ''' )

                if input("Choose Wisely !!!  ").upper ()==reader[question][5]:
                    score+=1
                    print(f"Correct Answer \n Your current score is: {score}")
                    continue
                else : 
                    print(f"Incorrect Answer \n Your score is: {score} \n The correct answer is {reader[question][5]}") 
                    break
                
                    if input("Press [A] to play again... ").upper() !="A" :
                        break