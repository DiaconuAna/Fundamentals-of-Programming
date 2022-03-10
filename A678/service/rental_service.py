from datetime import date

from domain.rental import Rental, RentalValidator, RentalException
from service.undo_service import FunctionCall, Operation


class RentalService:
    def __init__(self, rental_repo, book_repo, client_repo, undo_service):
        self._rentals_list = rental_repo
        self._book_list = book_repo
        self._client_list = client_repo
        self._undo_service = undo_service

    @property
    def rental_list(self):
        return self._rentals_list.rentals

    def find_book_id(self, book_id):
        """
        Checks if a book has already been rented(is in the rental list)
        :param book_id:
        :return: 1 if the book is available, -1 if the book has already been rented
        """
        rental_list = self._rentals_list.rentals
        for index in range(len(rental_list)):
            rental = rental_list[index]
            d1 = date(1,1,1)
            if book_id == rental.book_id and rental._returned_date == d1:
                return -1
        return 1

    def find_rental_by_id(self, rental_id):
        """
        Finds a rental by a given id
        :param rental_id:
        :return: rental index if it's in the list, else -1
        """
        rental_list = self._rentals_list.rentals
        for index in range(len(rental_list)):
            rental = rental_list[index]
            if rental_id == rental.rental_id:
                return index
        return -1

    def filter_clients(self, client_id):
        """
        Returns client's rentals
        :param client_id:
        :return:
        """
        result = []
        rental_list = self._rentals_list.rentals
        for index in range(len(rental_list)):
            rental = rental_list[index]
            if rental.client_id == client_id:
                result.append(rental)
        return result

    def filter_books(self, book_id):
        """
        Returns book's rentals
        :param book_id:
        :return:
        """
        result = []
        rental_list = self._rentals_list.rentals
        for index in range(len(rental_list)):
            rental = rental_list[index]
            if rental.book_id == book_id:
                result.append(rental)
        return result

    def create_rental(self, rental_id, book_id, client_id, rented_date, returned_date):
        """
        Since we create the rental for  a new rental, the returned date is 1
        :param rental_id:
        :param book_id:
        :param client_id:
        :param rented_date:
        :param returned_date:
        :return:
        """
        rental = Rental(rental_id, book_id, client_id, rented_date, returned_date)
        r1 = RentalValidator()
        r1.validate(rental)

        book_availability = self.find_book_id(book_id)
        if book_availability == -1:
            raise RentalException("We're sorry but the book has already been rented!")
        rental_list = self._rentals_list.rentals
        for index in range(len(rental_list)):
            rental1 = rental_list[index]
            if rental1.rental_id == rental.rental_id:
                raise RentalException("Two rentals cannot have the same id.")

        self._rentals_list.add_rental(rental)
        undo = FunctionCall(self._rentals_list.remove_rental, rental)
        redo = FunctionCall(self._rentals_list.add_rental, rental)
        operation = Operation(undo, redo)
        self._undo_service.add_operation(operation)

    def close_rental(self, rental_id, returned_date):
        """
        Close the rental given by rental_id
        :param rental_id:
        :param returned_date:
        :return:
        """
        rental_list = self._rentals_list.rentals
        rental_index = self.find_rental_by_id(rental_id)
        if rental_index == -1:
            raise RentalException("Rental does not exist!")
        rental = rental_list[rental_index]
        rental.returned_date = returned_date
        r1 = RentalValidator()
        r1.validate(rental)
        self._rentals_list.close_rental(returned_date, rental)
        undo = FunctionCall(self._rentals_list.open_rental, rental)
        redo = FunctionCall(self._rentals_list.close_rental, returned_date, rental)
        operation = Operation(undo, redo)
        self._undo_service.add_operation(operation)

    def update_rental(self, rental_id, update_info, update_id):
        """
        If a book's or a client's data changes, the corresponding rental changes as well
        :param rental_id:
        :param update_info:
        :param update_id: 1 for book_id, 2 for client_id
        :return:
        """
        rental_index = self.find_rental_by_id(rental_id)
        if rental_index == -1:
            raise RentalException("Rental does not exist")
        if update_id == '1':
            self._rentals_list.rentals[rental_index].book_id = update_info
        elif update_id == '2':
            self._rentals_list.rentals[rental_index].client_id = update_info


    def delete_rental(self, rental_id):
        """
        Remove a rental based on its id
        :param rental_id:
        :return:
        """
        index = self.find_rental_by_id(rental_id)
        if index == -1:
            raise RentalException("Rental does not exist!")
        rental = self._rentals_list.rentals[index]
        self._rentals_list.remove_rental(rental)

    def list_rentals(self, print_list):
        self._rentals_list.list_rentals(print_list)

    def generate_list(self):
        self._rentals_list.generate_rentals(self._client_list, self._book_list)

    def number_of_rentals(self, book_id):
        """
        Counts for how many times a  book identified by its id has been rented
        :param book_id: Book id
        :return: Number of times the book has been rented
        """
        time_counter = 0
        rental_list = self._rentals_list.rentals
        for index in range(len(rental_list)):
            rental = rental_list[index]
            if book_id == rental.book_id:
                time_counter += 1
        return time_counter

    def most_rented_books(self, book_list):
        """
        This will provide the list of books, sorted in descending order of the number of times they were rented.
        :return:
        """
        results = []

        for index in range(len(book_list)):
            b1 = book_list[index]
            rented_times = self.number_of_rentals(b1.book_id)
            results.append(BookRental(b1.book_id, b1.title, b1.author, rented_times))

        results.sort(key = lambda x: x.rental_times, reverse=True)
        return results

    def number_of_days(self, client_id):
        """
        Computes the number of book rental days a client identified by their id has
        :param client_id:
        :return:
        """
        number_of_days = 0
        rental_list = self._rentals_list.rentals
        for index in range(len(rental_list)):
            rental = rental_list[index]
            rental_date = rental.rented_date
            return_date = rental.returned_date
            if client_id == rental.client_id:
                if rental.returned_date != date(1,1,1):
                    delta = return_date - rental_date
                    number_of_days += delta.days
                else:
                    today = date.today()
                    delta = today - rental_date
                    number_of_days += delta.days

        return number_of_days

    def most_active_clients(self, client_list):
        """
        This will provide the list of clients, sorted in descending order of the number of book rental days they have
        :param client_list:
        :return:
        """
        results = []

        for index in range(len(client_list)):
            c1 = client_list[index]
            rented_days = self.number_of_days(c1.client_id)
            results.append(ClientRental(c1.client_id, c1.name, rented_days))

        results.sort(key=lambda x: x.rental_days, reverse=True)
        return results

    def number_of_rentals_per_author(self, author, book_list):
        """
        Counts how many rentals has each book written by the given author
        :param book_list:
        :param author:
        :return:
        """
        counter = 0
        for index in range(len(book_list)):
            book = book_list[index]
            if book.author == author:
                counter += self.number_of_rentals(book.book_id)

        return counter

    def most_rented_authors1(self, book_list):
        """
        :param book_list:
        :return:
        """
        results = []
        author_list = []
        for index in range(len(book_list)):
            b1 = book_list[index]
            if b1.author not in author_list:
                author_list.append(b1.author)

        for index in range(len(author_list)):
            rental_times = self.number_of_rentals_per_author(author_list[index], book_list)
            results.append(AuthorRental11(author_list[index], rental_times))

        results.sort(key=lambda x: x.rental_times, reverse=True)
        return results


class BookRental:
    def __init__(self, book_id, book_title, book_author, rental_times):
        self._book_id = book_id
        self._rental_times = rental_times
        self._title = book_title
        self._author = book_author

    @property
    def book_id(self):
        return self._book_id

    @property
    def rental_times(self):
        return self._rental_times

    def __str__(self):
        final = str(self._book_id).rjust(2) + ': ' + str(self._title).rjust(5) + ' by ' + str(self._author).ljust(3).rjust(7)
        final += ' >>>>Rented for: '.ljust(10) + str(self._rental_times) + ' times.'
        return final


class ClientRental:
    def __init__(self, client_id, client_name, rental_days):
        self._client_id = client_id
        self._client_name = client_name
        self._rental_days = rental_days

    @property
    def rental_days(self):
        return self._rental_days

    def __str__(self):
        return str(self._client_id) +": " + str(self._client_name).ljust(7) + " has " + str(self._rental_days) + " rental days."


class AuthorRental11:
    def __init__(self, author, rental_times):
        self._author = author
        self._rental_times = rental_times

    @property
    def author(self):
        return self._author

    @property
    def rental_times(self):
        return self._rental_times

    def __str__(self):
        return str(self._author).ljust(5) + " 's books have been rented for: " + str(self._rental_times) + ' times.'


