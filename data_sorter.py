import data_generator


def display_menu():
    print("Hello and welcome to the Disk Sorter!")
    print("1. Automatically generate data")
    print("2. Enter the data manually")
    print("3. Sort the files")
    print("4. Quit")


def choose_menu_option():
    option_chosen = int(input("Please select menu option\n"))
    return option_chosen


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
                pass
            case 4:
                quit_program = True
