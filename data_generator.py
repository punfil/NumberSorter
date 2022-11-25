import shutil
from random import uniform, randint

from record import Record


def load_from_file(filename):
    shutil.copy(filename, "tape3.txt")


def generate_records(number_of_records=10):
    with open("tape3.txt", "w+") as file:
        for _ in range(number_of_records):
            record = Record(uniform(0, 1), uniform(0, 1), uniform(0, 1))
            file.write(record.serialize())


def generate_fake_records(number_of_records=10):
    with open("tape3.txt", "w+") as file:
        for _ in range(number_of_records):
            record = Record(randint(100, 199), randint(100, 199), randint(100, 199))
            file.write(record.serialize())


def enter_records():
    number_of_records = int(input("Please enter how many records you want to create:\n"))
    with open("data.txt", "w") as file:
        for _ in range(number_of_records):
            record = Record(float(input("Enter probability of event a")), float(input("Enter probability of event b")),
                            float(input("Enter probability of sum of events")))
            file.write(record.serialize())
