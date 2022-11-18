import math

import constants
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
    return load_data("tape3.txt")


def count_runs(initial_numbers):
    runs_count = 1
    for i in range(len(initial_numbers) - 1):
        if initial_numbers[i] > initial_numbers[i + 1]:
            runs_count += 1
    return runs_count


def calculate_theoretical_number_of_phases(initial_numbers):
    return int(math.ceil(math.log2(count_runs(initial_numbers))))


def calculate_blocking_factor():
    return constants.size_of_block / 1  # We count block size in number of records.


def calculate_theoretical_number_of_reads_and_writes(number_of_records, initial_numbers):
    return 4 * number_of_records * calculate_theoretical_number_of_phases(initial_numbers) / calculate_blocking_factor()


def check_io_stats(tape, max_io):
    print(f"Tape {tape.filename} disk IO stats:")
    print(
        f"Reads: {tape.read_operations}, expected max {max_io}\nWrites: {tape.write_operations}, expected max {max_io}")


def validate(number_of_tests):
    number_of_records = 10
    number_of_tests_passed = 0
    for _ in range(number_of_tests):
        data_generator.generate_fake_records(number_of_records)
        data_from_input = load_data_from_generator()

        phases, tape1, tape2, tape3 = data_sorter.natural_merging_sort(verbose=1)
        theoretical_phases = calculate_theoretical_number_of_phases(data_from_input)

        sorted_by_program = load_data_sorted_by_program()

        sorted_by_validator = sorted(data_from_input, key=float)

        theoretical_io = calculate_theoretical_number_of_reads_and_writes(number_of_records,
                                                                          data_from_input)
        check_io_stats(tape1, theoretical_io)
        check_io_stats(tape2, theoretical_io)
        check_io_stats(tape3, theoretical_io)
        if sorted_by_program == sorted_by_validator and len(
                sorted_by_program) == number_of_records and phases <= theoretical_phases:
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
