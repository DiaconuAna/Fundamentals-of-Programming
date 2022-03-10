import unittest

from A10_module.iterable_data_structure import IterableStructure


class TestIterable(unittest.TestCase):
    def setUp(self):
        it = IterableStructure()
        self._it = it
        self._it.add_element('1')
        self._it.add_element('2')
        self._it.add_element('hello')

    def test_methods(self):
        #self._it.__delitem__(2)
        self._it.delete_item(2)
        self._it.set(1,'heyy')
        #self._it.__setitem__(1,'4')
        self._it.get(0)
        #self._it.__getitem__(0)
        it_list = iter(self._it)
        next(it_list)
        next(it_list)
        self.assertRaises(StopIteration, next, it_list)
        self._it.set_index_zero()
        next(it_list)
        len(self._it)
        self.assertRaises(ValueError, self._it.__setitem__, 4, 5)
        self.assertRaises(ValueError, self._it.__getitem__, 5)
        self.assertRaises(ValueError, self._it.__delitem__, 5)
        it1 = iter(self._it)
        while True:
            try:
                item = next(it1)
            except StopIteration:
                break
