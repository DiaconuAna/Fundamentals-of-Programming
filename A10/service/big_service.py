from A10_module.Filter import filter_function
from A10_module.Gnome_Sort import gnome_sort
from domain.book import Book, BookValidator, BookException
from domain.client import Client, ClientValidator, ClientException
from service.undo_service import FunctionCall, Operation, CascadedOperation
from domain.rental import Rental, RentalValidator, RentalException
from datetime import date




class BookService:
    def __init__(self, book_repo, rental_service, undo_service):
        self._books_list = book_repo
        self._rental_service = rental_service
        self._undo_service = undo_service

    @property
    def book_repo(self):
        return self._books_list

    def __len__(self):
        return len(self.book_repo.books)

    def find_book(self, data):
        """
        Finds a book in book_list based on the given data
        :param data: Can either be the book's id, author or title
        :return: Index in the book_list of the first book object
        """
        book_list = self._books_list.books
        for b in range(len(book_list)):
            book1 = book_list[b]
            if data in book1._book_id or data.lower() == book1._title.lower() or data.lower() == book1._author.lower():
                return b
            #index of the book

        return -1

    def add_book(self, book_id, title, author):
        book_list = self._books_list.books
        book = Book(book_id, title, author)
        b1 = BookValidator()
        b1.validate(book)
        for b in range(len(book_list)):
            book1 = book_list[b]
            if book._book_id == book1._book_id:
                raise BookException("Two books cannot have the same id")
        self._books_list.add_book(book)
        undo = FunctionCall(self._books_list.remove_book, book)
        redo = FunctionCall(self._books_list.add_book, book)
        operation = Operation(undo, redo)
        self._undo_service.add_operation(operation)

    def remove_book(self, data):
        book_index = self.find_book(data)
        book = self._books_list.books[book_index]
        if book_index != -1:
            self._books_list.remove_book(book)

            undo = FunctionCall(self._books_list.add_book, book)
            redo = FunctionCall(self._books_list.remove_book, book)
            operation = Operation(undo, redo)
            #self._undo_service.add_operation(operation)
            cascade_list = [operation]
            rental_list = self._rental_service.filter_books(book.book_id)
            if len(rental_list) != 0:
                for rent in rental_list:
                    self._rental_service.delete_rental(rent.rental_id)
                    undo = FunctionCall(self._rental_service._rentals_list.add_rental, rent)
                    redo = FunctionCall(self._rental_service._rentals_list.remove_rental, rent)
                    cascade_list.append(Operation(undo, redo))

                cop = CascadedOperation(*cascade_list)
                self._undo_service.add_operation(cop)
        else:
            raise BookException("Invalid data given. No book could be removed.")

    def update_book(self, data, update_info, update_id):
        """
        One can update all of a book's parameters: book_id, title, author
        The book the user wants to update the info for is found based on the book_data given
        If several books have the same author, only the first occurrence is updated
        If several books have the same title, only the first occurrence is updated
        IMPORTANT: If I change a book's title, the id also needs to be changed so that the first letter of the new title will be in it
        :param book_data: Used to identify the book the user wants to update
        :param update_info: Can be either book_id, author or title
        :param update_id: 1 for book_id, 2 for title, 3 for author
        :return: -
        """
        book_index = self.find_book(data)
        book = self._books_list.books[book_index]
        if book_index == -1:
            raise BookException("Invalid data given. No book could be updated.")

        if update_id == '1':
            initial_data = book.book_id
            rental_list = self._rental_service.filter_books(book.book_id)
            if len(rental_list) != 0:
                for rent in rental_list:
                    self._rental_service.update_rental(rent.rental_id, update_info, '1')
        if update_id == '2':
            initial_data = book.title
        elif update_id == '3':
            initial_data = book.author

        self._books_list.update_book(book, update_info, update_id)
        undo = FunctionCall(self._books_list.update_book, book, initial_data, update_id)
        redo = FunctionCall(self._books_list.update_book, book, update_info, update_id)
        operation = Operation(undo, redo)
        self._undo_service.add_operation(operation)

    def list_books(self, print_list):
        self._books_list.list_books(print_list)

    def get_list(self):
        return self._books_list.books

    def get_book(self, data):
        """
        Finds a book in the list by given data
        :param data:
        :return:
        """
        index = self.find_book(data)
        if index == -1:
            raise BookException("No book could be found.")
        return self._books_list.books[index]

    def search_book(self, data, search_list):
        """
        Search for books using any one of their fields ( id, title or author).
        The search must work using case-insensitive, partial string matching, and must return all matching items
        :param data:
        :param search_list:
        :return:
        """
        book_list = self.book_repo.books
        list = filter_function(book_list, lambda x: data.lower() in x.book_id.lower())
        if len(list) != 0:
            search_list.extend(list)
        list = filter_function(book_list, lambda x: data.lower() in x.title.lower())
        if len(list) != 0:
            search_list.extend(list)
        list = filter_function(book_list, lambda x: data.lower() in x.author.lower())
        if len(list) != 0:
            search_list.extend(list)

        if len(search_list) == 0:
            raise BookException("No matches for the given data!")


    def search_by_id(self, data, search_list):
        """
        Search a book by its id
        :param data:
        :param search_list:
        :return: 1 if it's in the list, else 0
        """
        book_list = self.book_repo.books
        for index in range(len(book_list)):
            book = book_list[index]
            if data.lower() in book._book_id.lower():
                search_list.append(book)

    def search_by_title(self, data, search_list):
        """
        Search a book by its title
        :param data:
        :param search_list:
        :return: 1 if it's in the list, else 0
        """
        book_list = self.book_repo.books
        for index in range(len(book_list)):
            book = book_list[index]
            if data.lower() in book._title.lower():
                search_list.append(book)

    def search_by_author(self, data, search_list):
        """
        Search a book by its author
        :param data:
        :param search_list
        :return: 1 if it's in the list, else 0
        """
        book_list = self.book_repo.books
        for index in range(len(book_list)):
            book = book_list[index]
            if data.lower() in book._author.lower():
                search_list.append(book)


class ClientService:
    def __init__(self, client_repo, rental_service, undo_service):
        self._clients_list = client_repo
        self._rental_service = rental_service
        self._undo_service = undo_service

    @property
    def client_repo(self):
        return self._clients_list

    def find_client(self, data):
        """
        Finds whether a client is in the list or not based on the given data
        :param data:
        :return: client's index
        """
        for index in range(len(self._clients_list.clients)):
            client = self._clients_list.clients[index]
            if data == client.client_id or data.lower() == client.name.lower():
                return index
        return -1

    def add_client(self, client_id, name):
        client = Client(client_id, name)
        c1 = ClientValidator()
        c1.validate(client)
        client_list = self._clients_list.clients

        for c in range(len(client_list)):
            client1 = client_list[c]
            if client.client_id == client1.client_id:
                raise ClientException("Two clients cannot have the same id")

        self._clients_list.add_client(client)

        undo = FunctionCall(self._clients_list.remove_client_object, client )
        redo = FunctionCall(self._clients_list.add_client, client)
        operation = Operation(undo, redo)
        self._undo_service.add_operation(operation)

    def remove_client(self, data):
        client_index = self.find_client(data)
        if client_index != -1:
            client = self._clients_list.clients[client_index]

            self._clients_list.remove_client_object(client)
            undo = FunctionCall(self._clients_list.add_client, client)
            redo = FunctionCall(self._clients_list.remove_client_object, client)
            operation = Operation(undo, redo)
            #self._undo_service.add_operation(operation)
            cascade_list = [operation]

            rental_list = self._rental_service.filter_clients(client.client_id)
            if len(rental_list) != 0:
                for rent in rental_list:
                    self._rental_service.delete_rental(rent.rental_id)
                    undo = FunctionCall(self._rental_service._rentals_list.add_rental, rent)
                    redo = FunctionCall(self._rental_service._rentals_list.remove_rental, rent)
                    cascade_list.append(Operation(undo, redo))

            cop = CascadedOperation(*cascade_list)
            self._undo_service.add_operation(cop)
        else:
            raise ClientException("Invalid data given. No client could be removed.")

    def update_client(self, data, update_info, update_id):
        client_index = self.find_client(data)
        client = self._clients_list.clients[client_index]
        if client_index == -1:
            raise ClientException("Invalid data given. No client could be updated.")
        if update_id == '1':
            initial_data = client.client_id
            rental_list = self._rental_service.rental_list
            for rental in rental_list:
                if rental.client_id == client.client_id:
                    self._rental_service.update_rental(rental.rental_id, update_info, '2')

        if update_id == '2':
            initial_data = client.name

        updated_client = self._clients_list.update_client(client, update_info, update_id)
        undo = FunctionCall(self._clients_list.update_client, updated_client, initial_data, update_id)
        redo = FunctionCall(self._clients_list.update_client, client, update_info, update_id)
        operation = Operation(undo, redo)
        self._undo_service.add_operation(operation)

    def list_clients(self, print_list):
        self._clients_list.list(print_list)


    def get_list(self):
        return self._clients_list.clients

    def get_client(self, data):
        """
        Find client by given data
        :param data:
        :return:
        """
        index = self.find_client(data)
        if index == -1:
            raise ClientException("Client could not be found.")
        return self._clients_list.clients[index]

    def search_client(self, data, search_list):
        """
        Search for clients using any one of their fields (client_id, name).
        The search must work using case-insensitive, partial string matching, and must return all matching items.
        :param data:
        :param search_list:
        :return:
        """
        client_list = self.client_repo.clients
        list1 = filter_function(client_list, lambda x: data.lower() in x.client_id.lower())
        if len(list1) != 0:
            search_list.extend(list1)
        list2 = filter_function(client_list, lambda x: data.lower() in x.name.lower())
        if len(list2) != 0:
            search_list.extend(list2)

        if len(search_list) == 0:
            raise ClientException("No matches for the given data!")


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
        gnome_sort(results, lambda x,y: x.rental_times > y.rental_times)
        #results.sort(key = lambda x: x.rental_times, reverse=True)
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

        gnome_sort(results, lambda x,y: x.rental_days > y.rental_days)
        #results.sort(key=lambda x: x.rental_days, reverse=True)
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

        gnome_sort(results, lambda x,y: x.rental_times > y.rental_times)
        #results.sort(key=lambda x: x.rental_times, reverse=True)
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


