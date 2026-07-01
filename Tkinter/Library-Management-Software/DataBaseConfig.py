import datetime
from faker import Faker
fake = Faker()
import random
import mysql.connector as mc 
db  = mc.connect(user="root",host="localhost",password="Aru@1234",database="LMS")
csr = db.cursor()

csr.execute("Select * from memberdata")
print(len(csr.fetchall()))

cmdIns="Insert into memberdata values(%s,%s,%s,%s,%s,%s,%s,%s)"

for dataRows in range(1000,1151):
  
    fName= (fake.first_name_female(),fake.first_name_male(),fake.first_name_nonbinary())
    lName= (fake.last_name_female(),fake.last_name_male(),fake.last_name_nonbinary()) 
    
    rndNameInt= random.choice((0,1,2))
    intVal = rndNameInt
    fNameVal = fName[intVal]
    lNameVal = lName[intVal]
    if intVal ==0:
        gender = "Female"
    if intVal==1 :
        gender = "Male"
    if intVal==2 :
        gender="Non Binary"
    phoneNum = fake.country_calling_code()+ " "+ fake.phone_number()
    birthdate = fake.date_of_birth(maximum_age=80,minimum_age=6)
    joining= fake.date_between(start_date=datetime.date(2020,1,1))
    MembershipType= random.choice(["Antimony","Radon","Bismuth","Amber"])
    insArray=(dataRows,fNameVal,lNameVal,birthdate,joining,MembershipType,gender,phoneNum)    
    csr.execute(cmdIns,insArray)
    db.commit()
print(f"Sucessfully inserted {11000-1000}")
'''
def books():
    ...
    
# Books Data
for booksRow in range(1000,1200):
    author = fake.name()
    quantity= random.randint(0,15)
    cost= random.randint(150 , 5000)
    edition= random.randint(1,15)



# Membership
>> Bismuth : Weekly
>> Amber : Monthly
>> Antimony : Yearly
>> Radon : Lifetime

# Admin Table

# roles= ("Owner","Manager","Worker","Worker","Record Keeper","Record Keeper","Accountant","Book Keeper","Book Keeper","Book Keeper","Book Keeper")
'''