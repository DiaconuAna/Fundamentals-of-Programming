"""
Consider a positive number n. Determine all its decompositions as sums of prime numbers.
"""


def is_prime(x):
    if x < 2:
        return 0
    if x == 2:
        return 1
    if x%2 == 0:
        return 0

    for j in range(3,x,2):
        if x%j == 0:
            return 0

    return 1


def sum(array):
    s = 0
    for number in array:
        s += number

    return s


def print_sol(array, x):
    print(x,end = "= ")
    for index in range(len(array)-1):
        print(array[index], end= '+')
    print(array[len(array) - 1])


def is_valid(array):
    """
    A solution is valid if the elements are in increasing order
    :param array:
    :return:
    """
    number = array[0]
    for index in range(1, len(array)):
        if number > array[index]:
            return 0
        number = array[index]

    return 1


def backtracking(array, number):
    sum_arr = sum(array)
    if sum_arr == number:
        if is_valid(array):
            print_sol(array, number)
        return
    if sum_arr > number:
        return
    array.append(0)
    for i in range(2, number - sum_arr+1):
        #print(number," ",number - sum(array)," ",i)
        if is_prime(i):
            array[-1] = i
            backtracking(array[:],  number)



number = int(input())
array = []
backtracking(array, number)