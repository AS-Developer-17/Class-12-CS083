import random, faker, csv
def FileMaker():
    with open("PassCodeUserPair.csv", "w+", newline="") as lFile:
        writer = csv.DictWriter(lFile, fieldnames=("Id", "PassCode"), delimiter="|")
        # writer.writeheader(('Id', 'Passcode'))
        seen_ids = set()
        fake = faker.Faker()
        for _ in range(int(input("Type the sample size: "))):
            user_id = fake.name()
            if user_id not in seen_ids:
                seen_ids.add(user_id)
                writer.writerow({"Id": user_id, "PassCode": fake.password(random.randint(8,15), True, True, True, True)})
                
#Linear Sort Approach 

def LoginFunction():
    with open("PassCodeUserPair.csv", "r", newline="") as lFile:
        reader = csv.DictReader(lFile, delimiter='|', fieldnames=("Id", "PassCode"))
        IdVal = input(" Enter your Id: ")
        PsVal = input(" Enter your Passcode: ")
        for rows in reader :
            if reader["Id"]== IdVal:
                if reader("PassCode")==PsVal:
                    print("Your Access is Validated")
                else : 
                    raise("Enter a Valid Passcode... ")
            else : 
                raise("Enter a Valid Id... ")
FileMaker()