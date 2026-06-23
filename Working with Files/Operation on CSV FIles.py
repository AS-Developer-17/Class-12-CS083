# Operation on CSV

import faker, random, csv
fake = faker.Faker()

def RandomMarksDataGenerator():
    def marks():
        return random.randint(0,100)

    def write_student_row(writer, roll_no):
        writer.writerow([roll_no, fake.name(), marks(), marks(), marks(), marks()])

    with open("Class Wise Marks Record.csv", mode="w+", newline='') as mrec:
        writer = csv.writer(mrec, delimiter=',')
        writer.writerow(["Roll No", "Name", "Maths", "Physics", "Chemistry", "Computer Science"])
        for index in range(1000, 1000 + int(input("Type the number of students... "))):
            write_student_row(writer, index)

#Using Reader Method
def NormalReader():
    with open("Class Wise Marks Record.csv", mode="r") as mrec:
        for me in csv.reader(mrec,delimiter=","):
            print(me[1:3])

#Using DictReader Method
def DictReader():
    with open("Class Wise Marks Record.csv", mode="r") as mrec:
        reader = csv.DictReader(mrec, delimiter=",")
        for row in reader:
            print(row["Name"])
            print(row["Roll No"])
            print(row)
        
def RandomMarksGeneratorDictWriter():
    def marks():
        return random.randint(0,100)

    with open("Class Wise Marks Record.csv", mode="w+", newline='') as mrec:
        fieldnames = ["Roll No", "Name", "Maths", "Physics", "Chemistry", "Computer Science"]
        writer = csv.DictWriter(mrec, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        for index in range(1000, 1000 + int(input("Type the number of students... "))):
            writer.writerow({
                "Roll No": index,
                "Name": fake.name(),
                "Maths": marks(),
                "Physics": marks(),
                "Chemistry": marks(),
                "Computer Science": marks()
            })
RandomMarksGeneratorDictWriter()
