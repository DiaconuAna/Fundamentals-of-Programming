from datetime import date
from random import randrange, choice

from A10_module.iterable_data_structure import IterableStructure
from domain.book import Book, BookValidator, BookValidationException, BookException
from domain.client import ClientValidator, Client
from domain.rental import RentalValidator, RentalValidationException, Rental, RentalException


class BookRepository:
    def __init__(self):
        self._book_list = IterableStructure()

    def __len__(self):
        return len(self._book_list)

    @property
    def books(self):
        return self._book_list._list

    def add_book(self, book):
        """
        Adds a book object to the list
        Things to look out for:
        ID already in the list
        :param book:
        :return:
        """
        self._book_list.add_element(book)
        return book

    def list_books(self, print_list):
        book_list = self.books
        for index in range(len(book_list)):
            print_list.append(self._book_list.get(index))
            #print(self._book_list.get(index))

    def remove_book(self, book):
        """
        One can remove a book from the list based on its id, title or author
        If several books have the same author, only the first occurrence is removed
        If several books have the same title, only the first occurrence is removed
        :param book: Book object to be removed
        :return: -
        """
        index = self.find_book_index(book)
        self._book_list.delete_item(index)

    def update_book(self, book, update_info, update_id):
        """
        One can update all of a book's parameters: book_id, title, author
        The book the user wants to update the info for is found based on the book_data given
        If several books have the same author, only the first occurrence is updated
        If several books have the same title, only the first occurrence is updated
        IMPORTANT: If I change a book's title, the id also needs to be changed so that the first letter of the new title will be in it
        :param book: Book object to be updated
        :param update_info: Can be either book_id, author or title
        :param update_id: 1 for book_id, 2 for title, 3 for author
        :return: -
        """
        b1 = BookValidator()
        book_index = self.find_book_index(book)
        if update_id == '1':
            book._book_id = update_info
            b1.validate(book)
            new_book = Book(book.book_id, book.title, book.author)
            self._book_list.set(book_index, new_book)
        elif update_id == '2':
            book._book_id = book._book_id[:-1]
            book._book_id = book._book_id + update_info[0]
            book._title = update_info
            b1.validate(book)
            new_book = Book(book.book_id, book.title, book.author)
            self._book_list.set(book_index, new_book)
        elif update_id == '3':
            book._author = update_info
            b1.validate(book)
            new_book = Book(book.book_id, book.title, book.author)
            self._book_list.set(book_index, new_book)

    def find_book_index(self, book):
        """
        Find a book's position in the list
        :param book:
        :return:
        """
        book_list = self.books
        for index in range(len(book_list)):
            b1 = book_list[index]
            if b1.book_id == book.book_id:
                return index

    def generate_list(self, length):

        title = ['A Court of Thorns and Roses', 'The Last Wish', 'Sword of Destiny', 'Good Omens', 'Time of Contempt',
                 'A Court of Mist and Fury'
            , 'A Court of Wings and Ruin', "The Queen's Rising", 'Lady of the Lake',
                 'Harry Potter and the Prisoner of Azkaban', 'The Year After You'
            , 'Hold Still', 'All the Bright Places', "Since you've been gone", "Serpent&Dove", "The Hate U Give",
                 'My Heart and Other Black Holes', 'The Astonishing Colour of After']
        author = ["Sarah J. Maas", "Morgan Matson", "Andrzej Sapkowski", "Nina de Pass", "J.K.Rowling",
                  "Jennifer Niven", "Rebecca Ross", "Nina Lacour", "Angie Thomas"
            , "Neil Gaiman", 'Jasmine Warga', 'Emily X.R. Pan']

        for i in range(length):
            id_ = str(randrange(1000, 9999))
            book_title = choice(title)
            id_ = id_ + book_title[0]
            book_author = choice(author)
            book = Book(id_, book_title, book_author)
            self.add_book(book)


class ClientRepository:
    def __init__(self):
        self._client_list = IterableStructure()

    def __len__(self):
        return len(self._client_list)

    @property
    def clients(self):
        return self._client_list._list

    def add_client(self, client):
        """
        Adds a client to the list if its id is not in the list already
        :param client:
        :return:
        """
        self._client_list.add_element(client)

    def remove_client_object(self, client):
        """

        :param client:
        :return:
        """
        index = self.find_client_index(client)
        self._client_list.delete_item(index)
        return client

    def update_client(self, client, update_info, update_id):
        """
        One can update all of client's parameters: client_id, name
        The client the user wants to update the info for is found based on the client_data given
        If several clients have the same name, only the first occurrence is updated
        IMPORTANT: If I change a client's name, the id also needs to be changed so that the first letter of the new name
                   will be in it
        :param client: Used to identify the client we want to update
        :param update_info: Client's new info
        :param update_id: 1 if client_id, 2 if name
        :return:
        """
        c1 = ClientValidator()
        client_index = self.find_client_index(client)

        if update_id == '1':
            client.client_id = update_info
            c1.validate(client)
            new_client = Client(client.client_id, client.name)
            self._client_list.set(client_index, new_client)
        elif update_id == '2':
            aux = client.client_id[1:]
            client.client_id = aux
            client.client_id = update_info[0] + client.client_id
            client.name = update_info
            c1.validate(client)
            new_client = Client(client.client_id, client.name)
            self._client_list.set(client_index, new_client)

        return client

    def find_client_index(self, client):
        """
        Returns the index of a client if it's in the list
        :param client:
        :return: -1 if client is not in the list
        """
        client_list = self.clients
        for index in range(len(client_list)):
            c1 = client_list[index]
            if client.client_id == c1.client_id:
                return index

    def list(self, print_list):
        client_list = self.clients
        for index in range(len(client_list)):
            print_list.append(self._client_list.get(index))

    def generate_list(self, length):
        """
        Generate first 10 elements from a list
        Convention: client_id is of form first_name_letter + 4 digits
        Name is a string of letters
        :return:
        """

        first_name = ['Anna', 'Linda', 'Chloe', 'Jackson', 'Bill', 'John', 'Sarah', 'Jordan', 'Rose', 'Strip', 'Sasha',
                      'Aliona', 'Michael', 'Nathan', 'Brian', 'Frances', 'Leah', 'Fred', 'George', 'Harry', 'Jane']
        last_name = ['Larson', 'McLachlan', 'Smith', 'Jefferson', 'Goodwin', 'Harding', 'Price', 'White', 'Johnson',
                     'Kay', 'Harper', 'Thomson', 'Gardner', 'Dean', 'Hamilton', 'Murray']

        for i in range(length):
            id_ = str(randrange(1000, 9999))
            name = choice(first_name) + ' ' + choice(last_name)
            client_id = name[0] + id_
            client = Client(client_id, name)
            self.add_client(client)


"""
Rental: rental_id, book_id, client_id, rented_date, returned_date
Rent or return a book. A client can rent an available book.
A client can return a rented book at any time. Only available books can be rented.
"""

class RentalRepository:
    def __init__(self):
        self._rental_list = IterableStructure()

    def __len__(self):
        return len(self._rental_list)

    @property
    def rentals(self):
        return self._rental_list._list

    def list_rentals(self, print_list):
        rentals = self.rentals
        for index in range(len(rentals)):
            rental = self._rental_list.get(index)
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
        self._rental_list.add_element(rental)

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
        rental = Rental(rental.rental_id, rental.book_id, rental.client_id, rental.rented_date, returned_date)
        self._rental_list.set(rental_index, rental)

    def open_rental(self, rental):
        """
        Undo equivalent for close_rental- date is set to default
        :param rental:
        :return:
        """
        rental_index = self.find_rental_index(rental)
        rental = Rental(rental.rental_id, rental.book_id, rental.client_id, rental.rented_date, date(1,1,1))
        self._rental_list.set(rental_index, rental)

    def find_rental_index(self, rental):
        rental_list = self.rentals
        for index in range(len(rental_list)):
            r1 = self._rental_list.get(index)
            if r1.rental_id == rental.rental_id:
                return index

    def remove_rental(self, rental):
        rental_index = self.find_rental_index(rental)
        self._rental_list.delete_item(rental_index)

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
