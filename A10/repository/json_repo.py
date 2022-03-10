import json
from datetime import date

from domain.book import Book
from domain.client import Client
from domain.rental import Rental
from repository.big_repo import BookRepository, ClientRepository, RentalRepository


class BookJSONRepository(BookRepository):
    def __init__(self, file_name):
        BookRepository.__init__(self)
        self._file_name = file_name
        self._read_json_file()

    def _read_json_file(self):
        try:
            f = open(self._file_name, 'r')
            books_dict = json.load(f)
            for index in range(len(books_dict)):
                book = Book(books_dict[index]['book_id'], books_dict[index]['title'], books_dict[index]['author'])
                BookRepository.add_book(self, book)
        except (IOError, EOFError):
            raise ValueError("Invalid file input.")

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
        f = open(self._file_name, 'w')
        books_dict = []
        for book in self._book_list:
            object = {"book_id": book.book_id, "title": book.title, "author": book.author}
            books_dict.append(object)
        json.dump(books_dict, f)
        f.close()


class ClientJSONRepository(ClientRepository):
    def __init__(self, file_name):
        ClientRepository.__init__(self)
        self._file_name = file_name
        self._read_json_file()


    def _read_json_file(self):
        try:
            f = open(self._file_name, 'r')
            clients_dict = json.load(f)
            for index in range(len(clients_dict)):
                client = Client(clients_dict[index]['client_id'], clients_dict[index]['name'])
                ClientRepository.add_client(self, client)
        except (EOFError, IOError):
            raise ValueError("Invalid file content.")

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
        f = open(self._file_name, 'w')
        clients_dict = []
        for client in self._client_list:
            object = {"client_id": client.client_id, "name": client.name}
            clients_dict.append(object)
        json.dump(clients_dict, f)
        f.close()


class RentalJSONRepository(RentalRepository):
    def __init__(self, file_name):
        RentalRepository.__init__(self)
        self._file_name = file_name
        self._read_json_file()


    def _read_json_file(self):
        try:
            f = open(self._file_name, 'r')
            rentals_dict = json.load(f)
            for index in range(len(rentals_dict)):
                rented_date = date(int(rentals_dict[index]['rented_date']['year']), int(rentals_dict[index]['rented_date']['month']), int(rentals_dict[index]['rented_date']['day']))
                returned_date = date(int(rentals_dict[index]['returned_date']['year']), int(rentals_dict[index]['returned_date']['month']), int(rentals_dict[index]['returned_date']['day']))
                rental = Rental(rentals_dict[index]['rental_id'], rentals_dict[index]["book_id"], rentals_dict[index]['client_id'], rented_date, returned_date)
                RentalRepository.add_rental(self, rental)
        except (EOFError, IOError):
            raise ValueError("Invalid file content.")

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
        f = open(self._file_name, 'w')
        rentals_dict = []
        for rental in self._rental_list:
            rental_object = {"rental_id": rental.rental_id, "book_id": rental.book_id, "client_id": rental.client_id,
                             "rented_date": {"year":str(rental.rented_date.year), "month": str(rental.rented_date.month), "day": str(rental.rented_date.day)},
                             "returned_date": {"year":str(rental.returned_date.year), "month": str(rental.returned_date.month), "day": str(rental.returned_date.day)}}
            rentals_dict.append(rental_object)
        json.dump(rentals_dict, f)
        f.close()


