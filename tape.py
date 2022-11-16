from block import Block
from record import Record


class Tape:
    def __init__(self, filename):
        self._filename = filename
        self._read_lines_consumed = 0
        self._end_of_file = False
        self._write_lines_consumed = 0
        self._block = Block()
        self._write_operations = 0
        self._read_operations = 0

    def load_block(self):
        if self._end_of_file is True:
            self._block.clear()
            return
        with open(self._filename, "r") as file:
            line_len = int(len(file.readline()))
            file.seek(0)
            file.seek(self._read_lines_consumed * self._block.size * line_len)
            for idx, line in enumerate(file):
                if idx >= self._block.size:
                    break
                elements = line.split(" ")
                if len(elements) == 3:
                    self._block.data.append(Record(float(elements[0]), float(elements[1]), float(elements[2])))
                else:
                    self._end_of_file = True
                    break
        self._read_operations += 1
        self._read_lines_consumed += self._block.size

    def save_block(self):
        with open(self._filename, "a+") as file:
            line_len = int(len(file.readline()))
            file.seek(0)
            file.seek(self._write_lines_consumed * self._block.size * line_len)
            file.write(self._block.serialize())

        self._block.clear()
        self._write_operations += 1
        self._write_lines_consumed += self._block.size

    def add_record_to_block(self, record: Record):
        self._block.data.append(record)
        if self._block.is_full() is True:
            self.save_block()

    def get_record_from_block(self):
        if self._block.is_empty():
            self.load_block()
        record = self._block.get_first_element()
        return record

    def flush_block(self):
        self.save_block()
        self._write_lines_consumed = 0

    def flush_read(self):
        self._read_lines_consumed = 0
    def clear_file(self):
        open(self._filename, "w").close()