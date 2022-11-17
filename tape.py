from block import Block
from record import Record
from record import DebugRecord

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
            if self._read_location_in_file is not None:
                file.seek(self._read_location_in_file)
            lines_consumed = 0
            line = file.readline()
            while line is not None:
                line_len = int(len(line))
                lines_consumed += 1
                elements = line.split(" ")
                if len(elements) == 3:
                    self._block.data.append(DebugRecord(float(elements[0]), float(elements[1]), float(elements[2])))
                else:
                    self._end_of_file = True
                    self._read_location_in_file = file.tell()
                    break
                if lines_consumed == self._block.size-1:
                    break
                line = file.readline()
            self._read_location_in_file = file.tell()
        self._read_operations += 1

    def save_block(self):
        with open(self._filename, "a+") as file:
            if self._write_location_in_file is not None:
                file.seek(self._write_location_in_file)
            file.write(self._block.serialize())
            self._write_location_in_file = file.tell()

        self._block.clear()
        self._write_operations += 1

    def add_record_to_block(self, record):
        self._block.data.append(record)
        if self._block.is_full() is True:
            self.save_block()

    def get_record_from_block(self):
        if self._block.is_empty():
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

    @property
    def end_of_file(self):
        return self._end_of_file
