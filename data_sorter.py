import data_generator
import os
from tape import Tape
from validation import validate


def display_menu():
    print("Hello and welcome to the Disk Sorter!")
    print("1. Automatically generate data")
    print("2. Enter the data manually")
    print("3. Sort the files")
    print("4. Quit")


def choose_menu_option():
    option_chosen = int(input("Please select menu option\n"))
    return option_chosen


def distribution(input_tape):
    tape1 = Tape("tape1.txt")
    tape2 = Tape("tape2.txt")
    tape1.clear_file()
    tape2.clear_file()
    current_tape = tape1
    current_record = None
    switched_tapes = False
    # Load data from the input tape
    while True:
        last_record = current_record
        current_record = input_tape.get_record_from_block()
        if current_record is None:
            break
        if last_record is not None and current_record < last_record:
            switched_tapes = True
            if current_tape == tape1:
                current_tape = tape2
            else:
                current_tape = tape1
        current_tape.add_record_to_block(current_record)
    tape1.flush_write()
    tape2.flush_write()
    input_tape.flush_read()
    return tape1, tape2, switched_tapes


def natural_merging_sort():  # 2+1 edition
    input_tape = Tape("data.txt")
    tape1, tape2, switched_tapes = distribution(input_tape)

    if switched_tapes is False:
        print("Whole list already sorted on input!")
        # TODO: Rewrite the whole list from input to output
        return
    tape3 = Tape("tape3.txt")
    tape3.clear_file()
    phase_count = 0
    while switched_tapes is True:
        last_tape1, curr_tape1, end_of_series_tape1 = tape1.fetch_new_record(None)
        last_tape2, curr_tape2, end_of_series_tape2 = tape2.fetch_new_record(None)
        go_inside = True
        while tape1.end_of_file is False and tape2.end_of_file is False or go_inside is True:
            go_inside = False
            while end_of_series_tape1 is False and end_of_series_tape2 is False:
                while end_of_series_tape1 is False and curr_tape1 <= curr_tape2:
                    tape3.add_record_to_block(curr_tape1)
                    last_tape1, curr_tape1, end_of_series_tape1 = tape1.fetch_new_record(curr_tape1)
                while end_of_series_tape1 is False and end_of_series_tape2 is False and curr_tape1 > curr_tape2:
                    tape3.add_record_to_block(curr_tape2)
                    last_tape2, curr_tape2, end_of_series_tape2 = tape2.fetch_new_record(curr_tape2)
            while end_of_series_tape1 is False:
                tape3.add_record_to_block(curr_tape1)
                last_tape1, curr_tape1, end_of_series_tape1 = tape1.fetch_new_record(curr_tape1)
            while end_of_series_tape2 is False:
                tape3.add_record_to_block(curr_tape2)
                last_tape2, curr_tape2, end_of_series_tape2 = tape2.fetch_new_record(curr_tape2)
            end_of_series_tape1 = False
            end_of_series_tape2 = False
            if tape1.end_of_file is True and tape2.end_of_file is True and curr_tape1 is not None and curr_tape2 is not None:
                go_inside = True
        while curr_tape1 is not None:
            tape3.add_record_to_block(curr_tape1)
            last_tape1, curr_tape1, end_of_series_tape1 = tape1.fetch_new_record(curr_tape1)
        while curr_tape2 is not None:
            tape3.add_record_to_block(curr_tape2)
            last_tape2, curr_tape2, end_of_series_tape2 = tape2.fetch_new_record(curr_tape2)
        tape1.flush_read()
        tape2.flush_read()
        tape1.clear_file()
        tape2.clear_file()
        tape3.flush_write()
        tape1, tape2, switched_tapes = distribution(tape3)
        if switched_tapes is not False:
            tape3.clear_file()
        phase_count += 1
    return phase_count - 1


def quit_program():
    delete_file("tape1.txt")
    delete_file("tape2.txt")


def delete_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)


def run_the_program():
    b_quit_program = False
    while b_quit_program is False:
        display_menu()
        menu_option = choose_menu_option()
        match menu_option:
            case 1:
                data_generator.generate_records()
            case 2:
                data_generator.enter_records()
            case 3:
                natural_merging_sort()
            case 4:
                b_quit_program = True
                quit_program()
            case 5:
                data_generator.generate_fake_records()
            case 6:
                validate(int(input("How many tests do you want to run?")))
