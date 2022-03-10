from datetime import datetime, date

from domain.book import Book
from domain.client import Client
from domain.rental import Rental
from repository.big_repo import BookRepository, ClientRepository, RentalRepository


class BookTextRepository(BookRepository):
    def __init__(self, file_name):
        BookRepository.__init__(self)
        self._file_name = file_name
        self._load_file()

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

    def _load_file(self):
            """
            Loading data from file
            """
            try:
                f = open(self._file_name, 'rt')  # read text
                lines = f.readlines()
                f.close()

                for line in lines:
                    line = line.split(';')
                    # book_id, title, author
                    BookRepository.add_book(self, Book(line[0].strip(), line[1].strip(), line[2].strip()))
            except IOError:
                raise ValueError("Input file not found!")

    def _write_to_file(self):
            f = open(self._file_name,"w")
            for book in self._book_list:
                line = str(book.book_id) + ';' + book.title + ';' + book.author
                f.write(line)
                f.write('\n')
            f.close()


class ClientTextRepository(ClientRepository):
    def __init__(self, file_name):
        ClientRepository.__init__(self)
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
            """
            Loading data from file
            """
            try:
                f = open(self._file_name, 'rt')  # read text
                lines = f.readlines()
                f.close()

                for line in lines:
                    line = line.split(';')
                    # client_id, name
                    ClientRepository.add_client(self, Client(line[0].strip(),line[1].strip()))
            except IOError:
                raise ValueError("Input file not found!")

    def add_client(self, client):
        ClientRepository.add_client(self, client)
        self._write_to_file()

    def remove_client_object(self, client):
        ClientRepository.remove_client_object(self, client)
        self._write_to_file()

    def update_client(self, client, update_info, update_id):
        ClientRepository.update_client(self, client, update_info, update_id)
        self._write_to_file()

    def list(self, print_list):
        ClientRepository.list(self, print_list)

    def _write_to_file(self):
            f = open(self._file_name,"w")
            for client in self._client_list:
                line = str(client.client_id) + ';' + client.name
                f.write(line)
                f.write('\n')
            f.close()


class RentalTextRepository(RentalRepository):
    def __init__(self, file_name):
        RentalRepository.__init__(self)
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        """
        Loading data from file
        """
        try:
            f = open(self._file_name, 'rt')  # read text
            lines = f.readlines()
            f.close()

            for line in lines:
                line = line.split(';')
                # rental_id, book_id, client_id, rented date(YY-MM-DD), returned date(same format)
                rdate = line[3].strip().split("-",3)
                rented_date = date(int(rdate[0].strip()),int(rdate[1].strip()),int(rdate[2].strip()))
                retdate = line[4].strip().split("-",3)
                returned_date = date(int(retdate[0].strip()),int(retdate[1].strip()),int(retdate[2].strip()))
                RentalRepository.add_rental(self, Rental(line[0], line[1], line[2], rented_date, returned_date))
        except IOError:
            raise ValueError("Input file not found!")

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
            f = open(self._file_name,"w")
            for rental in self.rentals:
                line = rental.rental_id +';'+ rental.book_id +';'+ rental.client_id +';'
                rt_date = rental.rented_date
                line += str(rt_date.year) + "-" + str(rt_date.month) + '-' + str(rt_date.day) +';'
                ret_date = rental.returned_date
                line += str(ret_date.year) + '-' + str(ret_date.month) + '-' + str(ret_date.day)
                f.write(line)
                f.write('\n')
            f.close()