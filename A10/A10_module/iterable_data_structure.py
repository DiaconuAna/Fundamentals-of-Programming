class IterableStructure:
    def __init__(self):
        self._list = []
        self._index = 0

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        #print(self._index, len(self._list))
        if self._index >= len(self._list):
            raise StopIteration
        self._index += 1
        return self._list[self._index - 1]

    def __len__(self):
        return len(self._list)

    def __setitem__(self, index, value):
        if index == -1 or index >= len(self._list):
            raise ValueError("Object index does not exist.")
        self._list[index] = value

    def __getitem__(self, index):
        if index == -1 or index >= len(self._list):
            raise ValueError("Object index does not exist.")
        return self._list[index]

    def set(self, index, value):
        self.__setitem__(index, value)

    def get(self, index):
        item = self.__getitem__(index)
        return item

    def __delitem__(self, index):
        if index == -1 or index >= len(self._list):
            raise ValueError("Object index does not exist.")
        del self._list[index]

    def delete_item(self, index):
        self.__delitem__(index)

    def add_element(self, element):
        self._list.append(element)
        #self._index += 1

    def set_index_zero(self):
        self._index = 0

    """
    def print_list(self):
        i_list = iter(self._list)
        while True:
            try:
                item = next(i_list)
                print(item)
            except StopIteration:
                break
    """

