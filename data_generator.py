from record import Record
from random import random


def generate_records():
    number_of_records = 10
    with open("data.txt", "w") as file:
        for _ in range(number_of_records):
            record = Record(random(), random(), random())
            file.write(record.serialize())


def enter_records():
    number_of_records = int(input("Please enter how many records you want to create:\n"))
    with open("data.txt", "w") as file:
        for _ in range(number_of_records):
            record = Record(float(input("Enter probability of event a")), float(input("Enter probability of event b")),
                            float(input("Enter probability of sum of events")))
            file.write(record.serialize() + " ")
