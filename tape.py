from block import Block
from record import Record


class Tape:
    def __init__(self, tape_id):
        self._tape_id = tape_id
        self._filename = "tape" + str(tape_id)
        self._read_lines_consumed = 0
        self._write_lines_consumed = 0
        self._block = Block()

    def load_block(self):
        with open(self._filename, "r'") as file:
            line_len = file.readline()
            file.seek(0)
            file.seek(self._read_lines_consumed * self._block.size * line_len)
            for idx, line in enumerate(file):
                if idx >= self._block.size:
                    break
                elements = line.split(" ")
                self._block.data[idx] = Record(elements[0], elements[1], elements[2])

        self._read_lines_consumed += self._block.size

    def save_block(self):
        with open(self._filename, "w") as file:
            line_len = file.readline()
            file.seek(0)
            file.seek(self._write_lines_consumed * self._block.size * line_len)
            file.write(self._block.serialize())
            self._block.clear()

        self._write_lines_consumed += self._block.size
