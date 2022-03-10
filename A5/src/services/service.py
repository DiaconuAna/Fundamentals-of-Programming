"""
    Service class includes functionalities for implementing program features
    1. Add a student
    2. Display the list of students
    3. Filter the list so that students in a given group are deleted from the list
    4. Undo the last operation that modified the program data
"""
from random import randrange, choice
from src.domain.entity import Student, StudentException
import copy


class Service:
    def __init__(self):
        self._students_list = []

    def add_student(self, student):
        """
        Add a new student to the list
        :param student: Student to be added
        :return:
        """

        if student in self._students_list:
            raise StudentException("Student already in the list")

        for s in range(len(self._students_list)):
            #2 students cannot have the same id
            stud = self._students_list[s]
            if int(student._id) == int(stud._id):
                raise StudentException("Two students cannot have the same id")

        self._students_list.append(student)

    def __len__(self):
        return len(self._students_list)

    def display_list(self,final_list):
        """
        Display the student list
        :return:
        """
        for stud in self._students_list:
            final_list.append(stud)

    def filter_list(self, group):
        """
        Filter the list so that the students in a given group are deleted from the list
        :param group: Given group
        :return: -
        """
        if len(self._students_list) == 0:
            raise StudentException("Student list is empty!")

        aux = 0

        if group < 100 or group > 120:
            raise StudentException("Invalid group number!")

        list_length = len(self._students_list)
        index = 0

        while index < list_length:
            student = self._students_list[index]
            if student._group == group:
                self._students_list.pop(index)
                list_length = len(self._students_list)
                aux += 1
            else:
                index += 1

        if aux == 0:
            raise StudentException("There are no students in given group!")

    def add_operation(self, op_list):
        aux_list = copy.deepcopy(self._students_list)
        op_list.append(aux_list)

    def undo(self, operation_list):
        if len(operation_list) <= 1:
            raise StudentException("No more undos")

        operation_list.pop()
        self._students_list.clear()
        self._students_list.extend(operation_list[-1])

    def generate_list(self):
        first_name = ['Anna', 'Linda', 'Chloe', 'Jackson', 'Bill', 'John', 'Sarah', 'Jordan', 'Rose', 'Strip', 'Sasha', 'Aliona', 'Michael', 'Nathan', 'Brian', 'Frances', 'Leah', 'Fred', 'George', 'Harry', 'Jane']
        last_name = ['Larson', 'McLachlan', 'Smith', 'Jefferson', 'Goodwin', 'Harding', 'Price', 'White', 'Johnson', 'Kay', 'Harper', 'Thomson', 'Gardner', 'Dean', 'Hamilton', 'Murray']

        for i in range(10):
            id_ = randrange(1, 1000)
            group = randrange(100, 120)
            name = choice(first_name) + ' ' + choice(last_name)
            student1 = Student(int(id_), name, int(group))
            try:
                self.add_student(student1)
            except StudentException:
                i -= 1
                continue


def test_add():
    studlist = Service()
    assert len(studlist) == 0

    studlist.add_student(Student(103, 'Anna Park', 103))
    assert len(studlist) == 1

    studlist.add_student(Student(456, 'John Doe', 104))
    assert len(studlist) == 2

    #try to add a student that's already in the list
    try:
        studlist.add_student(Student(456, 'John Doe', 104))
        assert False
    except StudentException:
        assert True

    assert len(studlist) == 2

    #try to add a student whose id's already in use

    try:
        studlist.add_student(Student(103, 'Jordan Mitch', 109))
        assert False
    except StudentException:
        assert True

    assert len(studlist) == 2

    studlist.add_student(Student(752, 'Elizabeth Tuktik', 115))
    assert len(studlist) == 3

    studlist.add_student(Student(837, 'Michael Chen', 109))
    assert len(studlist) == 4