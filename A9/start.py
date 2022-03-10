import sys

from PyQt5.QtWidgets import QApplication

from domain.settings import Settings
from repository.big_repo import ClientRepository, BookRepository, RentalRepository
from repository.binary_file_repo import BookBinaryRepository, ClientBinaryRepository, RentalBinaryRepository
from repository.json_repo import BookJSONRepository, ClientJSONRepository, RentalJSONRepository
from repository.text_repo import BookTextRepository, ClientTextRepository, RentalTextRepository
from service.big_service import RentalService, ClientService, BookService
from service.undo_service import UndoService
from ui.console_gui import GUi
from ui.gui import LibraryUi
from ui.menu_ui import Ui


class Start:
    def __init__(self):
        self._commands = Settings()
        cmd_dict = self._commands.file_parse()
        if cmd_dict['ui'].lower() == 'menu_ui':
            if cmd_dict['repository'].lower() == 'inmemory':
                client_repo = ClientRepository()
                client_repo.generate_list(10)
                book_repo = BookRepository()
                book_repo.generate_list(10)
                rental_repo = RentalRepository()
                rental_repo.generate_rentals(client_repo, book_repo)
                start = Ui(book_repo, client_repo, rental_repo)
                start.menu()
            elif cmd_dict['repository'].lower() == 'textfiles':
                client_repo = ClientTextRepository(cmd_dict['clients'])
                book_repo = BookTextRepository(cmd_dict['books'])
                rental_repo = RentalTextRepository(cmd_dict['rentals'])
                start = Ui(book_repo, client_repo, rental_repo)
                start.menu()
            elif cmd_dict['repository'].lower() == 'binaryfiles':
                client_repo = ClientBinaryRepository(cmd_dict['clients'])
                book_repo = BookBinaryRepository(cmd_dict['books'])
                rental_repo = RentalBinaryRepository(cmd_dict['rentals'])
                start = Ui(book_repo, client_repo, rental_repo)
                start.menu()
            elif cmd_dict['repository'].lower() == 'jsonfiles':
                client_repo = ClientJSONRepository(cmd_dict['clients'])
                book_repo = BookJSONRepository(cmd_dict['books'])
                rental_repo = RentalJSONRepository(cmd_dict['rentals'])
                start = Ui(book_repo, client_repo, rental_repo)
                start.menu()
        elif cmd_dict['ui'] == 'GUI':
            if cmd_dict['repository'].lower() == 'inmemory':
                client_repo = ClientRepository()
                client_repo.generate_list(10)
                book_repo = BookRepository()
                book_repo.generate_list(10)
                rental_repo = RentalRepository()
                rental_repo.generate_rentals(client_repo, book_repo)
                undo_service = UndoService()
                rental_service = RentalService(rental_repo, book_repo, client_repo, undo_service)
                client_service = ClientService(client_repo, rental_service, undo_service)
                book_service = BookService(book_repo, rental_service, undo_service)
                app = GUi(book_service, client_service, rental_service, undo_service)
                mv = QApplication(sys.argv)
                view = LibraryUi(app)
                view.show()
                sys.exit(mv.exec_())
            elif cmd_dict['repository'] == 'textfiles':
                client_repo = ClientTextRepository(cmd_dict['clients'])
                book_repo = BookTextRepository(cmd_dict['books'])
                rental_repo = RentalTextRepository(cmd_dict['rentals'])
                undo_service = UndoService()
                rental_service = RentalService(rental_repo, book_repo, client_repo, undo_service)
                client_service = ClientService(client_repo, rental_service, undo_service)
                book_service = BookService(book_repo, rental_service, undo_service)
                app = GUi(book_service, client_service, rental_service, undo_service)
                mv = QApplication(sys.argv)
                view = LibraryUi(app)
                view.show()
                sys.exit(mv.exec_())
            elif cmd_dict['repository'] == 'binaryfiles':
                client_repo = ClientBinaryRepository(cmd_dict['clients'])
                book_repo = BookBinaryRepository(cmd_dict['books'])
                rental_repo = RentalBinaryRepository(cmd_dict['rentals'])
                undo_service = UndoService()
                rental_service = RentalService(rental_repo, book_repo, client_repo, undo_service)
                client_service = ClientService(client_repo, rental_service, undo_service)
                book_service = BookService(book_repo, rental_service, undo_service)
                app = GUi(book_service, client_service, rental_service, undo_service)
                mv = QApplication(sys.argv)
                view = LibraryUi(app)
                view.show()
                sys.exit(mv.exec_())
            elif cmd_dict['repository'] == 'jsonfiles':
                client_repo = ClientJSONRepository(cmd_dict['clients'])
                book_repo = BookJSONRepository(cmd_dict['books'])
                rental_repo = RentalJSONRepository(cmd_dict['rentals'])
                undo_service = UndoService()
                rental_service = RentalService(rental_repo, book_repo, client_repo, undo_service)
                client_service = ClientService(client_repo, rental_service, undo_service)
                book_service = BookService(book_repo, rental_service, undo_service)
                app = GUi(book_service, client_service, rental_service, undo_service)
                mv = QApplication(sys.argv)
                view = LibraryUi(app)
                view.show()
                sys.exit(mv.exec_())


if __name__ == '__main__':
    start_menu = Start()

