from domain.book import Book, BookValidator, BookException
from service.undo_service import FunctionCall, Operation, CascadedOperation


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

    def generate_list(self, length):
        self._books_list.generate_list(length)

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
        self.search_by_id(data, search_list)
        self.search_by_title(data, search_list)
        self.search_by_author(data, search_list)
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
