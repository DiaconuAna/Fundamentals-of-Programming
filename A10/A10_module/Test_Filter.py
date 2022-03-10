import unittest

from A10_module.Filter import filter_function


class TestFilter(unittest.TestCase):
    def test_filter(self):
        self._list = ['Hello','Hola','Ciao','Annyeong','Ni Hao','Konnichiwa']
        self._filtered_list = filter_function(self._list, lambda x: 'h' in x.lower())
        for greeting in self._filtered_list:
            self.assertIn('h',greeting.lower())

