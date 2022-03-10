"""
The sequence a1, ..., an of distinct integer numbers is given. Display all subsets with a mountain aspect.
A set has a mountain aspect if the elements increase up to a point and then they decrease. E.g. 10, 16, 27, 18, 14, 7.
"""


def print_solution(x):
    """
    Prints the  elements of the given array x
    :param x: array of numbers
    :return: -
    """
    for number in x:
        print(number, end=" ")
    print()


def is_increasing(x, y):
    """
    Checks if a sequence is increasing by
    comparing the last two consecutive terms of it
    :param x:
    :param y:
    :return: 1 if increasing, 0 if decreasing
    """
    if x <= y:
        return 1
    else:
        return 0


def is_solution(prev_flag,  current_flag):
    """

    :param prev_flag:
    :param current_flag:
    :return:
    """
    if prev_flag == 0 and current_flag == 1:
        return 0
    elif prev_flag == -1 and current_flag == 0:
        return -1
    elif prev_flag != -1 and current_flag == 0:
        return 1
    elif prev_flag == 1 and  current_flag == 1:
        return 2
    elif prev_flag == -1 and current_flag == 1:
        return 3


def recursive_bktr(x, prev_flag, init_list):
    """

    :param x:
    :param prev_flag:
    :param init_list:
    :return:
    """
    if len(init_list):
        x.append(0)  # making room for the next element
        x[-1] = init_list[0]
        # print(x[-1])
        if len(x) == 1:
            init_list.pop(0)
            recursive_bktr(x, prev_flag, init_list)
        else:
            current_flag = is_increasing(x[-2], x[-1])
            is_sol = is_solution(prev_flag, current_flag)

            if is_sol == 0:
                x = x[-2:]
                recursive_bktr(x, current_flag, init_list[1:])
            elif is_sol == 1:
                print_solution(x)
                recursive_bktr(x, current_flag, init_list[1:])
            elif is_sol == -1:
                recursive_bktr(x, prev_flag, init_list[1:])
            elif is_sol == 2:
                recursive_bktr(x, current_flag, init_list[1:])
            elif is_sol == 3:
                x = x[-2:]
                recursive_bktr(x, current_flag, init_list[1:])
    else:
        return


init_list = [13,12,11,9,10,8,6,10,16,27,18,14,7,9,0]
x = []
recursive_bktr(x,-1, init_list)
