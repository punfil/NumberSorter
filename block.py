class Block:
    def __init__(self, size=4):
        self._size = size
        self._data = []

    def is_full(self):
        return len(self._data) == self._size

    def is_empty(self):
        return len(self._data) == 0

    def get_first_element(self):
        if self.is_empty() is False:
            return self._data.pop(0)
        return None

    def serialize(self):
        returning = ""
        for record in self._data:
            returning += record.serialize()
        return returning

    def clear(self):
        self._data = []

    @property
    def data(self):
        return self._data

    @property
    def size(self):
        return self._size
