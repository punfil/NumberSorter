import os

import data_generator
import validation
from tape import Tape


def display_menu() -> None:
    """
    Displays the main menu in the program
    :rtype: None
    """
    print("Hello and welcome to the Disk Sorter!")
    print("0. Load data from file")
    print("1. Automatically generate data")
    print("2. Enter the data manually")
    print("3. Sort the files")
    print("4. Quit")


def choose_menu_option() -> int:
    """
    Reads the menu option chosen by user and returns it.
    :rtype: int
    """
    option_chosen = int(input("Please select menu option\n"))
    return option_chosen


def distribution(input_tape: Tape, tape1: Tape, tape2: Tape) -> int:
    """
    Distributes records between tapes and returns how many times it switched between tapes.
    :rtype: int
    :return: How many times did the function switch between tapes.
    :param input_tape: Tape all the records are on.
    :param tape1: First tape the records will be written to.
    :param tape2: Second tape the records will be written to.
    """
    tape1.clear_file()
    tape2.clear_file()
    current_tape = tape1
    # How many times was the tape switched
    switched_tapes = 0
    # Load data from the input tape
    last_record, current_record, end_of_series = input_tape.fetch_new_record(None)
    while True:
        if current_record is None:
            break
        if end_of_series is True:
            switched_tapes += 1
            current_tape = tape1 if current_tape == tape2 else tape2
        current_tape.add_record_to_block(current_record)
        last_record, current_record, end_of_series = input_tape.fetch_new_record(current_record)
    tape1.flush_write()
    tape2.flush_write()
    input_tape.flush_read()
    return switched_tapes


def natural_merging_sort(verbose: int) -> (int, Tape, Tape, Tape):  # 2+1 edition

    tape3 = Tape("tape3.txt")  # Load file with data

    # Display content of the tape before sorting
    print("Displaying content of tape before sorting")
    tape3.print_content()

    # Perform initial distribution
    tape1 = Tape("tape1.txt")
    tape2 = Tape("tape2.txt")
    switched_tapes = distribution(tape3, tape1, tape2)
    finished_next_time = False
    if switched_tapes == 1:
        finished_next_time = True
    if switched_tapes == 0:
        return switched_tapes, tape1, tape2, tape3
    tape3.clear_file()  # Get ready to write here
    phase_count = 0

    # Sort till there's one series (when all numbers distributed to one tape)
    while True:
        # Fetch one record at the beginning for each tape
        last_tape1, curr_tape1, end_of_series_tape1 = tape1.fetch_new_record(None)
        last_tape2, curr_tape2, end_of_series_tape2 = tape2.fetch_new_record(None)
        go_inside = True  # Emulation of do while, enter the loop at least once.
        while tape1.end_of_file is False and tape2.end_of_file is False or go_inside is True:
            go_inside = False
            # During current series switch between data from tapes depending on curr_value
            while end_of_series_tape1 is False and end_of_series_tape2 is False:
                # Get data from tape1
                while end_of_series_tape1 is False and curr_tape1 <= curr_tape2:
                    tape3.add_record_to_block(curr_tape1)
                    last_tape1, curr_tape1, end_of_series_tape1 = tape1.fetch_new_record(curr_tape1)
                # Get data from tape2
                while end_of_series_tape1 is False and end_of_series_tape2 is False and curr_tape1 > curr_tape2:
                    tape3.add_record_to_block(curr_tape2)
                    last_tape2, curr_tape2, end_of_series_tape2 = tape2.fetch_new_record(curr_tape2)
            # When data (of current series) remain on only one tape, write all of them to the output tape
            while end_of_series_tape1 is False:
                tape3.add_record_to_block(curr_tape1)
                last_tape1, curr_tape1, end_of_series_tape1 = tape1.fetch_new_record(curr_tape1)
            while end_of_series_tape2 is False:
                tape3.add_record_to_block(curr_tape2)
                last_tape2, curr_tape2, end_of_series_tape2 = tape2.fetch_new_record(curr_tape2)
            # We change the series to the next one
            end_of_series_tape1 = False
            end_of_series_tape2 = False
            # Corner case - when there are only few numbers, it still should sort it, not just rewrite
            if (
                    tape1.end_of_file is True or tape2.end_of_file is True) and curr_tape1 is not None and curr_tape2 is not None:
                go_inside = True
        # When the end_of_file flag is set there might be still some numbers in cache.
        while curr_tape1 is not None:
            tape3.add_record_to_block(curr_tape1)
            last_tape1, curr_tape1, end_of_series_tape1 = tape1.fetch_new_record(curr_tape1)
        while curr_tape2 is not None:
            tape3.add_record_to_block(curr_tape2)
            last_tape2, curr_tape2, end_of_series_tape2 = tape2.fetch_new_record(curr_tape2)
        # Clear all the variables inside the files
        tape1.flush_read()
        tape2.flush_read()
        # Get tapes ready for next iteration
        tape1.clear_file()
        tape2.clear_file()
        tape3.flush_write()
        phase_count += 1
        if verbose == 1:
            print(f"Printing content of tape after {phase_count} phase!")
            tape3.print_content()
        if finished_next_time:
            break
        switched_tapes = distribution(tape3, tape1, tape2)
        if switched_tapes == 1:
            finished_next_time = True
        if switched_tapes == 0:
            break
        tape3.clear_file()

    print(f"Sorting finished!")
    if verbose == 0:
        print(f"Printing content of tape after sorting finished!")
        tape3.print_content()
    return phase_count, tape1, tape2, tape3


def quit_program():
    delete_file("tape1.txt")
    delete_file("tape2.txt")
    delete_file("tape3.txt")


def delete_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)


def sort_the_files(verbose):
    if not os.path.exists("tape3.txt"):
        print("No input file provided. Generate data/enter yours/give me some!")
        return
    records_count = sum(1 if len(line.split(" ")) == 3 else 0 for line in open('tape3.txt'))
    phases, tape1, tape2, tape3 = natural_merging_sort(verbose)
    max_theoretical_phases = validation.calculate_max_theoretical_number_of_phases(records_count)
    avg_theoretical_phases = validation.calculate_avg_theoretical_number_of_phases(records_count)

    max_theoretical_io = validation.calculate_max_theoretical_number_of_reads_and_writes(records_count)
    avg_theoretical_io = validation.calculate_avg_theoretical_number_of_reads_and_writes(records_count)

    sum_of_io_operations = validation.calculate_io_stats(tape1, tape2, tape3)
    print(
        f"Disk IO stats.\nReads/writes: {sum_of_io_operations}, expected avg {avg_theoretical_io} and max {max_theoretical_io}")
    print(f"Sorted in {phases}. Expected avg {avg_theoretical_phases} and max {max_theoretical_phases}")


def run_the_program(verbose=0):
    b_quit_program = False
    while b_quit_program is False:
        display_menu()
        menu_option = choose_menu_option()
        match menu_option:
            case 0:
                data_generator.load_from_file(input("Enter filename to load data from: "))
            case 1:
                data_generator.generate_records(int(input("How many records to generate?")))
            case 2:
                data_generator.enter_records()
            case 3:
                sort_the_files(verbose)
            case 4:
                b_quit_program = True
                quit_program()
            case 5:  # Hidden option for debug
                validation.validate_io_operations_and_phases()
