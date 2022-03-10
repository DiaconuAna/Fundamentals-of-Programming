#
# Write the implementation for A2 in this file
#

"""
Problem Statement
Implement a menu-driven console application that provides the following functionalities:
1. Read a list of complex numbers (in `z = a + bi` form) from the console.
  *I considered a and b as integers for aesthetic purposes*
2. Display the entire list of numbers on the console.
3. Display on the console the longest sequence of numbers having the same modulus
4. Display on the console the longest sequence of numbers having increasing modulus (I did stricly increasing here)
*the application displays the first sequence of maximum length*
5. Exit the application.
"""


# UI section
# (write all functions that have input or print statements here).
# Ideally, this section should not contain any calculations relevant to program functionalities




def read_number():
    """
    Reads real and imaginary number parts from the console
    :return:
    """
    number = input("Enter your complex number of form z=a+bi: ")
    return create_complex_number(number)


def add_number_ui(number_list):
    """
    Adds a new complex number to the list
    :return: -
    """
    number = read_number()
    if number is None:
        print("Invalid input. Please enter a valid number!")
        return 0
    else:
        number_list.append(number)
        return 1


def add_list_of_numbers_ui(number_list):
    """
    Add a number of numbers to the number list
    :param number_list: the list of complex numbers
    :return: -
    """
    number = number_of_numbers_to_be_added()
    for index in range(number):
       ok = add_number_ui(number_list)
       while (ok==0):
           ok = add_number_ui(number_list)

def number_of_numbers_to_be_added():
    """
    Number of numbers the user wants to add to the list
    :return: the above-mentioned number
    """
    print("How many numbers do you want to add to the list?")
    return int(input())

def display_list_of_numbers(number_list):
    """
    Shows the list of complex numbers
    :param number_list: list of complex numbers
    :return: -
    """
    for number in range(len(number_list)):
        print(to_str(number_list[number]))


def display_sequence_of_numbers(number_list, option):
    """
    Displays the longest sequence of numbers with the given property
    :param number_list: list of complex numbers
    :param option: indicates the given property
    :return: -
    """
    command_dict = {'3': longest_seq_equal_mod, '4': longest_seq_increasing_mod}
    x = command_dict[option]()
    lengthmax = length_of_longest_seq(number_list, x)
    first_el_index = first_element_of_longest_seq(number_list, lengthmax, x)
    last_el_index = first_el_index+lengthmax
    for index in range(first_el_index, last_el_index):
        print(to_str(number_list[index]))


def print_menu():
    """
    Prints the menu of the app
    :return:
    """
    print("1. Read a list of complex numbers")
    print("2. Display current list of complex numbers")
    print("3. Display longest sequence of complex numbers having the same modulus")
    print("4. Display longest sequence of complex numbers having increasing modulus")
    print("5. Exit")


def start():
    """
    Main menu of the application
    Steps:
    1. Print menu
    2. Input options
    3. Processing given options
    :return:
    """
    command_dict = {'1': add_list_of_numbers_ui, '2': display_list_of_numbers, '3': longest_seq_equal_mod, '4': longest_seq_increasing_mod}
    number_list = []
    list_init(number_list)
    number = 0
    over = False
    while not over:
        print_menu()
        command = input("Enter command: ")
        if command == '5':
            over = True
            print("Goodbye!")
        elif command not in command_dict:
            print("Invalid command. Please enter a valid command!")
        elif command == '2':
            display_list_of_numbers(number_list)
        elif command == '1':
             add_list_of_numbers_ui(number_list)
        else:
            display_sequence_of_numbers(number_list, command)


# Function section
# (write all non-UI functions in this section)
# There should be no print or input statements below this comment
# Each function should do one thing only
# Functions communicate using input parameters and their return values


def create_complex_number(number):
    """
    Create a complex number based on a string
    :param number: complex number given as a string
    :return: The complex number
    """
    index = 0
    real_part = 0
    imaginary_part = 0
    sign = 1
    if number[index] == '-':
        sign = -1
        index = 1


    while index < len(number) and number[index] >= '0' and number[index] <= '9':
        real_part = real_part*10 + int(number[index])
        index = index+1
    real_part = real_part*sign

    if index>=len(number):
        imaginary_part=0
    else:
        if number[index] == 'i':
            if index == 1 and number[0]=='-': imaginary_part = -1
            elif index == 0: imaginary_part = 1
            else:
                imaginary_part = real_part
            real_part = 0
        elif number[index] == '-':
                sign = -1
                index = index + 1
                p10 = 1
                while (index < len(number) and number[index] >= '0' and number[index] <= '9'):
                    imaginary_part = imaginary_part * 10 + int(number[index])
                    index = index + 1
                if imaginary_part==0:
                    imaginary_part=sign
                else:
                    imaginary_part = imaginary_part * sign
        elif number[index] == '+':
                sign = 1
                index = index + 1
                p10 = 1
                while (index< len(number) and number[index] >= '0' and number[index] <= '9'):
                    imaginary_part = imaginary_part*10 + int(number[index])
                    index = index + 1
                if imaginary_part==0:
                    imaginary_part=sign
                else:
                    imaginary_part = imaginary_part*sign
        else:
            return None

    validinputs=["0","1","2","3","4","5","6","7","8","9","i"]


    if number[len(number)-1] not in validinputs:
        return None

    if imaginary_part!=0 and number[len(number)-1]!='i':
        return None

    return {'Re': real_part, 'Im': imaginary_part}


def get_real_part(number):
    """
    Return the number's real part
    :param number: -
    :return: -
    """
    return number['Re']


def get_imaginary_part(number):
    """
    Return the number's imaginary part
    :param number: -
    :return: -
    """
    return number['Im']

def set_number_value(number,x):
    """

    :param number:
    :param x:
    :return:
    """
    number=x

def modulus(number):
    """
    Calculates the square of the modulus of a complex number
    :param number: the complex number
    :return: modulus of the number
    """
    real = get_real_part(number)
    imaginary = get_imaginary_part(number)
    """
    import cmath
    modulus=cmath.sqrt(real*real+imaginary*imaginary)
    """
    mod = real*real+imaginary*imaginary
    return mod



def to_str(number):
    """
    Return the string representing the complex number
    :param number: -
    :return: -
    """

    if get_real_part(number) == 0:
        if get_imaginary_part(number) == 0:
            return str(0)
        else :
            return str(get_imaginary_part(number))+"i"
    elif get_imaginary_part(number) == 0:
        return str(get_real_part(number))
    elif get_imaginary_part(number) > 0:
        return str(get_real_part(number)) + "+" + str(get_imaginary_part(number)) + "i"
    else:
        return str(get_real_part(number)) + str(get_imaginary_part(number)) + "i"



def maximum(number1, number2):
    """
    Returns max(number1,number2)
    :param number1: -
    :param number2: -
    :return: the bigger number
    """
    if number1 > number2:
        return number1
    else:
        return number2


def equal_modulus_check(number, number_list):
    """
    Checks whether two consecutive numbers have the same modulus
    :param number: index of current number in the list
    :param number_list: list of complex numbers
    :return: 1 if equal, 0 otherwise
    """
    if number+1 < len(number_list) and modulus(number_list[number]) == modulus(number_list[number+1]):
        return 1
    else:
        return 0


def increasing_modulus_check(number, number_list):
    """
    Checks whether two consecutive numbers from the list have increasing modulus
    :param number: index of current number in the list
    :param number_list: list of complex numbers
    :return: 1 if true, else 0
    """
    if number+1 < len(number_list) and modulus(number_list[number]) < modulus(number_list[number+1]):
        return 1
    else:
        return 0


def calculate_length(number_list, number, option):
    """
    Calculates the length of a sequence with a given property, starting from the element with the index 'number'
    :param number_list: list of complex numbers
    :param number: index of the first number from the sequence
    :param option: represents the given property
    :return: length of the sequence
    """
    '''marking the first element of the sequence'''
    length = 1
    command_dict = {'1': equal_modulus_check, '2': increasing_modulus_check}
    x = command_dict[option](number, number_list)
    while x != 0:
        length = length + 1
        number = number + 1
        x = command_dict[option](number, number_list)
    return length


def length_of_longest_seq(number_list, option):
    """
    Calculates the length of the longest sequence with the 'option' property
    :param number_list: list of complex numbers
    :param option: indicates the property we want to apply
    :return: maximum length of the sequence
    """
    lengthmax = 0

    for number in range(len(number_list)):
        length = calculate_length(number_list, number, option)
        lengthmax = maximum(length, lengthmax)

    return lengthmax


def first_element_of_longest_seq(number_list, lengthmax, option):
    """
    Finds the index of the first element of the longest sequence of a given property
    :param number_list: list of complex numbers
    :param lengthmax: the length of the longest sequence
    :param option: indicates the given property
    :return: the index of the first element of the longest sequence
    """
    for number in range(len(number_list)):
        length = calculate_length(number_list, number, option)
        if length == lengthmax:
            return number


def longest_seq_equal_mod():
    """
    States the 'id' of the property
    :return: the id
    """
    return '1'


def longest_seq_increasing_mod():
    """
    States the 'id' of the property
    :return: the id
    """
    return '2'


def list_init(number_list):
    number_list.append(create_complex_number('5+2i'))
    number_list.append(create_complex_number('2+5i'))
    number_list.append(create_complex_number('2+5i'))
    number_list.append(create_complex_number('8+6i'))
    number_list.append(create_complex_number('6+10i'))
    number_list.append(create_complex_number('3+8i'))
    number_list.append(create_complex_number('4+9i'))
    number_list.append(create_complex_number('5+10i'))
    number_list.append(create_complex_number('6+12i'))
    number_list.append(create_complex_number('7+9i'))


if __name__ == "__main__":
    start()