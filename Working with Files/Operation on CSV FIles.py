# Working with CSV
import faker, random, csv
with open("Class Wise Marks Record.csv",mode="w+")as mrec:
    writer= csv.writer(mrec)
    reader= csv.reader(mrec)
    writer.writerow