import unittest
from A10_module.Gnome_Sort import gnome_sort


class TestGnomeSort(unittest.TestCase):
    def test_sort(self):
        self._list = [3, 7, -1, 5]
        gnome_sort(self._list, lambda x, y: x < y)
        for index in range(len(self._list)-1):
            self.assertLessEqual(self._list[index], self._list[index+1])



