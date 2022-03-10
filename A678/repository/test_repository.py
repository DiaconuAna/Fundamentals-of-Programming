import unittest
from datetime import date

from domain.book import Book, BookValidationException
from domain.client import ClientException, Client, ClientValidationException
from domain.rental import Rental
from repository.book_repository import BookRepository
from repository.client_repository import ClientRepository
from repository.rental_repository import RentalRepository
from service.book_service import BookService
from service.client_service import ClientService
from service.rental_service import RentalService
from service.undo_service import UndoService


class BookRepoTest(unittest.TestCase):
    def setUp(self):
        book_repo = BookRepository()
        self._repo = book_repo
        rental_repo = RentalRepository()
        client_repo = ClientRepository()
        undo_service = UndoService()
        rental_service = RentalService(rental_repo, book_repo, client_repo, undo_service)
        self._service = BookService(book_repo, rental_service, undo_service)
        self._repo.add_book(Book("1234U", "Uprooted", "Naomi Novik"))
        self._repo.add_book(Book("1345G", "Good Omens", "Neil Gaiman"))

    def test_add_book(self):
        book = self._repo.get_last_book()
        self.assertEqual(len(self._repo), 2)
        self.assertEqual(book.book_id, "1345G")
        self.assertEqual(book.title, "Good Omens")
        self.assertEqual(book.author, "Neil Gaiman")

    def test_remove_book(self):
        # remove the 2nd book based on its id
        self._service.remove_book("1345G")
        book = self._repo.get_last_book()
        self.assertEqual(book.book_id, "1234U")
        self.assertEqual(book.title, "Uprooted")
        self.assertEqual(book.author, "Naomi Novik")
        self._repo.add_book(Book("5456S", "Serpent&Dove", "Shelby Mahurin"))
        # remove the last book based on its title
        self._service.remove_book("Serpent&Dove")
        book = self._repo.get_last_book()
        self.assertEqual(book.book_id, "1234U")
        self.assertEqual(book.title, "Uprooted")
        self.assertEqual(book.author, "Naomi Novik")

    def test_update_book(self):
        """
        Possible errors raised:
        -> BookException: there is no book with the given attributes in the list
        -> BookValidationException: new book_id, title or author are invalid
        :return:
        """
        self._repo.add_book(Book("3456B", "Baptism Of Fire", "Andrzej Sapkowski"))
        # update 2nd book on the list by changing its title
        self._service.update_book("Baptism of Fire", "Tower of the Swallow", '2')
        book = self._repo.get_last_book()
        self.assertEqual(book.book_id, "3456T")
        self.assertEqual(book.title, "Tower of the Swallow")
        self.assertEqual(book.author, "Andrzej Sapkowski")
        # update 2nd book on the list by changing its id- valid id
        self._service.update_book("3456T", "4567T", '1')
        book = self._repo.get_last_book()
        self.assertEqual(book.book_id, "4567T")
        self.assertEqual(book.title, "Tower of the Swallow")
        self.assertEqual(book.author, "Andrzej Sapkowski")
        # update 2nd book on the list by changing the author
        self._service.update_book("Tower of the Swallow", "Andrew Mill", '3')
        book = self._repo.get_last_book()
        self.assertEqual(book.book_id, "4567T")
        self.assertEqual(book.title, "Tower of the Swallow")
        self.assertEqual(book.author, "Andrew Mill")

        # try to update the last book by giving an invalid id
        self.assertRaises(BookValidationException, self._service.update_book,"Tower of the Swallow", "3456G", "1")


    def test_list_books(self):
        print_list = []
        self._repo.list_books(print_list)
        self.assertEqual(len(self._repo), len(print_list))

    def tearDown(self):
        print("----")


class RentalRepoTest(unittest.TestCase):
    def setUp(self):
        rental_repo = RentalRepository()
        book_repo = BookRepository()
        client_repo = ClientRepository()
        undo_service = UndoService()
        self._repo = rental_repo
        self._service = RentalService(rental_repo, book_repo, client_repo, undo_service)
        self._service.create_rental('5641', '3451H', 'A5641', date(2020, 10, 15), date(1, 1, 1))
        self._service.create_rental('5642', '3452A', 'S5642', date(2020, 10, 10), date(1, 1, 1))

    def test_add_rental(self):
        """
        A rental consists of a rental_id, book_id, client_id, rented_date, returned_date which is 1,1,1 as the book
            has just been rented, not returned
            Raises RentalException if:
               -> book_id is already in the list and its rental hasn't been closed <=> the book has already been rented and hasn't been returned yet
               -> two rentals have the same id
        :return:
        """
        r1 = self._repo.get_last_rental()
        self.assertEqual(len(self._repo), 2)
        self.assertEqual(r1.rental_id,'5642')
        self.assertEqual(r1.client_id, 'S5642')
        self.assertEqual(r1.book_id, '3452A' )
        self.assertEqual(r1.rented_date, date(2020,10,10))
        self.assertEqual(r1.returned_date, date(1,1,1))

    def test_close_rental(self):
        """
        We say a rental is closed if the rented book has been returned
            The rental is identified by its rental_id
            Raises RentalException if:
            -> rental does not exist
            -> returned date is incorrect (RentalValidateException here)
        :return:
        """

        self._service.close_rental('5642', date(2020, 10, 12))
        r1 = self._repo.get_last_rental()
        self.assertEqual(r1.returned_date, date(2020,10,12))

    def test_list_rental(self):
        print_list = []
        self._repo.list_rentals(print_list)
        self.assertEqual(len(print_list), len(self._repo))


    def test_open_rental(self):
        self._service.close_rental('5641', date(2020, 10, 22))
        rental = Rental('5641', '3451H', 'A5641', date(2020, 10, 15), date(2020, 10, 22))
        self._repo.open_rental(rental)


    def tearDown(self):
        print("-----")


class ClientRepoTest(unittest.TestCase):
    def setUp(self):
        client_repo = ClientRepository()
        undo_service = UndoService()
        book_repo = BookRepository()
        rental_repo = RentalRepository()
        rental_service = RentalService(rental_repo, book_repo, client_repo, undo_service)
        self._repo = client_repo
        self._service = ClientService(client_repo, rental_service, undo_service)
        self._service.add_client("S4531", "Sarah Kays")

    def test_add_client(self):
        self.assertEqual(len(self._repo), 1)
        client = self._repo.get_last_client()
        self.assertEqual(client.client_id, 'S4531')
        self.assertEqual(client.name, 'Sarah Kays')

    def test_remove_client(self):
        self._repo.add_client(Client("F4531", "Finn McMissile"))
        self.assertEqual(len(self._repo), 2)
        self._service.remove_client("F4531")
        client = self._repo.get_last_client()
        self.assertEqual(client.client_id, 'S4531')
        self.assertEqual(client.name, 'Sarah Kays')
        self.assertEqual(len(self._repo), 1)

    def test_update_client(self):
        """
        Possible errors raised:
        -> ClientException: there is no client with the given attributes in the list
        -> ClientValidationException: new client_id or name are invalid
        :return:
        """
        self._repo.add_client(Client("F4531", "Finn McMissile"))
        self._service.update_client("Finn McMissile", "Tow Mater", '2')
        client = self._repo.get_last_client()
        self.assertEqual(client.client_id, 'T4531')
        self.assertEqual(client.name, 'Tow Mater')
        self._service.update_client("T4531", "T6001", '1')
        client = self._repo.get_last_client()
        self.assertEqual(client.client_id, 'T6001')
        self.assertEqual(client.name, 'Tow Mater')
        # try to update a client by giving an invalid id
        self.assertRaises(ClientValidationException, self._service.update_client, "T6001", "A7531", '1')
        # try to update a client that's not in the list
        self.assertRaises(ClientException, self._service.update_client, "Angel", 'A5432', '1')

    def test_list_clients(self):
        print_list = []
        self._repo.list(print_list)
        self.assertEqual(len(self._repo), len(print_list))


class Generate_Test(unittest.TestCase):
    def test_generate_books(self):
        self._repo = BookRepository()
        self._repo.generate_list(10)
        book_list = self._repo.books
        self.assertEqual(len(book_list), 10)
        self._repo.generate_list(1000)

    def test_generate_clients(self):
        self._repo = ClientRepository()
        self._repo.generate_list(10)
        client_list = self._repo.clients
        self.assertEqual(len(client_list), 10)
        self._repo.generate_list(1000)

    def test_generate_rentals(self):
        self._repo = RentalRepository()
        client_list = ClientRepository()
        client_list.generate_list(10)
        book_list = BookRepository()
        book_list.generate_list(10)
        self._repo.generate_rentals(client_list, book_list)
        self.assertEqual(len(self._repo), 10)
        for i in range(10):
            self._repo.generate_rentals(client_list, book_list)


if __name__ == '__main__':
     unittest.main()