"""
    Entity class should be coded here
    Entity class -> Student
"""


class StudentException(Exception):
    def __init__(self, message):
        self._message = message


class Student:
    """
    Represent a student identified by name, id and group
    """
    def __init__(self, id_, name, group):
        """
        Create student
        :param id_: ID - integer in [0,1000]
        :param name: Name given as a string
        :param group: Group - integer in [100,120]
        """
        if group < 100 or group > 120:
            raise StudentException("Invalid group number!")

        if id_ < 0 or id_ > 1000:
            raise StudentException("Id should be an integer in [0,1000)")

        l = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for index in range(len(l)):
            if l[index] in name:
                raise StudentException("Name should be a string! ")

        self._id = id_
        self._name = name
        self._group = group

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        if value < 100 and value > 120:
            raise ValueError("Invalid group number")
        self._group = value

    def __str__(self):
        return str(self._id).rjust(4) +'. '+ str(self._name).ljust(20).rjust(5) + ' ;Group ' + str(self._group)

    def __eq__(self, other):
        if not isinstance(other, Student):
            raise TypeError('Cannot compare Student to ' + str(type(other)))
        #Checking whether two students have the same id
        return self.id == other.id


def test_student():
    student1 = Student(911, 'Park', 120)
    student2 = Student(913, 'John', 101)
    assert student1.name == 'Park' and student1.id == 911 and student1.group == 120
    assert student2.name == 'John' and student2.id == 913 and student2.group == 101

    #Student with non-existent group
    try:
        student3 = Student(102, 'Sasha', 203)
        assert False
    except StudentException:
        assert True

    #Student with invalid id
    try:
        student4 = Student(2045, 'Danny', 120)
        assert False
    except StudentException:
        assert True

    #Student with invalid name
    try:
        student5 = Student(134, 'Amanda355', 103)
        assert False
    except StudentException:
        assert True