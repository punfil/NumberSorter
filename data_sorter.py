import data_generator
import os
from tape import Tape


def display_menu():
    print("Hello and welcome to the Disk Sorter!")
    print("1. Automatically generate data")
    print("2. Enter the data manually")
    print("3. Sort the files")
    print("4. Quit")


def choose_menu_option():
    option_chosen = int(input("Please select menu option\n"))
    return option_chosen


def natural_merging_sort():  # 2+1 edition
    input_tape = Tape("data.txt")
    tape1 = Tape("tape1.txt")
    tape2 = Tape("tape2.txt")
    tape3 = Tape("tape3.txt")
    current_tape = tape1
    current_record = None
    last_record = None
    # Load data from the input tape
    while True:
        last_record = current_record
        current_record = input_tape.get_record_from_block()
        if current_record is None:
            break
        if last_record is not None and current_record > current_record:
            if current_tape == tape1:
                current_tape = tape2
            else:
                current_tape = tape1
        current_tape.add_record_to_block(current_record)
    tape1.flush_block()
    tape2.flush_block()
    pass


def quit_program():
    delete_file("tape1.txt")
    delete_file("tape2.txt")
    delete_file("tape3.txt")


def delete_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)


def run_the_program():
    quit_program = False
    while quit_program is False:
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
                quit_program = True
                quit_program()
