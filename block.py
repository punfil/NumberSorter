class Block:
    def __init__(self, size=4):
        self._size = size
        self._data = [None for _ in range(size)]

    def get_record_from_block(self, index):
        assert (index >= 0)
        assert (index < len(self._data))
        return self._data[index]

    def serialize(self):
        returning = ""
        for record in self._data:
            if record is not None:
                returning += record.serialize()
            else:
                returning += "None\n"  # IDK if that's ok, probably not
        return returning

    def clear(self):
        self._data = [None for _ in range(self._size)]

    @property
    def data(self):
        return self._data

    @property
    def size(self):
        return self._size
