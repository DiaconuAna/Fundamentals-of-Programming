import unittest
from datetime import date

from domain.book import Book, BookException, BookValidationException
from domain.client import Client, ClientValidationException, ClientException
from domain.rental import RentalException, RentalValidationException
from repository.book_repository import BookRepository
from repository.client_repository import ClientRepository
from repository.rental_repository import RentalRepository
from service.book_service import BookService
from service.client_service import ClientService
from service.rental_service import RentalService, BookRental, ClientRental, AuthorRental11
from service.undo_service import UndoService, Operation, FunctionCall


class BookServiceTest(unittest.TestCase):
    def setUp(self):
        book_repo = BookRepository()
        rental_repo = RentalRepository()
        client_repo = ClientRepository()
        undo_service = UndoService()
        rental_service = RentalService(rental_repo, book_repo, client_repo, undo_service)
        rental_service.create_rental('5641', '1234U', 'A5641', date(2020, 10, 15), date(1, 1, 1))
        rental_service.create_rental('5642', '1345G', 'S5642', date(2020, 10, 10), date(1, 1, 1))

        self._service = BookService(book_repo, rental_service, undo_service)
        self._service.add_book("1234U", "Uprooted", "Naomi Novik")
        self._service.add_book("1345G", "Good Omens", "Neil Gaiman")


    def test_add_book(self):
        self.assertEqual(len(self._service), 2)
        self.assertRaises(BookException, self._service.add_book,"1345G", "A Sorcery of Thorns", "Anna Bey")
        self.assertRaises(BookValidationException, self._service.add_book,"1347C", "A Sorcery of Thorns", "")
        # try to add a book with an empty title
        self.assertRaises(BookValidationException, self._service.add_book, "1345G", "", "Anna Bey")
        # try to add an invalid author name
        self.assertRaises(BookValidationException, self._service.add_book, "1345G", "A Sorcery of Thorns", "A9nna Bey")
        #try to add a book with an existent id
        self.assertRaises(BookException, self._service.add_book, "1345G", "Ga Sorcery of Thorns", "Anna Bey")
        #try to add a book with an invalid id
        self.assertRaises(BookException, self._service.add_book,"13454", "A Sorcery of Thorns", "Anna Bey")

    def test_remove_book(self):
        # remove the 2nd book based on its id
        self._service.remove_book("1345G")
        # try to remove a book based on invalid data
        self.assertRaises(BookException,self._service.remove_book,"5653J")

    def test_update_book(self):
        """
        Possible errors raised:
        -> BookException: there is no book with the given attributes in the list
        -> BookValidationException: new book_id, title or author are invalid
        :return:
        """
        # try to update a book whose given data is not in the list/// input invalid update data
        self.assertRaises(BookException, self._service.update_book,"4521T", "Test", '1')
        self._service.update_book('1345G','1346G','1')

    def test_list_books(self):
        print_list = []
        self._service.list_books(print_list)

    def test_generate_list(self):
        self._service.generate_list(10)

    def test_get_list(self):
        self._service.get_list()

    def test_get_book(self):
        #try to get a book with invalid data
        self.assertRaises(BookException, self._service.get_book, '1344A')
        self._service.get_book("1234U")

    def test_search_book(self):
        search_list = []
        #try to search a book by giving invalid data
        self.assertRaises(BookException, self._service.search_book, "1235A",search_list)
        self._service.search_by_id("1234U", search_list)
        self._service.search_by_author("Naomi Novik", search_list)
        self._service.search_by_title("Uprooted", search_list)


    def tearDown(self):
        print("----")


class ClientServiceTest(unittest.TestCase):
    def setUp(self):
        client_repo = ClientRepository()
        book_repo = BookRepository()
        rental_repo = RentalRepository()
        undo_service = UndoService()
        rental_service = RentalService(rental_repo, book_repo, client_repo, undo_service)
        rental_service.create_rental('5641', '1234U', 'A5641', date(2020, 10, 15), date(1, 1, 1))
        rental_service.create_rental('5642', '1345G', 'S4531', date(2020, 10, 10), date(1, 1, 1))
        self._service = ClientService(client_repo, rental_service, undo_service)
        self._service.add_client("S4531", "Sarah Kays")

    def test_add_client(self):
        self.assertEqual(len(self._service.client_repo), 1)

        # try to add a client with invalid attributes
        self.assertRaises(ClientValidationException, self._service.add_client, "A4532", " ")

        # try to add a client whose id is already in the list
        self.assertRaises(ClientException, self._service.add_client, "S4531", "Sasha Sloan")

        #try to add a client with an invalid name
        self.assertRaises(ClientException, self._service.add_client, "S4531", "Sas6ha Sloan")

        #try to add a client with an empty name
        self.assertRaises(ClientValidationException, self._service.add_client, "S4931", " ")


    def test_remove_client(self):
        # try to remove a client that's not in the list
        self.assertRaises(ClientException, self._service.remove_client, 'D5432')
        self._service.remove_client('S4531')

    def test_update_client(self):
        """
        Possible errors raised:
        -> ClientException: there is no client with the given attributes in the list
        -> ClientValidationException: new client_id or name are invalid
        :return:
        """
        # try to update a client that's not in the list
        self.assertRaises(ClientException, self._service.update_client, "Angel", 'A5432', '1')
        self._service.update_client('S4531','S2314','1')

    def test_list_clients(self):
        print_list = []
        self._service.list_clients(print_list)

    def test_generate_list(self):
        self._service.generate_list(10)

    def test_get_list(self):
        self._service.get_list()

    def test_get_client(self):
        #try to get a client with invalid data
        self.assertRaises(ClientException, self._service.get_client, "Hello")
        self._service.get_client("S4531")

    def test_search_client(self):
        search_list = []
        #try to search with invalid data
        self.assertRaises(ClientException, self._service.search_client, "Hello", search_list)
        self._service.search_by_id("S4531",search_list)
        self._service.search_by_name("Sarah Kays", search_list)



class RentalServiceTest(unittest.TestCase):
    def setUp(self):
        rental_repo = RentalRepository()
        book_repo = BookRepository()
        client_repo = ClientRepository()
        undo_service = UndoService()
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
        # add new rental with the same id
        self.assertRaises(RentalException, self._service.create_rental, '5642', '2342A', 'A3542', date(10, 10, 10), date(1, 1, 1))

        # try to rent a book that's already been rented, but not returned
        self.assertRaises(RentalException, self._service.create_rental, "4532", '3452A', 'A4532', date(10, 10, 10), date(1, 1, 1))

        #try to return a book at an invalid date
        self.assertRaises(RentalValidationException, self._service.create_rental, "4532", '3452A', 'A4532', date(10, 10, 10), date(10, 9, 1))
        self.assertRaises(RentalValidationException, self._service.create_rental, "4532", '3452A', 'A4532', date(10, 10, 10), date(9, 9, 1))

        # try to create a rental with an invalid id
        self.assertRaises(RentalValidationException, self._service.create_rental, "452", '3452A', 'A4532', date(10, 10, 10), date(10, 9, 1))

    def test_close_rental(self):
        """
        We say a rental is closed if the rented book has been returned
            The rental is identified by its rental_id
            Raises RentalException if:
            -> rental does not exist
            -> returned date is incorrect (RentalValidateException here)
        :return:
        """

        # try to close a rental that does not exist
        self.assertRaises(RentalException, self._service.close_rental,'4532', date(10, 10, 10))
        # try to close a rental with an incorrect return date
        self.assertRaises(RentalValidationException, self._service.close_rental, '5642', date(2020, 10, 7))

    def test_delete_rental(self):
        #try to delete an inexistent rental
        self.assertRaises(RentalException, self._service.delete_rental,'1024')
        self._service.delete_rental('5641')

    def test_update_rental(self):
        #try to update an inexistent rental
        self.assertRaises(RentalException, self._service.update_rental,'1035', 'S1020','2')

    def test_list_rental(self):
        print_list = []
        self._service.list_rentals(print_list)

    def test_generate_rental(self):
        self._service._book_list.generate_list(10)
        self._service._client_list.generate_list(10)
        self._service.generate_list()

    def test_most_rented_books(self):
        self._service.close_rental('5641',date(2020,11,10))
        self._service.create_rental('5643', '3451H', 'A5641', date(2020, 11, 15), date(1, 1, 1))
        self._service.close_rental('5643',date(2020,11,30))
        self._service.create_rental('5644', '3451H', 'S5642', date(2020, 12, 10), date(1, 1, 1))
        book1 = Book('3451H','Hello','Me')
        book2 = Book('3452A','Ayy','Mee')
        book_list = [book1, book2]
        self._service.most_rented_books(book_list)


    def test_most_active_clients(self):
        self._service.close_rental('5641', date(2020, 11, 10))
        self._service.create_rental('5643', '3451H', 'A5641', date(2020, 11, 15), date(1, 1, 1))
        self._service.close_rental('5643', date(2020, 11, 30))
        self._service.create_rental('5644', '3451H', 'S5642', date(2020, 12, 10), date(1, 1, 1))
        client1 = Client('A5641','Anna')
        client2 = Client("S5642",'Sarah')
        client_list = [client1, client2]
        self._service.most_active_clients(client_list)

    def test_most_rented_authors(self):
        self._service.close_rental('5641', date(2020, 11, 10))
        self._service.create_rental('5643', '3451H', 'A5641', date(2020, 11, 15), date(1, 1, 1))
        self._service.close_rental('5643', date(2020, 11, 30))
        self._service.create_rental('5644', '3451H', 'S5642', date(2020, 12, 10), date(1, 1, 1))
        book1 = Book('3451H', 'Hello', 'Me')
        book2 = Book('3452A', 'Ayy', 'Mee')
        book_list = [book1, book2]
        self._service.most_rented_authors1(book_list)

    def test_class_book_rental(self):
        b1 = BookRental('1001A', 'Anxious People', 'Fredrik Backman', 7)
        self.assertEqual(b1.book_id, '1001A')
        self.assertEqual(b1.rental_times, 7)
        b = str(b1)

    def test_class_client_rental(self):
        c1 = ClientRental('A2000', 'Anna Park', 234)
        self.assertEqual(c1._client_id, 'A2000')
        c = str(c1)

    def test_class_author_rental(self):
        a1 = AuthorRental11("Fredrik Backman",13)
        self.assertEqual(a1.author, 'Fredrik Backman')
        self.assertEqual(a1.rental_times, 13)
        a = str(a1)

    def tearDown(self):
        print("-----")

class UndoServiceTest(unittest.TestCase):

    def test_undo_simple(self):
        client_repo = ClientRepository()
        book_repo = BookRepository()
        rental_repo = RentalRepository()
        undo_service = UndoService()
        rental_service = RentalService(rental_repo, book_repo, client_repo, undo_service)
        rental_service.create_rental('5641', '1234U', 'A5641', date(2020, 10, 15), date(1, 1, 1))
        rental_service.create_rental('5642', '1345G', 'S4531', date(2020, 10, 10), date(1, 1, 1))
        self._undo = undo_service
        self._service = ClientService(client_repo, rental_service, undo_service)
        self._service.add_client("A4952",'Anna Park')
        self._undo.undo()
        self._undo.redo()
        self.assertRaises(ValueError, self._undo.redo)
        self._undo.undo()
        self._undo.undo()
        self._undo.undo()
        self.assertRaises(ValueError, self._undo.undo)

    def test_undo_cascaded(self):
        client_repo = ClientRepository()
        book_repo = BookRepository()
        rental_repo = RentalRepository()
        undo_service = UndoService()
        rental_service = RentalService(rental_repo, book_repo, client_repo, undo_service)
        rental_service.create_rental('5641', '1234U', 'A4952', date(2020, 10, 15), date(1, 1, 1))
        rental_service.create_rental('5642', '1345G', 'S4531', date(2020, 10, 10), date(1, 1, 1))
        self._undo = undo_service
        self._service = ClientService(client_repo, rental_service, undo_service)
        self._service.add_client("A4952",'Anna Park')
        self._service.remove_client('A4952')
        self._undo.undo()
        self._undo.redo()
        self.assertRaises(ValueError, self._undo.redo)

    def test_more_undo(self):
        client_repo = ClientRepository()
        book_repo = BookRepository()
        rental_repo = RentalRepository()
        undo_service = UndoService()
        rental_service = RentalService(rental_repo, book_repo, client_repo, undo_service)
        rental_service.create_rental('5641', '1234U', 'A4952', date(2020, 10, 15), date(1, 1, 1))
        rental_service.create_rental('5642', '1345G', 'S4531', date(2020, 10, 10), date(1, 1, 1))
        self._undo = undo_service  #undo has 3 operations in history
        self._service = ClientService(client_repo, rental_service, undo_service)
        self._service.add_client('A4952','Anna') #4 operations in undo history
        self._undo.undo() #undoing first operation
        self._service.add_client('A4953', 'Anna')
        #self._service.remove_client('A4953')
        self._undo.undo()
        self._undo.undo()
        self._service.add_client('A4953', 'Anna')

if __name__ == '__main__':
     unittest.main()