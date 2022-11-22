import constants
from block import Block
from record import Record, DebugRecord
import os


class Tape:
    def __init__(self, filename):
        self._filename = filename
        self._end_of_file = False
        self._block = Block()
        self._write_operations = 0
        self._read_operations = 0
        self._read_location_in_file = None
        self._write_location_in_file = None

    def load_block(self):
        if self._end_of_file is True:
            self._block.clear()
            return
        with open(self._filename, "r") as file:
            lines_consumed = 0
            size_of_file = os.path.getsize(self._filename)
            line_len = len(file.readline()) # Not good if we load 1.0 it will be shorter
            file.seek(0)
            if self._read_location_in_file is not None:
                if size_of_file - self._read_location_in_file <= constants.size_of_block * (line_len+1):
                    self._end_of_file = True
                file.seek(self._read_location_in_file)
            elif size_of_file <= constants.size_of_block * line_len:
                self._end_of_file = True
            line = file.readline()
            while line is not None:
                elements = line.split(" ")
                self._read_location_in_file = file.tell()
                if len(elements) == 3:
                    self._block.data.append(DebugRecord(float(elements[0]), float(elements[1]), float(elements[2])))
                else:
                    break
                if lines_consumed == self._block.size - 1:
                    break
                lines_consumed += 1
                line = file.readline()
        self._read_operations += 1

    def save_block(self):
        with open(self._filename, "a+") as file:
            if self._write_location_in_file is not None:
                file.seek(self._write_location_in_file)
            file.write(self._block.serialize())
            self._write_location_in_file = file.tell()

        if not self._block.is_empty():
            self._write_operations += 1
        self._block.clear()

    def add_record_to_block(self, record):
        self._block.data.append(record)
        if self._block.is_full() is True:
            self.save_block()

    def get_record_from_block(self):
        if self._block.is_empty():
            if self._end_of_file:
                return None
            self.load_block()
        record = self._block.get_first_element()
        return record

    def flush_write(self):
        self.save_block()
        self._write_location_in_file = None

    def flush_read(self):
        self._read_location_in_file = None
        self._end_of_file = False

    def fetch_new_record(self, last_record):
        end_of_series = False
        new_record = self.get_record_from_block()
        if new_record is None:
            end_of_series = True
        elif last_record is None:
            return None, new_record, end_of_series
        elif new_record < last_record:
            end_of_series = True
        return last_record, new_record, end_of_series

    def clear_file(self):
        open(self._filename, "w").close()

    def print_disk_io_stats(self):
        print(f"Tape {self._filename} disk IO stats:")
        print(f"Reads: {self._read_operations}, writes: {self._write_operations}")

    def print_content(self):
        save_reads = self._read_operations
        curr_tape = self.get_record_from_block()
        print(f"Printing content of tape: {self.filename}")
        while curr_tape is not None:
            print(curr_tape.serialize(), end="")
            curr_tape = self.get_record_from_block()
        self.flush_read()
        self._read_operations = save_reads

    @property
    def read_operations(self):
        return self._read_operations

    @property
    def write_operations(self):
        return self._write_operations

    @property
    def end_of_file(self):
        return self._end_of_file

    @property
    def filename(self):
        return self._filename
