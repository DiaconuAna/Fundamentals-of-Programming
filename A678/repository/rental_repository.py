"""
Rental: rental_id, book_id, client_id, rented_date, returned_date
Rent or return a book. A client can rent an available book.
A client can return a rented book at any time. Only available books can be rented.
"""
from datetime import date
from random import randrange, choice
from domain.rental import RentalException, RentalValidator, Rental, RentalValidationException


class RentalRepository:
    def __init__(self):
        self._rental_list = []

    def __len__(self):
        return len(self._rental_list)

    def get_last_rental(self):
        return self._rental_list[-1]

    @property
    def rentals(self):
        return self._rental_list

    def list_rentals(self, print_list):
        for index in range(len(self)):
            rental = self._rental_list[index]
            print_list.append(rental)

    def add_rental(self, rental):
        """
        A rental consists of a rental_id, book_id, client_id, rented_date, returned_date which is 1,1,1 as the book
        has just been rented, not returned
        Raises RentalException if:
           -> book_id is already in the list and its rental hasn't been closed <=> the book has already been rented and hasn't been returned yet
           -> two rentals have the same id
        :param rental:
        :return:
        """
        r1 = RentalValidator()
        r1.validate(rental)
        self._rental_list.append(rental)

    def close_rental(self, returned_date, rental):
        """
        We say a rental is closed if the rented book has been returned
        The rental is identified by its rental_id
        Raises RentalException if:
        -> rental does not exist
        -> returned date is incorrect (RentalValidateException here)
        :param returned_date:
        :param rental:
        :return:
        """
        #if the rental is valid, meaning the returned date is valid, we close the proper rental
        rental_index = self.find_rental_index(rental)
        self._rental_list[rental_index].returned_date = returned_date

    def open_rental(self, rental):
        """
        Undo equivalent for close_rental- date is set to default
        :param rental:
        :return:
        """
        rental_index = self.find_rental_index(rental)
        self._rental_list[rental_index].returned_date = date(1,1,1)

    def find_rental_index(self, rental):
        for index in range(len(self._rental_list)):
            r1 = self._rental_list[index]
            if r1.rental_id == rental.rental_id:
                return index

    def remove_rental(self, rental):
        #rental_index = self.find_rental_index(rental)
        self._rental_list.remove(rental)

    def generate_rentals(self, client_list, book_list):
        """
        Generate rentals taking book_id and client_id from the current clients and books list
        Rental: rental_id, book_id, client_id, rented_date, returned_date
        Rental_id = string of 4 digits
        :return:
        """
        number_of_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        i = 0
        while i < 10:
            rental_id = str(randrange(1000, 9999))
            year = 2020
            month = randrange(1, 12)
            day = randrange(1, number_of_days[month-1])
            rented_date = date(year, month, day)
            year = 2020
            month = randrange(1, 12)
            day = randrange(1, number_of_days[month-1])
            returned_date = date(year, month, day)
            client = choice(client_list.clients)
            client_id = client.client_id
            book = choice(book_list.books)
            book_id = book.book_id
            rental = Rental(rental_id, book_id, client_id, rented_date, returned_date)

            try:
                self.add_rental(rental)
                i += 1
            except (RentalValidationException, RentalException):
                continue
