"""
Domain file includes code for entity management
entity = number, transaction, expense etc.
"""


def get_p1(participant):
    return participant['p1']


def get_p2(participant):
    return participant['p2']


def get_p3(participant):
    return participant['p3']


def get_position(participant):
    return participant['position']


def set_p1(participant, value):
    participant['p1'] = value


def set_p2(participant, value):
    participant['p2'] = value


def set_p3(participant, value):
    participant['p3'] = value


def set_position(participant, value):
    participant['position'] = value


def get_command(operation):
    return operation['command']


def get_list(operation):
    return operation['list']


def average_score(p1, p2, p3):
    """
    Computes the average score of a participant
    :param p1: P1 score
    :param p2: P2 score
    :param p3: P3 score
    :return: (p1+p2+p3)/3
    """
    return float((p1+p2+p3)/3)


def average_extended(average_list):
    """
    Computes the average score of the scores from a list
    :param average_list: List of average scores
    :return: Average score of given scores
    """
    sum = 0
    number_of_elements = len(average_list)

    for index in range(len(average_list)):
        sum += average_list[index]

    return float(sum/number_of_elements)
