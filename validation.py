import math

import data_generator
import data_sorter


def load_data(filename):
    data = []
    with open(filename) as file:
        for line in file:
            elements = line.split(" ")
            if len(elements) == 3:
                data.append(float(elements[0]))
            else:
                print("Error in file format\n")
                break
    return data


def load_data_sorted_by_program():
    return load_data("tape3.txt")


def load_data_from_generator():
    return load_data("data.txt")


def validate(number_of_tests=1000):
    number_of_records = 10
    for _ in range(number_of_tests):
        data_generator.generate_fake_records(number_of_records)
        phases = data_sorter.natural_merging_sort()
        sorted_by_program = load_data_sorted_by_program()
        data_from_input = load_data_from_generator()
        sorted_by_validator = sorted(data_from_input, key= float)
        if sorted_by_program == sorted_by_validator and len(sorted_by_program) == number_of_records:
            print("Test passed")
        else:
            print("Test failed!")
