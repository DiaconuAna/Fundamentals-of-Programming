import unittest
from datetime import date

from domain.book import Book, BookValidator, BookValidationException
from domain.client import Client, ClientValidator, ClientValidationException
from domain.rental import Rental, RentalValidator, RentalValidationException


class TestDomain(unittest.TestCase):

    def test_book(self):
        book1 = Book('1345G', 'Good Omens', 'Neil Gaiman')
        book2 = Book('3442B', 'Baptism of Fire', 'Andrzej Sapkowski')
        self.assertEqual(book1.book_id, '1345G')
        self.assertEqual(book2.book_id, '3442B')
        self.assertEqual(book1.title, 'Good Omens')
        self.assertEqual(book2.title, 'Baptism of Fire')
        self.assertEqual(book1.author, 'Neil Gaiman')
        self.assertEqual(book2.author, 'Andrzej Sapkowski')
        book1.author = 'Terry Prattchet'
        book2.title = 'Lady of the Lake'
        self.assertEqual(book1.author, 'Terry Prattchet')
        self.assertEqual(book2.title, 'Lady of the Lake')

    def test_rental(self):

        r1 = Rental("1434", '2342A', 'F5432', date(2019, 2, 5), date(2019, 3, 4))
        self.assertEqual(r1.rental_id, '1434')
        self.assertEqual(r1.book_id, '2342A')
        self.assertEqual(r1.client_id, 'F5432')
        self.assertEqual(r1.rented_date, date(2019,2,5))
        self.assertEqual(r1.returned_date, date(2019,3,4))
        r1.book_id = '2341A'
        r1.client_id = 'F1034'
        self.assertEqual(r1.book_id, '2341A')
        self.assertEqual(r1.client_id, 'F1034')

    def test_client(self):
        client1 = Client('S1345', 'Sarah Klein')
        self.assertEqual(client1.client_id, 'S1345')
        self.assertEqual(client1.name, 'Sarah Klein')
        client1.client_id = 'S2345'
        self.assertEqual(client1.client_id, 'S2345')


    def test_string_book(self):
        book1 = Book('1345G', 'Good Omens', 'Neil Gaiman')
        print(book1)

    def test_string_client(self):
        client1 = Client('S1345', 'Sarah Klein')
        print(client1)

    def test_string_rental(self):
        book = Book('1045A','Anxious People','Fredrik Backman')
        client = Client("A3452",'Anna Park')
        rental = Rental("1434", '2342A', 'F5432', date(2019, 2, 5), date(2019, 3, 4))
        c = str(rental.print_rental(client, book))
        rental = Rental("1434", '2342A', 'F5432', date(2019, 2, 5), date(1,1,1))
        c = str(rental.print_rental(client, book))


class TestExceptions(unittest.TestCase):
    def test_book_validator(self):
        book_validator = BookValidationException(["Invalid name","Try again"])
        b = str(book_validator)

    def test_client_validator(self):
        client_validator = ClientValidationException(["Invalid name","Try again"])
        c = str(client_validator)

    def test_rental_validator(self):
        rental_validator = RentalValidationException(["Invalid rental","Try again!"])
        r = str(rental_validator)

if __name__ == '__main__':
     unittest.main()