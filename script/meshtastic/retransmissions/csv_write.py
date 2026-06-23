import csv

def csvWrite(path, data):
    with open(path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)