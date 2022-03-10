from datetime import date, datetime


class GUi:
    def __init__(self, book_service, client_service, rental_service, undo_service):
        self._books = book_service
        self._clients = client_service
        self._rentals = rental_service
        self._undo = undo_service

    def add_client(self, client_id, name):
        id_ = name[0] + client_id
        self._clients.add_client(id_, name)

    def add_book(self, book_id, title, author):
        book_id += title[0]
        self._books.add_book(book_id, title, author)

    def list_clients_ui(self):
        print_list = []
        self._clients.list_clients(print_list)
        return print_list

    def list_books_ui(self):
        print_list = []
        self._books.list_books(print_list)
        return print_list

    def remove_client_ui(self, data):
        self._clients.remove_client(data)

    def remove_book_ui(self, data):
        self._books.remove_book(data)

    def update_client_ui(self, data, update_info, update_id):
            self._clients.update_client(data, update_info, update_id)

    def update_book_ui(self, data, update_info, update_id):
            self._books.update_book(data, update_info, update_id)

    def update_ui(self):
        print("**********")
        print("1. Update a client.")
        print("2. Update a book.")
        command = input("Enter your choice: ")
        if command == '1':
            self.update_client_ui()
        elif command == '2':
            self.update_book_ui()
        else:
            raise ValueError("Invalid command.")

    def rent_ui(self, rental_date, book_data, client_data, rental_id):
        returned_date = date(1, 1, 1)
        book = self._books.get_book(book_data)
        client = self._clients.get_client(client_data)
        self._rentals.create_rental(rental_id, book.book_id, client.client_id, rental_date, returned_date)

    def return_ui(self, rental_id, returned_date):
        self._rentals.close_rental(rental_id, returned_date)

    def list_rentals_ui(self):
        client_list = self._clients.client_repo
        book_list = self._books.book_repo
        print_list = []
        self._rentals.list_rentals(print_list)
        list = []
        for index in range(len(print_list)):
            rental = print_list[index]
            client_index = self._clients.find_client(rental.client_id)
            client = client_list.clients[client_index]
            book_index = self._books.find_book(rental.book_id)
            book = book_list.books[book_index]
            str1 = rental.rental_id + ': ' + book.title + ' by ' + book.author
            str1 += ' is rented by ' + client.name
            str1 += '\n' + 'Rented at: ' + str(rental.rented_date)
            d0 = date(1, 1, 1)
            if d0 != rental.returned_date:
                str1 += '\n' + 'Returned at: ' + str(rental.returned_date)
            else:
                str1 += '\n' + "Hasn't been returned yet"
            list.append(str1)
        return list

    def search_books(self, data):
        search_list = []
        self._books.search_book(data, search_list)
        return search_list

    def search_clients(self, data):
        search_list = []
        self._clients.search_client(data, search_list)
        return search_list

    def most_rented_books(self):
        book_list = self._books.book_repo.books
        results = self._rentals.most_rented_books(book_list)
        return results

    def most_active_clients(self):
        client_list = self._clients.client_repo.clients
        results = self._rentals.most_active_clients(client_list)
        return results

    def most_rented_author(self):
        book_list = self._books.book_repo.books
        results = self._rentals.most_rented_authors1(book_list)
        return results

    def undo_ui(self):
        self._undo.undo()

    def redo_ui(self):
        self._undo.redo()