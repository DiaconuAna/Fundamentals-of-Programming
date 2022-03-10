from datetime import date

from domain.book import BookValidationException, BookException
from domain.client import ClientValidationException, ClientException
from domain.rental import RentalValidationException, RentalException
from repository.book_repository import BookRepository
from repository.client_repository import ClientRepository
from repository.rental_repository import RentalRepository
from service.book_service import BookService
from service.client_service import ClientService
from service.rental_service import RentalService
from service.undo_service import UndoService

"""
Create the lists for each entity in start and send them as parameters for the services
"""

class Ui:
    def __init__(self, book_repo, client_repo, rental_repo):
        """
        client_repo = ClientRepository()
        client_repo.generate_list()
        book_repo = BookRepository()
        book_repo.generate_list()
        rental_repo = RentalRepository()
        rental_repo.generate_rentals(client_repo, book_repo)
        """
        self._undo_service = UndoService()
        self._rental_service = RentalService(rental_repo, book_repo, client_repo, self._undo_service)
        self._book_service = BookService(book_repo, self._rental_service, self._undo_service)
        self._client_service = ClientService(client_repo, self._rental_service, self._undo_service)


    def add_book_ui(self):
        print("**********")
        print("Input book data>>>")
        title = input("Give me a title: ")
        author = input("Now an author: ")
        book_id = input("Now a 4-digit id: ")
        book_id += title[0]
        self._book_service.add_book(book_id, title, author)

    def add_client_ui(self):
        print("**********")
        print("Input client data>>>")
        name = input("What's your client's name? ")
        id_ = input("Give me a 4-digit id: ")
        client_id = name[0] + id_
        self._client_service.add_client(client_id, name)

    def add_ui(self):
        print("**********")
        print("1. Add a client.")
        print("2. Add a book.")
        command = input("Enter your choice: ")
        if command == '1':
            self.add_client_ui()
        elif command == '2':
            self.add_book_ui()
        else:
            raise ValueError("Invalid command.")

    def remove_client_ui(self):
        """
        One can remove a client from the list based on their id or name
        If several clients have the same name, only the first occurrence is removed
        :return: -
        """
        print("Input data of the client you want to remove: ")
        data = input()
        self._client_service.remove_client(data)

    def remove_book_ui(self):
        """
        One can remove a book from the list based on its id, title or author
        If several books have the same author, only the first occurrence is removed
        If several books have the same title, only the first occurrence is removed
        :return:
        """
        print("Input data of the book you want to remove: ")
        data = input()
        self._book_service.remove_book(data)

    def remove_ui(self):
        print("**********")
        print("1. Remove a client.")
        print("2. Remove a book.")
        command = input("Enter your choice: ")
        if command == '1':
            self.remove_client_ui()
        elif command == '2':
            self.remove_book_ui()
        else:
            raise ValueError("Invalid command.")

    def list_clients_ui(self):
        print("********** \n")
        print_list = []
        self._client_service.list_clients(print_list)
        self.display_list(print_list)
        print("\n **********")

    def list_books_ui(self):
        print("********** \n")
        print_list = []
        self._book_service.list_books(print_list)
        self.display_list(print_list)
        print("\n ********** ")

    def list_ui(self):
        print("**********")
        print("1. List clients.")
        print("2. List books.")
        command = input("Enter your choice: ")
        if command == '1':
            self.list_clients_ui()
        elif command == '2':
            self.list_books_ui()
        else:
            raise ValueError("Invalid command.")

    def display_list(self, list):
        print("\n")
        for index in range(len(list)):
            print(list[index])
        print("\n")

    def update_client_ui(self):
        """
        One can update all of client's parameters: client_id, name
        The client the user wants to update the info for is found based on the client_data given
        If several clients have the same name, only the first occurrence is updated
        :return:
        """
        print("Input name or id of the client you want to update data for: ")
        client_data = input()
        print("Which data would you like to update?")
        print("1. Client's id")
        print("2. Client's name")
        update_id = input()
        if update_id == '2':
            print("Input updated client's name: ")
            update_info = input()
            self._client_service.update_client(client_data, update_info, update_id)
        elif update_id == '1':
            print("Input updated client's id of form first-name-letter-abcd where a,b,c,d are digits")
            update_info = input()
            self._client_service.update_client(client_data, update_info, update_id)
        else:
            raise ValueError("Invalid input...")


    def update_book_ui(self):
        """
        One can update all of a book's parameters: book_id, title, author
        The book the user wants to update the info for is found based on the book_data given
        If several books have the same author, only the first occurrence is updated
        If several books have the same title, only the first occurrence is updated
        :return:
        """
        print("Input id, title or author of the book you want to update data for: ")
        book_data = input()
        print("Which data would you like to update?")
        print("1. Book's id")
        print("2. Book's title")
        print("3. Author")
        update_id = input()
        if update_id == '1':
            print("Input updated book's id: ")
            update_info = input()
            self._book_service.update_book(book_data, update_info, update_id)
        elif update_id == '2':
            print("Input new title: ")
            update_info = input()
            self._book_service.update_book(book_data, update_info, update_id)
        elif update_id == '3':
            print("Input new author: ")
            update_info = input()
            self._book_service.update_book(book_data, update_info, update_id)
        else:
            raise ValueError("Invalid input...")


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


    def rent_ui(self):
        """
        A rental consists of a rental_id, book_id, client_id, rented_date, returned_date which is 1,1,1 as the book
        has just been rented, not returned
        :return:
        """
        returned_date = date(1,1,1)
        year = int(input("Input rental year: "))
        month = int(input("Input rental month: "))
        day = int(input("Input rental day: "))
        rental_date = date(year, month, day)
        book_data = input("Input title or id of rented book: ")
        book = self._book_service.get_book(book_data)
        client_data = input("Input id or name of the client's who's renting: ")
        client = self._client_service.get_client(client_data)
        rental_id = input("Input 4-digit rental id: ")
        self._rental_service.create_rental(rental_id, book.book_id, client.client_id, rental_date, returned_date)

    def return_ui(self):
        """

        :return:
        """
        rental_id = input("Please enter the rental's id: ")
        year = int(input("Input year of returning: "))
        month = int(input("Input month of returning: "))
        day = int(input("Input day of returning: "))
        returned_date = date(year, month, day)
        self._rental_service.close_rental(rental_id, returned_date)

    def list_rentals_ui(self):
        client_list = self._client_service.client_repo
        book_list = self._book_service.book_repo
        print_list = []
        print("********** \n")
        self._rental_service.list_rentals(print_list)
        for index in range(len(print_list)):
            rental = print_list[index]
            client_index = self._client_service.find_client(rental.client_id)
            client = client_list.clients[client_index]
            book_index = self._book_service.find_book(rental.book_id)
            book = book_list.books[book_index]
            print(rental.print_rental(client, book))
            print()
        print("\n**********")

    def search_books(self):
        search_list = []
        data = input("Enter book data: ")
        self._book_service.search_book(data, search_list)
        self.display_list(search_list)

    def search_clients(self):
        search_list = []
        data = input("Enter client data: ")
        self._client_service.search_client(data, search_list)
        self.display_list(search_list)

    def most_rented_books(self):
        book_list = self._book_service.book_repo.books
        results = self._rental_service.most_rented_books(book_list)
        self.display_list(results)

    def most_active_clients(self):
        client_list = self._client_service.client_repo.clients
        results = self._rental_service.most_active_clients(client_list)
        self.display_list(results)

    def most_rented_author(self):
        book_list = self._book_service.book_repo.books
        results = self._rental_service.most_rented_authors1(book_list)
        self.display_list(results)

    @staticmethod
    def rentals_menu():
        print("\n1.  Rent a book.")
        print("2.  Return a book.")
        print("3.  List rentals. \n")

    def manage_rentals(self):
        rental_dict = {'1': self.rent_ui, '2': self.return_ui, '3': self.list_rentals_ui}
        self.rentals_menu()
        rental = input("Choose an operation>> ")
        if rental in rental_dict:
            rental_dict[rental]()
        else:
            raise ValueError("Invalid Command! ")

    @staticmethod
    def statistics_menu():
        print("1. Display most rented books.")
        print("2. Display most active clients.")
        print("3. Display most rented author list.")

    def manage_statistics(self):
        statistics_dict = {'1': self.most_rented_books, '2':self.most_active_clients, '3':self.most_rented_author}
        self.statistics_menu()
        statistic = input("Choose an operation>> ")
        if statistic in statistics_dict:
            statistics_dict[statistic]()
        else:
            raise ValueError("Invalid Command! ")

    def undo_ui(self):
        self._undo_service.undo()

    def redo_ui(self):
        self._undo_service.redo()

    @staticmethod
    def print_main_menu():
        print("\n1.  Add a book or a client.")
        print("2.  Remove a book or a client.")
        print("3.  List books or clients.")
        print("4.  Update a book or a client.")
        print("5.  Manage rentals")
        print("6.  Search for a book in the list.")
        print("7.  Search for a client in the list.")
        print("8.  Manage statistics.")
        print("9.  Undo")
        print("10. Redo")
        print("11. Exit.\n")

    def menu(self):
        self._book_service.generate_list(10)
        self._client_service.generate_list(10)
        self._rental_service.generate_list()

        cmd_dict = {'1':self.add_ui, '2':self.remove_ui, '3':self.list_ui,'5': self.manage_rentals,'4':self.update_ui, '6': self.search_books,
                    '7':self.search_clients,'8': self.manage_statistics,'9':self.undo_ui, '10':self.redo_ui}
        is_it_over_yet = 0
        while not is_it_over_yet:
            self.print_main_menu()
            command = input("Enter your command>> ")
            if command in cmd_dict:
                try:
                    cmd_dict[command]()
                except (RentalException, RentalValidationException, BookException, BookValidationException, ClientException, ClientValidationException, ValueError) as e:
                    print(str(e))
            elif command == '11':
                is_it_over_yet = 1
                print("Come back soon")
            else:
                print("Invalid command")


if __name__ == '__main__':
    client_repo = ClientRepository()
    book_repo = BookRepository()
    rental_repo = RentalRepository()
    start = Ui(book_repo, client_repo, rental_repo)
    start.menu()