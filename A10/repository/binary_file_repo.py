import pickle
from datetime import date

from domain.book import Book
from domain.client import Client
from domain.rental import Rental
from repository.big_repo import BookRepository, ClientRepository, RentalRepository


class BookBinaryRepository(BookRepository):
    def __init__(self, file_name):
        BookRepository.__init__(self)
        self._file_name = file_name
        #self._initialise_file()
        self._read_binary_file()

    def _initialise_file(self):
        """
        Initialising a binary file
        :return:
        """
        books = [Book("1234C","Chanel's Riviera","Anne de Courcy"),Book("1235A","All the Flowers in Paris","Sarah Jio"),
                 Book("2031L","Liberation","Imogen Kealey"), Book("1357M","My Heart and Other Black Holes","Jasmine Warga"),
                 Book("1353A","Anxious People","Fredrik Backman"), Book("2456T","The Secret Messenger","Mandy Robotham"),
                 Book("2367T","The Year After You","Nina de Pass"), Book("1356H","Harry Potter and the Prisoner of Azkaban","J.K.Rowling"),
                 Book("2469H","Harry Potter and the Goblet of Fire","J.K.Rowling"),
                 Book("2939B","Baptism of Fire","Andrzej Sapkowski"), Book("3495G","Good Omens","Neil Gaiman"), Book("5040S","Sword of Destiny","Andrzej Sapkowski")]

        try:
            f = open(self._file_name, "wb")
            pickle.dump(books, f)
            f.close()
        except (EOFError,IOError):
            raise ValueError("Invalid file content.")

    def _read_binary_file(self):
        f = open(self._file_name,'rb')
        books = pickle.load(f)
        for b in books:
            BookRepository.add_book(self, b)

    def add_book(self, book):
        BookRepository.add_book(self, book)
        self._write_to_file()

    def remove_book(self, book):
        BookRepository.remove_book(self, book)
        self._write_to_file()

    def list_books(self, print_list):
        BookRepository.list_books(self, print_list)

    def update_book(self, book, update_info, update_id):
        BookRepository.update_book(self, book, update_info, update_id)
        self._write_to_file()

    def _write_to_file(self):
        f = open(self._file_name, 'bw')
        pickle.dump(self._book_list, f)
        f.close()


class ClientBinaryRepository(ClientRepository):
    def __init__(self, file_name):
        ClientRepository.__init__(self)
        self._file_name = file_name
        #self._initialise_file()
        self._read_binary_file()

    def _initialise_file(self):
        """
        Initialising a binary file
        :return:
        """
        clients = [Client("A2949","Alexandra Trusova"), Client("A9294","Alena Kostornaia"), Client("M3848","Michael Johnson"), Client("R3030","Roman McKane"),
                   Client("R3030","Roman McKane"), Client("E3469","Elaine Sweets"), Client("J3838","Jane Karlson"), Client("H2949","Helene Bauer"),
                   Client("K9283","Kate Cameron"), Client("F0594","Fred Weasley"), Client("C5938","Cedric Diggory"), Client("S4002","Sirius Black")]
        try:
            f = open(self._file_name, "wb")
            pickle.dump(clients , f)
            f.close()
        except (EOFError,IOError):
            raise ValueError("Invalid file content.")

    def _read_binary_file(self):
        f = open(self._file_name,'rb')
        clients = pickle.load(f)
        for c in clients:
            ClientRepository.add_client(self, c)

    def add_client(self, client):
        ClientRepository.add_client(self, client)
        self._write_to_file()

    def remove_client_object(self, client):
        ClientRepository.remove_client_object(self, client)
        self._write_to_file()

    def list_clients(self, print_list):
        ClientRepository.list(self, print_list)

    def update_client(self, client, update_info, update_id):
        ClientRepository.update_client(self, client, update_info, update_id)
        self._write_to_file()

    def _write_to_file(self):
        f = open(self._file_name, 'bw')
        pickle.dump(self._client_list, f)
        f.close()


class RentalBinaryRepository(RentalRepository):
    def __init__(self, file_name):
        RentalRepository.__init__(self)
        self._file_name = file_name
        #self._initialise_file()
        self._read_binary_file()

    def _initialise_file(self):
        """
        Initialising a binary file
        :return:
        """
        rentals = [Rental("1000","1235A","E3469", date(2019,12,25), date(2020, 1,23)), Rental("1001","1356H","K9283",date(2020,10,12),date(2020,10,14)),
                   Rental("1002","1353A","F0594",date(2019,5,4),date(2020,2,2)), Rental("1003","3495G","R3030",date(2020,3,4),date(2020,4,5)),
                   Rental("1004","5040S","E3469",date(2019,4,5),date(2019,5,6)), Rental("1005","2939B","S4002",date(2019,5,14),date(2019,7,14)),
                   Rental("1006","2031L","S4002",date(2019,3,24),date(2019,11,23))]
        try:
            f = open(self._file_name, "wb")
            pickle.dump(rentals , f)
            f.close()
        except (EOFError,IOError):
            raise ValueError("Invalid file content.")

    def _read_binary_file(self):
        f = open(self._file_name,'rb')
        rentals = pickle.load(f)
        for rental in rentals:
            RentalRepository.add_rental(self, rental)

    def add_rental(self, rental):
        RentalRepository.add_rental(self, rental)
        self._write_to_file()

    def close_rental(self, returned_date, rental):
        RentalRepository.close_rental(self, returned_date, rental)
        self._write_to_file()

    def list_rentals(self, print_list):
        RentalRepository.list_rentals(self, print_list)
        self._write_to_file()

    def _write_to_file(self):
        f = open(self._file_name, 'bw')
        pickle.dump(self._rental_list, f)
        f.close()



