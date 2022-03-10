from random import randrange, choice
from domain.book import Book, BookValidator, BookValidationException, BookException

class BookRepository:
    def __init__(self):
        self._book_list = []

    def __len__(self):
        return len(self._book_list)

    @property
    def books(self):
        return self._book_list

    def get_last_book(self):
        return self._book_list[-1]

    def add_book(self, book):
        """
        Adds a book object to the list
        Things to look out for:
        ID already in the list
        :param book:
        :return:
        """
        self._book_list.append(book)
        return book

    def list_books(self, print_list):
        for index in range(len(self)):
            print_list.append(self._book_list[index])

    def remove_book(self, book):
        """
        One can remove a book from the list based on its id, title or author
        If several books have the same author, only the first occurrence is removed
        If several books have the same title, only the first occurrence is removed
        :param book: Book object to be removed
        :return: -
        """
        self._book_list.remove(book)

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
            self._book_list[book_index].book_id = update_info
        elif update_id == '2':
            book._book_id = book._book_id[:-1]
            book._book_id = book._book_id + update_info[0]
            book._title = update_info
            b1.validate(book)
            self._book_list[book_index].book_id = self._book_list[book_index].book_id[:-1]
            self._book_list[book_index].book_id = self._book_list[book_index].book_id + update_info[0]
            self._book_list[book_index].title = update_info
        elif update_id == '3':
            book._author = update_info
            b1.validate(book)
            self._book_list[book_index].author = update_info

    def find_book_index(self, book):
        """
        Find a book's position in the list
        :param book:
        :return:
        """
        for index in range(len(self._book_list)):
            b1 = self._book_list[index]
            if b1.book_id == book.book_id:
                return index

    def generate_list(self, length):

        title = ['A Court of Thorns and Roses','The Last Wish','Sword of Destiny','Good Omens','Time of Contempt','A Court of Mist and Fury'
                 ,'A Court of Wings and Ruin',"The Queen's Rising",'Lady of the Lake','Harry Potter and the Prisoner of Azkaban','The Year After You'
                 ,'Hold Still','All the Bright Places',"Since you've been gone","Serpent&Dove","The Hate U Give",'My Heart and Other Black Holes','The Astonishing Colour of After']
        author = ["Sarah J. Maas","Morgan Matson","Andrzej Sapkowski","Nina de Pass","J.K.Rowling","Jennifer Niven","Rebecca Ross","Nina Lacour","Angie Thomas"
                  ,"Neil Gaiman",'Jasmine Warga','Emily X.R. Pan']

        for i in range(length):
            id_ = str(randrange(1000, 9999))
            book_title = choice(title)
            id_ = id_ + book_title[0]
            book_author = choice(author)
            book = Book(id_, book_title, book_author)
            self.add_book(book)

