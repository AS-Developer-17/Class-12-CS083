from datetime import date
import random
import faker
fake = faker.Faker()
# Name Generation
'''
# Important Method For Obtaining First and Last Name
      {fake.name().split(" ")[0]} 

'''
print(f''' Generating Names
        {fake.name().split(" ")[0]} 
        {fake.name_male()}
        {fake.name_female()}
        {fake.name_nonbinary()}
      ''',sep="\n")
# Date of Birth Generation
dob = fake.date_of_birth(minimum_age=1,maximum_age=99)
day = dob.day
month= dob.month
year = dob.year
print(f'''Generating Ages:
     Date of Birth { dob }
     Date { day}
     Month { month}
     Year {year }
     Age { date.today().year- dob.year}
     
     For Age Generaion without Date
     random.randint(1,Max Val)
     Random Age: {random.randint(1,99)}
      ''')
