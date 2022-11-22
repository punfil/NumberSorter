import math
import random
import shutil

import constants
import data_generator
import data_sorter


def calculate_max_theoretical_number_of_phases(initial_numbers_cnt):
    return int(math.ceil(math.log2(initial_numbers_cnt)))


def calculate_avg_theoretical_number_of_phases(initial_numbers_cnt):
    return int(math.ceil(math.log2(initial_numbers_cnt / 2)))


def calculate_blocking_factor():
    return constants.size_of_block / 1  # We count block size in number of records.


def calculate_max_theoretical_number_of_reads_and_writes(number_of_records):
    return 4 * number_of_records * calculate_max_theoretical_number_of_phases(
        number_of_records) / calculate_blocking_factor()


def calculate_avg_theoretical_number_of_reads_and_writes(number_of_records):
    return 4 * number_of_records * calculate_avg_theoretical_number_of_phases(
        number_of_records) / calculate_blocking_factor()


def calculate_io_stats(tape1, tape2, tape3):
    return tape1.read_operations + tape2.read_operations + tape3.read_operations + tape1.write_operations + tape2.write_operations + tape3.write_operations


def validate_io_operations_and_phases():
    for _ in range(1000):
        num_records = 15
        data_generator.generate_fake_records(num_records)
        shutil.copyfile("tape3.txt", "backup.txt")
        phases, tape1, tape2, tape3 = data_sorter.natural_merging_sort(0)
        max_theoretical_phases = calculate_max_theoretical_number_of_phases(num_records)

        max_theoretical_io = calculate_max_theoretical_number_of_reads_and_writes(num_records)

        sum_of_io_operations = calculate_io_stats(tape1, tape2, tape3)

        print(
            f"Disk IO stats.\nReads/writes: {sum_of_io_operations}, expected max {max_theoretical_io}")
        print(f"Sorted in {phases}. Expected max {max_theoretical_phases}")
        if sum_of_io_operations > 66:
            assert sum_of_io_operations <= max_theoretical_io
            assert phases <= max_theoretical_phases
