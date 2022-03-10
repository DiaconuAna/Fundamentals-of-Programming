
# Import QApplication and the required widgets from PyQt5.QtWidgets
from datetime import date

from PyQt5.QtWidgets import QTextEdit, QGroupBox, QTextBrowser, QInputDialog
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

import sys

from domain.book import BookException, BookValidationException
from domain.client import ClientException, ClientValidationException
from domain.rental import RentalException, RentalValidationException
from repository.big_repo import ClientRepository, RentalRepository, BookRepository
from repository.text_repo import BookTextRepository, ClientTextRepository
from service.big_service import RentalService, ClientService, BookService
from service.undo_service import UndoService
from ui.console_gui import GUi


class AddWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('Add a client.')
        b2 = QPushButton('Add a book.')
        self.box = QGroupBox('Output>>')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.create_layout(b1, b2)
        b1.clicked.connect(self.add_client)
        b2.clicked.connect(self.add_book)

    def create_layout(self, b1, b2):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def add_client(self):
        try:
            client_id, result = QInputDialog.getText(self, "Input Dialog", "Enter 4-digit client id: ")
            if result:
                name, result1 = QInputDialog.getText(self, "Input Dialog", "Enter client's name: ")
                if result1:
                    self.ui.add_client(client_id, name)
        except (ClientException, ClientValidationException) as clexc:
            self.output.append(str(clexc))

    def add_book(self):
        try:
            book_id, result = QInputDialog.getText(self,"Input Dialog", "Enter 4-digit book id: ")
            if result:
                title, res1 = QInputDialog.getText(self, "Input Dialog", "Enter book's title: ")
                if res1:
                    author, res2 = QInputDialog.getText(self, "Input Dialog", "Enter book's author: ")
                    if res2:
                        self.ui.add_book(book_id, title, author)
        except (BookException, BookValidationException) as bookexc:
            self.output.append(str(bookexc))


class ListWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('List clients.')
        b2 = QPushButton('List books.')
        self.box = QGroupBox('Output>>')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.create_layout(b1, b2)
        b1.clicked.connect(self.list_clients)
        b2.clicked.connect(self.list_books)

    def create_layout(self, b1, b2):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def list_clients(self):
        print_list = self.ui.list_clients_ui()
        for client in print_list:
            self.output.append(str(client))
        self.output.append("\n*********\n")

    def list_books(self):
        print_list = self.ui.list_books_ui()
        for book in print_list:
            self.output.append(str(book))
        self.output.append("\n*********\n")


class RentalWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('Rent a book.')
        b2 = QPushButton('Return a book.')
        b3 = QPushButton("List rentals")
        self.box = QGroupBox('Output>>')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.create_layout(b1, b2, b3)
        b1.clicked.connect(self.rent)
        b2.clicked.connect(self.return_book)
        b3.clicked.connect(self.list_rentals)

    def create_layout(self, b1, b2, b3):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(b3)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def rent(self):
        try:
            year, r1 = QInputDialog.getInt(self, "Input Dialog", "Enter year: ")
            if r1:
                month, r2 = QInputDialog.getInt(self, "Input Dialog", "Enter month: ")
                if r2:
                    day, r3 = QInputDialog.getInt(self, "Input Dialog", "Enter day: ")
                    if r3:
                        rent_date = date(year, month, day)
                        cl_data, r4 = QInputDialog.getText(self, "Input Dialog", "Enter client data: ")
                        if r4:
                            b_data, r5 = QInputDialog.getText(self, "Input Dialog", "Enter book data: ")
                            if r5:
                                rent_id, r6 = QInputDialog.getText(self, "Input Dialog", "Enter 4-digit rental id: ")
                                if r6:
                                    self.ui.rent_ui(rent_date, b_data, cl_data, rent_id)
        except(RentalException, RentalValidationException) as rexc:
            self.output.append(str(rexc))

    def return_book(self):
        try:
            r_id, r1 = QInputDialog.getText(self, "Input Dialog", "Enter rental id: ")
            if r1:
                year, r2 = QInputDialog.getInt(self, "Input Dialog", "Enter returning year: ")
                if r2:
                    month, r3 = QInputDialog.getInt(self, "Input Dialog", "Enter returning month: ")
                    if r3:
                        day, r4 = QInputDialog.getInt(self, "Input Dialog", "Enter returning day: ")
                        if r4:
                            ret_date = date(year, month, day)
                            self.ui.return_ui(r_id, ret_date)
        except(RentalException, RentalValidationException) as rexc:
            self.output.append(str(rexc))

    def list_rentals(self):
            print_list = self.ui.list_rentals_ui()
            for rental in print_list:
                self.output.append(str(rental))
            self.output.append("\n*********\n")


class RemoveWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('Remove a client.')
        b2 = QPushButton('Remove a book.')
        self.box = QGroupBox('Output>>')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.create_layout(b1, b2)
        b1.clicked.connect(self.remove_client)
        b2.clicked.connect(self.remove_book)

    def create_layout(self, b1, b2):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def remove_client(self):
        try:
            removal_data, res = QInputDialog.getText(self, "Input Dialog", "Enter removal data: ")
            if res:
                self.ui.remove_client_ui(removal_data)
        except (ClientException, ClientValidationException) as clexc:
            self.output.append(str(clexc))

    def remove_book(self):
        try:
            removal_data, res = QInputDialog.getText(self, "Input Dialog", "Enter removal data: ")
            if res:
                self.ui.remove_book_ui(removal_data)
        except (BookException, BookValidationException) as bookexc:
            self.output.append(str(bookexc))

class UpdateClientWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('Update name.')
        b2 = QPushButton('Update id.')
        self.box = QGroupBox('Output>>')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.create_layout(b1, b2)
        b1.clicked.connect(self.update_name)
        b2.clicked.connect(self.update_id)

    def create_layout(self, b1, b2):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def update_name(self):
        try:
            id_data, res = QInputDialog.getText(self, "Input Dialog", "Enter identification data: ")
            if res:
                name, res1 = QInputDialog.getText(self, "Input Dialog", "Enter new name: ")
                if res1:
                    self.ui.update_client_ui(id_data, name, '2')
        except (ClientException,ClientValidationException) as ec:
            self.output.append(str(ec))

    def update_id(self):
        try:
            id_data, res = QInputDialog.getText(self, "Input Dialog", "Enter identification data: ")
            if res:
                cl_id, res1 = QInputDialog.getText(self, "Input Dialog", "Enter new id: ")
                if res1:
                    self.ui.update_client_ui(id_data, cl_id, '1')
        except (ClientException,ClientValidationException) as ec:
            self.output.append(str(ec))


class UpdateBookWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('Update id.')
        b2 = QPushButton('Update title.')
        b3 = QPushButton("Update author.")
        self.box = QGroupBox('Output>>')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.create_layout(b1, b2, b3)
        b1.clicked.connect(self.update_id)
        b2.clicked.connect(self.update_title)
        b3.clicked.connect(self.update_author)

    def create_layout(self, b1, b2, b3):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(b3)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def update_id(self):
        try:
            id_data, res = QInputDialog.getText(self, "Input Dialog", "Enter identification data: ")
            if res:
                b_id, res1 = QInputDialog.getText(self, "Input Dialog", "Enter new id: ")
                if res1:
                    self.ui.update_book_ui(id_data,b_id,'1')
        except (BookException, BookValidationException) as ec:
            self.output.append(str(ec))

    def update_title(self):
        try:
            id_data, res = QInputDialog.getText(self, "Input Dialog", "Enter identification data: ")
            if res:
                title, res1 = QInputDialog.getText(self, "Input Dialog", "Enter new title: ")
                if res1:
                    self.ui.update_book_ui(id_data, title, '2')
        except (BookException, BookValidationException) as ec:
            self.output.append(str(ec))

    def update_author(self):
        try:
            id_data, res = QInputDialog.getText(self, "Input Dialog", "Enter identification data: ")
            if res:
                author, res1 = QInputDialog.getText(self, "Input Dialog", "Enter new author: ")
                if res1:
                    self.ui.update_book_ui(id_data, author, '3')
        except (BookException, BookValidationException) as ec:
            self.output.append(str(ec))


class UpdateWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('Update a client.')
        b2 = QPushButton('Update a book.')
        self.box = QGroupBox('Output>>')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.create_layout(b1, b2)
        b1.clicked.connect(self.update_client)
        b2.clicked.connect(self.update_book)

    def create_layout(self, b1, b2):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def update_client(self):
        self.box.hide()
        self.window = UpdateClientWindow(self.ui)
        self.window.show()

    def update_book(self):
        self.box.hide()
        self.window = UpdateBookWindow(self.ui)
        self.window.show()

class SearchWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('Search for a client.')
        b2 = QPushButton('Search for a book.')
        self.box = QGroupBox('Output>>')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.create_layout(b1, b2)
        b1.clicked.connect(self.search_client)
        b2.clicked.connect(self.search_book)

    def create_layout(self, b1, b2):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def search_client(self):
        try:
            data, r1 = QInputDialog.getText(self, "Input Dialog", "Enter client data: ")
            if r1:
                print_list = self.ui.search_clients(data)
                for client in print_list:
                    self.output.append(str(client))
                self.output.append("\n*******\n")
        except (ClientException, ClientValidationException) as ec:
            self.output.append(str(ec))

    def search_book(self):
        try:
            data, r1 = QInputDialog.getText(self, "Input Dialog", "Enter book data: ")
            if r1:
                print_list = self.ui.search_books(data)
                for book in print_list:
                    self.output.append(str(book))
                self.output.append("\n*******\n")
        except (BookException, BookValidationException) as ec:
            self.output.append(str(ec))


class StatisticsWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('Most rented books.')
        b2 = QPushButton('Most active clients.')
        b3 = QPushButton("Most rented authors.")
        self.box = QGroupBox('Output>>')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(10, 90, 331, 111))
        self.create_layout(b1, b2, b3)
        b1.clicked.connect(self.most_rented_books)
        b2.clicked.connect(self.most_active_clients)
        b3.clicked.connect(self.most_rented_authors)

    def create_layout(self, b1, b2, b3):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(b3)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def most_rented_books(self):
        print_list = self.ui.most_rented_books()
        for book in print_list:
            self.output.append(str(book))
        self.output.append('\n******\n')

    def most_active_clients(self):
        print_list = self.ui.most_active_clients()
        for client in print_list:
            self.output.append(str(client))
        self.output.append('\n******\n')

    def most_rented_authors(self):
        print_list = self.ui.most_rented_author()
        for author in print_list:
            self.output.append(str(author))
        self.output.append('\n******\n')



class UndoRedoWindow(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        b1 = QPushButton('Undo.')
        b2 = QPushButton('Redo.')
        self.box = QGroupBox('Output>>')
        self.output = QTextBrowser(self.box)
        self.output.setGeometry(QtCore.QRect(20, 100, 360, 160))
        self.create_layout(b1, b2)
        b1.clicked.connect(self.undo)
        b2.clicked.connect(self.redo)

    def create_layout(self, b1, b2):
        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(self.box)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def undo(self):
        try:
            self.ui.undo_ui()
            self.output.append("Succesful undo! :)")
        except ValueError as err:
            self.output.append(str(err))

    def redo(self):
        try:
            self.ui.redo_ui()
            self.output.append("Succesful redo! :)")
        except ValueError as err:
            self.output.append(str(err))


class LibraryUi(QMainWindow):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.setWindowTitle('Cozy Corner Library')
        self.setFixedSize(1000, 500)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        b1 = QPushButton('Add book or client.')
        b2 = QPushButton("List books or clients.")
        b3 = QPushButton("Remove clients or books.")
        b4 = QPushButton("Update clients or books.")
        b5 = QPushButton("Manage rentals")
        b6 = QPushButton("Search for a client or a book.")
        b7 = QPushButton("Manage statistics.")
        b8 = QPushButton("Undo/Redo.")
        b9 = QPushButton("Exit")
        self.box = QTextEdit('Output', self._centralWidget)
        self.box.hide()
        self.create_layout(b1, b2, b3, b4, b5, b6, b7, b8, b9)
        b1.clicked.connect(self.add)
        b2.clicked.connect(self.list)
        b3.clicked.connect(self.remove)
        b4.clicked.connect(self.update)
        b5.clicked.connect(self.rentals)
        b6.clicked.connect(self.search)
        b7.clicked.connect(self.statistics)
        b8.clicked.connect(self.undo_redo)
        b9.clicked.connect(self.close_app)

    def create_layout(self, b1, b2, b3, b4, b5, b6, b7, b8, b9):
        generalL = QVBoxLayout()
        generalL.addWidget(b1)
        generalL.addWidget(b2)
        generalL.addWidget(b3)
        generalL.addWidget(b4)
        generalL.addWidget(b5)
        generalL.addWidget(b6)
        generalL.addWidget(b7)
        generalL.addWidget(b8)
        generalL.addWidget(b9)
        generalL.addWidget(self.box)
        self._centralWidget.setLayout(generalL)

    def add(self):
        self.box.hide()
        self.w = AddWindow(self.ui)
        self.w.show()

    def list(self):
        self.box.hide()
        self.w = ListWindow(self.ui)
        self.w.show()

    def remove(self):
        self.box.hide()
        self.w = RemoveWindow(self.ui)
        self.w.show()

    def update(self):
        self.box.hide()
        self.w = UpdateWindow(self.ui)
        self.w.show()

    def rentals(self):
        self.box.hide()
        self.w = RentalWindow(self.ui)
        self.w.show()

    def search(self):
        self.box.hide()
        self.w = SearchWindow(self.ui)
        self.w.show()

    def statistics(self):
        self.box.hide()
        self.w = StatisticsWindow(self.ui)
        self.w.show()

    def undo_redo(self):
        self.box.hide()
        self.w = UndoRedoWindow(self.ui)
        self.w.show()

    def close_app(self):
        self.close()


