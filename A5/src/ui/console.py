"""
    UI class.

    Calls between program modules
    ui -> service -> entity
    ui -> entity
"""
from src.services.service import Service, test_add
from src.domain.entity import Student, StudentException, test_student


class Ui:
    def __init__(self):
        self._student_list = Service()
        self._operation_list = []

    def add_student_ui(self):
        """
        Add a student to the list
        :return: -
        """
        id_ = input("Give an id between 0 and 1000: ")
        name = input("Enter student's name: ")
        group = input("Choose a group from 100 to 120: ")
        self._student_list.add_student(Student(int(id_), name, int(group)))

    def display_list_ui(self):
        """
        Display the list of students
        :return: -
        """
        final_list = []
        print("-------")
        self._student_list.display_list(final_list)
        for stud in final_list:
            print(stud)
        print("-------")

    def filter_list_ui(self):
        """
        Deletes the students from a given group
        :return:
        """
        group = input("Please enter a group number between 100 and 120: ")
        self._student_list.filter_list(int(group))

    def undo_ui(self):
        """
        Undo the last operations that modifies the list
        :return:
        """
        self._student_list.undo(self._operation_list)

    @staticmethod
    def print_menu():
        print("**********")
        print("1. Add a student")
        print("2. Display the list of students")
        print("3. Filter the list so that students from a given group are deleted")
        print("4. Undo")
        print("5. Exit")
        print("**********")

    def add_operation_ui(self):
        """
        Add an operation to the list (the list modified after a certain operation)
        :return:
        """
        self._student_list.add_operation(self._operation_list)

    def start(self):
        self._student_list.generate_list()
        #we add the first version of the student list to the operation list so that we don't lose it
        self.add_operation_ui()
        is_it_over_yet = False
        cmd_dict = {'1': self.add_student_ui, '2': self.display_list_ui, '3': self.filter_list_ui, '4': self.undo_ui}

        while not is_it_over_yet:
            self.print_menu()
            cmd = input("Enter an option: ")
            if cmd in cmd_dict:
                try:
                    cmd_dict[cmd]()
                    if cmd in {'1', '3'}:
                        self.add_operation_ui()
                except StudentException as studstr:
                    print(str(studstr))
            elif cmd == '5':
                is_it_over_yet = True
                print("Come back soon! ")
            else:
                print("Invalid command")


if __name__ == '__main__':
    test_student()
    test_add()
    start = Ui()
    start.start()
