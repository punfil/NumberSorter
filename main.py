import data_sorter
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usage of the program",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true", help="Run with increased verbosity")
    args = vars(parser.parse_args())
    if args['verbose'] == 1:
        data_sorter.run_the_program(verbose=1)
    else:
        data_sorter.run_the_program(verbose=0)
