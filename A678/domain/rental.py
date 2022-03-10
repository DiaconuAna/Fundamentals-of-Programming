"""
Rental entity is declared here
Rental: rental_id, book_id, client_id, rented_date, returned_date
Convention: rental_id is a string formed of 4 digits
"""
import datetime
from datetime import date


class RentalException(Exception):
    def __init__(self, msg = ''):
        self._msg = msg

class RentalValidationException(RentalException):
    def __init__(self, error_list):
        self._errors = error_list

    @property
    def errors(self):
        return self._errors

    def __str__(self):
        result = ''
        for e in self.errors:
            result += e
            result += '\n'
        return result


class Rental:
    def __init__(self, rental_id, book_id, client_id, rented_date, returned_date):
        self._rental_id = rental_id
        self._book_id = book_id
        self._client_id = client_id
        self._rented_date = rented_date
        self._returned_date = returned_date

    def print_rental(self, client, book):
        str1 = self._rental_id + ': ' + book.title + ' by ' + book.author
        str1 += ' is rented by ' + client.name
        str1 += '\n' + 'Rented at: ' + str(self.rented_date)
        d0 = date(1, 1, 1)
        if d0 != self._returned_date:
            str1 += '\n' + 'Returned at: ' + str(self._returned_date)
        else:
            str1 += '\n' + "Hasn't been returned yet"
        return str1

    @property
    def rental_id(self):
        return self._rental_id

    @property
    def book_id(self):
        return self._book_id

    @book_id.setter
    def book_id(self, value):
        self._book_id = value

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        self._client_id = value

    @property
    def rented_date(self):
        return self._rented_date

    @property
    def returned_date(self):
        return self._returned_date

    @returned_date.setter
    def returned_date(self, value):
        self._returned_date = value

"""
A client can rent an available book. A client can return a rented book at any time. Only available books can be rented.
Create a rental_list in the rental_repo- if the book_id is in the rental list and the returned date has not been specified yet
it means the book is not available- raise the error in the rental_repo. 
Other errors to be raised in the rental_repo - if the book or the client don't exist in the database.
! Cannot return a book that has no rental date//hasn't been rented yet

Rent - returned data is automatically set to 0
"""


class RentalValidator:
    def validate(self, rental):
        """
        Validate the input data for a given rental object
        :param rental: -
        :return: -
        """
        errors = []

        if len(rental.rental_id) != 4 or not rental.rental_id.isdigit():
            errors.append("Invalid rental id- should be a 4-digit code")

        #Returned date shouldn't be before rented_date
        ok = self.date_validator(rental.rented_date, rental.returned_date)

        if ok == 0:
            errors.append("Invalid return date! One cannot return a book they have not rented yet!")

        if len(errors) != 0:
            raise RentalValidationException(errors)

    def date_validator(self, rent_date, returned_date):
        """
        Checks if returned_date is valid
        :param rent_date:
        :param returned_date:
        :return:
        """
        # Returned date shouldn't be before rented_date
        rent_date = str(rent_date)
        returned_date = str(returned_date)
        rent_date1 = datetime.datetime.strptime(rent_date, "%Y-%m-%d")
        returned_date1 = datetime.datetime.strptime(returned_date, "%Y-%m-%d")
        if not (returned_date1.year == 1 and returned_date1.day == 1 and returned_date1.month == 1):
            if returned_date1.year < rent_date1.year:
                return 0
            if returned_date1.year == rent_date1.year and returned_date1.month < rent_date1.month:
                return 0
            if returned_date1.year == rent_date1.year and returned_date1.month == rent_date1.month and returned_date1.day < rent_date1.day:
                return 0

        return 1


