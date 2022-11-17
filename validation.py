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


def count_runs(initial_numbers):
    runs_count = 1
    for i in range(len(initial_numbers)-1):
        if initial_numbers[i] > initial_numbers[i + 1]:
            runs_count += 1
    return runs_count


def calculate_theoretical_number_of_phases(initial_numbers):
    return int(math.ceil(math.log2(count_runs(initial_numbers))))


def validate(number_of_tests=1000):
    number_of_records = 10
    number_of_tests_passed = 0
    for _ in range(number_of_tests):
        #data_generator.generate_fake_records(number_of_records)
        phases = data_sorter.natural_merging_sort()
        sorted_by_program = load_data_sorted_by_program()
        data_from_input = load_data_from_generator()
        sorted_by_validator = sorted(data_from_input, key=float)
        theoretical_phases = calculate_theoretical_number_of_phases(data_from_input)
        if sorted_by_program == sorted_by_validator and len(sorted_by_program) == number_of_records and phases <= theoretical_phases:
            number_of_tests_passed += 1
        else:
            print(f"Test failed! Passed {number_of_tests_passed} out of {number_of_tests}")
            if sorted_by_program != sorted_by_validator:
                print("Incorrectly sorted data")
            if len(sorted_by_program) != number_of_records:
                print("Too many numbers or missing numbers!")
            if phases > theoretical_phases:
                print(f"Program did something slower then expected! ({phases} instead of {theoretical_phases} phases) ")
            break
    print(f"Passed all tests: {number_of_tests_passed} out of {number_of_tests}")
