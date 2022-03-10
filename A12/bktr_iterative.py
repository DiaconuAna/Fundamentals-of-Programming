def init_next_elem(array):
    """
    Create new position to add element on
    :param array:
    :param k:
    :return:
    """
    array.append(0)


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
    for elem in array:
        s += elem
    return s


def print_sol(array, x):
    print(x,end = "= ")
    for index in range(len(array)-2):
        print(array[index], end= '+')
    print(array[len(array) - 2])


def is_valid(array):
    """
    A solution is valid if the elements are in increasing order
    :param array:
    :return:
    """
    number = array[0]
    for index in range(1, len(array)-1):
        if number > array[index]:
            return 0
        number = array[index]

    return 1

def successor(x, array):
    """
    Checks if x can be the next element of the solution
    :param x:
    :param array:
    :return:
    """
    if is_prime(x) == 0:
        return 0
    if x >=  array[-1]:
        return 1
    return 0


def iterative_backtracking(number):
    array = []
    k = 0
    array.append(0)
    while k >= 0:
        sum_arr = sum(array)

        if sum_arr == number:
            if is_valid(array):
                print_sol(array, number)
        elif sum_arr > number:
            k = k - 2
            array.pop(-1)
            array.pop(-1)

        if k < 0: #we have finished all combinations
            return

        val = array[-1] + 1

        while not successor(val, array):
            val += 1

        #print(val,"  ", array[k])
        #print(sum_arr)
        if val >= array[k]:
            #array.append(0)
            array[k] = val
            array.append(0)
            k += 1
        else:
            k -= 1


        #print(array)
        #print()






number = int(input())
array = []
iterative_backtracking(number)









