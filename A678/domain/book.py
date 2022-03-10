"""
Book entity is declared here
Convention:
book_id: 4 digits code and letter -first letter from title
Author is a string of letters
For a book, only the author and the title can be updated
"""
class BookException(Exception):
    def __init__(self, msg = ''):
        self._msg = msg

class BookValidationException(BookException):
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

class Book:
    def __init__(self, book_id, title, author):
        self._book_id = book_id
        self._title = title
        self._author = author

    def __str__(self):
        return str(self._book_id).rjust(2) + ': ' + str(self._title).rjust(5) +' by ' + str(self._author).ljust(3)

    @property
    def book_id(self):
        return self._book_id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @book_id.setter
    def book_id(self, value):
        self._book_id = value

    @title.setter
    def title(self, value):
        self._title = value

    @author.setter
    def author(self, value):
        self._author = value


class BookValidator:
    def validate(self, book):
        """
        Validate the input data for a given book object
        :param book: -
        :return: -
        """
        errors = []
        if self.validate_id(book.book_id, book.title) == 0:
                errors.append("Invalid book id provided. Input id of form abcd_first_title_letter, where a,b,c,d are digits.")
        if len(book._title) == 0 or book.title == ' ':
            errors.append("Invalid title, what's the book about?")
        if len(book._author) == 0 or book.author == ' ':
            errors.append("Invalid author, someone actually wrote this book!")
        l = ['1', '2', '3', '4', '5', '6', '7', '8', '9','0']
        for index in range(len(l)):
            if l[index] in book.author:
                errors.append("Name should only contain letters!")
        if len(errors) != 0:
            raise BookValidationException(errors)

    def validate_id(self, id_, title):
        """
        book_id: 4 digits code and letter -first letter from title
        :param id_:
        :param title:
        :return:
        """
        fr = 0
        tmp_id = id_[:-1]
        if len(title) > 0:
            if len(id_) != 5 or id_[-1].lower() != title[0].lower():
                return 0

