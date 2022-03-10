"""
Functions that implement program features. They should call each other, or other functions from the domain
"""
from src.domain.entity import *
import copy


def create_element(operation_list, command, participant_list):
    """
    Creates and element of operation list and appends it to the list
    :param operation_list:
    :param command:
    :param participant_list:
    :return:
    """
    aux_list = copy.deepcopy(participant_list)
    operation = create_operation(command, aux_list)
    operation_list.append(operation)


def create_operation(command, list):
    """
    Creates an operation
    :param command: Command
    :param list: Modified list after using command
    :return: -
    """
    return {'command': command, 'list': list}


def undo(operation_list, participant_list):
    """
    Undo the last operation, if possible
    :param operation_list:
    :param participant_list:
    :return:
    """
    if len(operation_list) == 0:
        raise ValueError("There are no more operations to be undone. Please do some.")

    operation_list.pop(len(operation_list)-1)
    if len(operation_list) != 0:
        participant_list.clear()
        aux_list = copy.deepcopy(get_list(operation_list[-1]))
        participant_list.extend(aux_list)
    else:
        participant_list.clear()
        test_init(participant_list)


def is_integer(number):
    """
    Check if given number is an integer in [0,10]
    :param number: -
    :return: 1 if true, else 0
    """
    if int(number) >= 0 and int(number) <= 10:
        return 1
    else:
        return 0


def create_participant(p1, p2, p3, position):
    """
    Creates a new participant with the given information
    :param p1: P1 score
    :param p2: P2 score
    :param p3: P3 score
    :param position: Participant's position on the list
    :return: The new participant's data
    """
    if is_integer(p1) == 0:
        raise ValueError('P1 score should be integer in [0, 10]')

    if is_integer(p2) == 0:
        raise ValueError('P2 score should be integer in [0, 10]')

    if is_integer(p3) == 0:
        raise ValueError('P3 score should be integer in [0, 10]')

    return {'position': position, 'p1': p1, 'p2': p2, 'p3': p3}


def possibility_to_insert(participant_list, position):
    """
    Checks if a participant at a given position can be inserted within the current participant list
    :param participant_list: -
    :param position: -
    :return: 1 if true, else 0
    """
    if int(position) >= len(participant_list):
        return 0
    else:
        return 1


def remove_score_simple(participant):
    """
    Set the scores of the participant to 0
    :param participant: -
    :return: -
    """
    set_p1(participant, 0)
    set_p2(participant, 0)
    set_p3(participant, 0)


def remove_score_complex(start_position, end_position, participant_list):
    """
    Set the scores of participants at positions [<start_position>,<end_position>] to 0
    :param start_position: -
    :param end_position: -
    :param participant_list: List of participants
    :return: -
    """
    for position in range(int(start_position), int(end_position)+1):
        if position > len(participant_list):
            raise ValueError("Cannot remove from this position as there are no more participants in the list")
        else:
            participant = participant_list[find_by_position(participant_list, position)]
            remove_score_simple(participant)


def remove_average_scores_equal(participant_list, score):
    """
    Set the scores of participants having an average score = 'score' to 0
    :param participant_list: List of participants
    :param score: -
    :return: -
    """

    tmp = 0
    for index in range(len(participant_list)):
        participant = participant_list[index]
        if average_score(get_p1(participant), get_p2(participant), get_p3(participant)) == score:
            remove_score_simple(participant_list[index])
            tmp += 1
    if tmp == 0:
        raise ValueError("No score was removed.")


def remove_average_scores_larger_than(participant_list, score):
    """
    Set the scores of participants having an average score > 'score' to 0
    :param participant_list: List of participants
    :param score: -
    :return: -
    """

    tmp = 0
    for index in range(len(participant_list)):
        participant = participant_list[index]
        if average_score(get_p1(participant), get_p2(participant), get_p3(participant)) > score:
            remove_score_simple(participant_list[index])
            tmp += 1

    if tmp == 0:
        raise ValueError("No score was removed.")


def remove_average_scores_less_than(participant_list, score):
    """
    Set the scores of participants having an average score < 'score' to 0
    :param participant_list: List of participants
    :param score: -
    :return: -
    """
    tmp = 0
    for index in range(len(participant_list)):
        participant = participant_list[index]
        if average_score(get_p1(participant), get_p2(participant), get_p3(participant)) < score:
            remove_score_simple(participant_list[index])
            tmp += 1
    if tmp == 0:
        raise ValueError("No score was removed.")


def remove_average_scores(participant_list, relation_id, score):
    """
    Set the scores of participants having a certain average score, based on relation id and top score
    :param participant_list: List of participants
    :param relation_id: < , = or >
    :param score: The removal standard
    :return: -
    """

    if score < 0 or score > 10:
        raise ValueError("Standard score should be an integer in [0,10].")
    if relation_id == '<':
        remove_average_scores_less_than(participant_list, score)
    elif relation_id == '=':
        remove_average_scores_equal(participant_list, score)
    elif relation_id == '>':
        remove_average_scores_larger_than(participant_list, score)
    else:
        raise ValueError("Invalid relation id. It should be either '<' , '=' or '>' !")


def replace_score_problem(participant, problem_id, value):
    """
    Replace the score obtained by the participant at problem<score> with <value>
    :param participant: The participant wr want to change the score for
    :param problem_id: P1,P2 or P3's id
    :param value: the new score
    :return: -
    """
    problem_dict = {'p1': set_p1, 'p2': set_p2, 'p3': set_p3}
    if value < 0 or value > 10:
        raise ValueError("Problem score should be an integer in [0,10]")
    if problem_id in problem_dict:
        problem_dict[problem_id](participant, value)
    else:
        raise ValueError("Invalid input. Please enter problem id as p<Problem number> !")


def shift_participants(new_list, position):
    """
    Makes room to insert a new participant at the given position by incrementing other participant's positions who have positions bigger than the given one, by one
    :param new_list: List of participants
    :param position: Position of insertion
    :return:
    """

    for index in range(len(new_list)):
        participant = new_list[index]
        if int(get_position(participant)) >= int(position):
         set_position(participant, int(get_position(participant))+1)


def to_str_participant(participant):
    """
    Build the string representation of the given participant
    :param participant: -
    :return: -
    """
    return str(get_position(participant)).rjust(2) + ". " + str(get_p1(participant)).ljust(2) + " " + str(get_p2(participant)).ljust(2) + " " + str(get_p3(participant)).ljust(2)


def sort_participant_list_by_position(new_list):
    """
    Sorts the list of participants by position, in increasing order
    :param new_list: list of participants
    :return: -
    """
    for index1 in range(len(new_list)-1):
        for index2 in range(index1+1, len(new_list)):
            participant1 = new_list[index1]
            participant2 = new_list[index2]
            if int(get_position(participant1)) > int(get_position(participant2)):
                aux = new_list[index1]
                new_list[index1] = new_list[index2]
                new_list[index2] = aux


def sort_list_by_problem(participant_list, problem_id):
    """
    Sorts the participants in ascending order by their problem id score
    :param participant_list: List of participants
    :param problem_id: P1,P2 or P3
    :return: -
    """
    problem_id.lower()
    problem_dict = {'p1': get_p1, 'p2': get_p2, 'p3': get_p3}
    if problem_id not in problem_dict:
        raise ValueError("Invalid problem number. Please choose between P1,P2 and P3 only!")

    prev_list = get_list(participant_list)
    new_list = prev_list.copy()

    for index1 in range(len(new_list)-1):
        for index2 in range(index1+1, len(new_list)):
            participant1 = new_list[index1]
            participant2 = new_list[index2]
            if problem_dict[problem_id](participant1) < problem_dict[problem_id](participant2):
                aux = new_list[index1]
                new_list[index1] = new_list[index2]
                new_list[index2] = aux


def sort_participant_list_by_average_score(new_list):
    """
    Sorts the list of participants by average score, in decreasing order
    :param new_list: List of participants
    :return: -
    """
    for index1 in range(len(new_list)-1):
        for index2 in range(index1+1, len(new_list)):
            participant2 = new_list[index2]
            avg2 = average_score(get_p1(participant2), get_p2(participant2), get_p3(participant2))
            participant1 = new_list[index1]
            avg1 = average_score(get_p1(participant1), get_p2(participant1), get_p3(participant1))

            if avg2 >= avg1:
                aux = new_list[index1]
                new_list[index1] = new_list[index2]
                new_list[index2] = aux


def compute_average(participant_list, start_position, end_position):
    """
    Computes the average score of the average scores for participants between two given positions
    :param participant_list: -
    :param start_position: -
    :param end_position: -
    :return: Average score of average scores
    """
    average_list = []

    if int(start_position) >= len(participant_list) or int(start_position) < 0:
        raise ValueError("There are no participants starting from ", start_position)



    for index in range(len(participant_list)):
        participant = participant_list[index]
        if int(get_position(participant)) >= int(start_position) and int(get_position(participant)) <= int(end_position):
            p1 = get_p1(participant)
            p2 = get_p2(participant)
            p3 = get_p3(participant)
            avg = average_score(p1, p2, p3)
            average_list.append(avg)

    return average_extended(average_list)


def insert_participant(participant_list, position, p1, p2, p3):
    """
    Insert a participant at a given position
    :param participant_list: List of participants
    :param position: Position of insertion given as a string
    :param p1: P1 score
    :param p2: P2 score
    :param p3: P3 score
    :return: -
    """

    if is_integer(p1) and is_integer(p2) and is_integer(p3):
        shift_participants(participant_list, position)
        add_participant(participant_list, p1, p2, p3, position)
    else:
        raise ValueError("Invalid position or problem scores")


def find_by_position(participant_list, position):
    """
    Finds a participant by their position in the list
    :param participant_list: List of participants
    :param position: Position of the participant we want to find
    :return: participant's index in list or 0 if it doesn't exist
    """

    for index in range(len(participant_list)):
        if int(get_position(participant_list[index])) == int(position):
            return index

    return -1


def add_participant(new_list, p1, p2, p3, position):
   """
   Add a new participant to the list
   :param new_list: Record of lists of participants
   :param p1: P1 score
   :param p2: P2 score
   :param p3: P3 score
   :param position: participant's position- length of list if default
   :return: -
   """
   if position == '-1':
       position = len(new_list)

   participant = create_participant(int(p1), int(p2), int(p3), position)
   new_list.append(participant)


def insert_scores(participant_list, position, p1, p2, p3):
    """
    Inserts new score at given position
    :param participant_list: List of participants
    :param position: Insertion position given as a string
    :param p1: P1 score
    :param p2: P2 score
    :param p3: P3 score
    :return: -
    """
    if possibility_to_insert(participant_list, position):
        insert_participant(participant_list, position, p1, p2, p3)
    else:
        raise ValueError("Cannot be inserted at the given position as the said position hasn't been created yet")


def remove_scores(participant_list, position):
    """
    Remove scores for a participant at a given position by setting them to 0
    :param participant_list: List of participants
    :param position: Position of the participant
    :return: -
    """

    index = find_by_position(participant_list, position)
    if index == -1:
        raise ValueError("Participant does not exist in the list")
    else:
        remove_score_simple(participant_list[index])


def replace_score_participant(participant_list, position, value, problem_id):
    """
    Replace score for a participant at a given position
    :param participant_list: List of participant
    :param position: Position of the participant
    :param value: New value
    :param problem_id: Indicates P1,P2 or P3
    :return: -
    """

    participant_index = find_by_position(participant_list, position)

    if participant_index == -1:
        raise ValueError("Participant at the given position is not on the list")
    else:
        participant = participant_list[participant_index]
        replace_score_problem(participant, problem_id, int(value))


def minimum(a, b):
    """
    Finds the minimum of a and b
    :param a: -
    :param b: -
    :return: min(a,b)
    """
    if a < b:
        return a
    else:
        return b


def lowest_average_score(participant_list, start_position, end_position):
    """
    Finds the lowest average score of the participants between two given positions
    :param participant_list: list of participants
    :param start_position: start position given as a string
    :param end_position: end position given as a string
    :return: lowest average score
    """
    #default minimum value
    lowest_avg = 11

    if int(start_position) > len(participant_list):
        raise ValueError("There are no participants starting from ", start_position)

    for index in range(len(participant_list)):
        participant = participant_list[index]
        if int(get_position(participant)) >= int(start_position) and int(get_position(participant)) <= int(end_position):
            lowest_avg = minimum(lowest_avg, average_score(get_p1(participant), get_p2(participant), get_p3(participant)))

    return lowest_avg


def list_equal_aux(participant_list, new_list, value):
    """
    Selects the participants with average scores that are equal to the given value
    :param participant_list:
    :param new_list:
    :param value:
    :return:
    """
    for index in range(len(participant_list)):
        participant = participant_list[index]
        p1 = get_p1(participant)
        p2 = get_p2(participant)
        p3 = get_p3(participant)
        if average_score(p1, p2, p3) == value:
            new_list.append(index)


def list_less_than_aux(participant_list, new_list, value):
    """
    Selects the participants with average scores that are equal to the given value
    :param participant_list:
    :param new_list:
    :param value:
    :return:
    """
    for index in range(len(participant_list)):
        participant = participant_list[index]
        p1 = get_p1(participant)
        p2 = get_p2(participant)
        p3 = get_p3(participant)
        if average_score(p1, p2, p3) < value:
            new_list.append(index)


def list_larger_than_aux(participant_list, new_list, value):
    """
    Selects the participants with average scores that are equal to the given value
    :param participant_list:
    :param new_list:
    :param value:
    :return:
    """
    for index in range(len(participant_list)):
        participant = participant_list[index]
        p1 = get_p1(participant)
        p2 = get_p2(participant)
        p3 = get_p3(participant)
        if average_score(p1, p2, p3) > value:
            new_list.append(index)


def top_list(participant_list, average_list, number):
    """
    Creates a new list with 'number' participants having the highest average score, in descending order of average score
    :param participant_list: List of participants
    :param average_list: List of top participants sorted by average score
    :param number: Number of top participants
    :return: -
    """
    sort_participant_list_by_average_score(participant_list)
    if number > len(participant_list):
        raise ValueError("Your number is larger than the number of participants, thus you cannot have a proper top! (': ")
    if number <= 0:
        raise ValueError("Your number is smaller than 0. Try again :D")
    for index in range(number):
        average_list.append(participant_list[index])


def sort_by_problem_id(participant_list, problem_id):
    """
    Sort the list in decreasing order by one problem's score
    :param participant_list: List of participants
    :param problem_id: P1,P2 or P3
    :return: -
    """
    problem_dict = {'p1': get_p1, 'p2': get_p2, 'p3': get_p3}
    if problem_id not in problem_dict:
        raise ValueError("Invalid problem ID. You should enter one of these: P1, P2, P3")
    sort_participant_list_by_average_score(participant_list)

    for index1 in range(len(participant_list)-1):
        for index2 in range(index1+1, len(participant_list)):
            participant1 = participant_list[index1]
            participant2 = participant_list[index2]
            if problem_dict[problem_id](participant1) < problem_dict[problem_id](participant2):
                aux = participant_list[index1]
                participant_list[index1] = participant_list[index2]
                participant_list[index2] = aux


def top_list_number(participant_list, score_list, number, problem_id):
    """
    Creates a new list with 'number' participants having the highest score for a problem identified by a given id
    :param participant_list: List of participants
    :param score_list: List of top participants
    :param number: Number of top participants
    :param problem_id: P1,P2 or P3
    :return: -
    """

    if number > len(participant_list):
        raise ValueError("Your number is larger than the number of participants, thus you cannot have a proper top! (': ")
    if number <= 0:
        raise ValueError("Your number is smaller than 0. Try again :D")

    sort_by_problem_id(participant_list, problem_id)

    for index in range(number):
        score_list.append(participant_list[index])


def split_command(command):
    """
    Separate user command into command word and parameters
    :param command: User command
    :return: (command word, command parameters)
    """
    tokens = command.strip().split(' ', 1)
    cmd_word = tokens[0].lower().strip()

    if len(tokens) == 2:
        cmd_params = tokens[1].lower().strip()
    else:
        cmd_params = '-'

    return cmd_word, cmd_params


#Test functions


def test_split_command():
    for cmd in ['add 3 8 10', 'AdD 3 8 10', 'aDd      3 8 10   ', 'add 3 8 '
                                                                  '10']:
        cmd_word, cmd_params = split_command(cmd)

        assert cmd_word == 'add' and cmd_params == '3 8 10'

    cmd_word, cmd_params = split_command('exit')
    assert cmd_word == 'exit' and cmd_params == '-'

    for cmd in ['insert  5 6 7 at 5', 'InSErT 5 6 7 at 5', 'INSErt    5 6 7 at 5']:
        cmd_word, cmd_params = split_command(cmd)
        assert cmd_word == 'insert' and cmd_params == '5 6 7 at 5'

    for cmd in ['remove 6', 'reMovE     6', 'REMOve    6']:
        cmd_word, cmd_params = split_command(cmd)
        assert cmd_word == 'remove' and cmd_params == '6'

    for cmd in ['remove 6 to 8', 'reMovE     6 to 8', 'REMOve    6 to 8']:
        cmd_word, cmd_params = split_command(cmd)
        assert cmd_word == 'remove' and cmd_params == '6 to 8'

    for cmd in ['replace 4 P2 with 5', 'replace    4 P2 with 5', 'RePLAce  4 P2 with 5']:
        cmd_word, cmd_params = split_command(cmd)
        assert cmd_word == 'replace' and cmd_params == '4 p2 with 5'

    for cmd in ['list', 'LisT   ']:
        cmd_word, cmd_params = split_command(cmd)
        assert cmd_word == 'list' and cmd_params == '-'

    for cmd in ['list sorted', 'liSt sORted', 'LiSt     SorteD']:
        cmd_word, cmd_params = split_command(cmd)
        assert cmd_word == 'list' and cmd_params == 'sorted'

    for cmd in ['list <', 'List   <', 'LiSt    <']:
        cmd_word, cmd_params = split_command(cmd)
        assert cmd_word == 'list' and cmd_params == '<'


def test_remove_participant():
    participant_list = []
    test_init(participant_list)

    remove_scores(participant_list, '5')
    index = find_by_position(participant_list, '5')
    assert get_p1(participant_list[index]) == 0 and get_p2(participant_list[index]) == 0 and get_p3(participant_list[index]) == 0

    remove_score_complex('6', '8', participant_list)
    for position in range(6, 8):
        index = find_by_position(participant_list, str(position))
        assert get_p1(participant_list[index]) == 0 and get_p2(participant_list[index]) == 0 and get_p3(participant_list[index]) == 0

    test_init(participant_list)
    remove_average_scores_equal(participant_list, 10)
    i1 = find_by_position(participant_list,'0')
    i2 = find_by_position(participant_list,'6')
    p1 = participant_list[i1]
    p2 = participant_list[i2]

    assert average_score(get_p1(p1), get_p2(p1), get_p3(p1)) == 0 and average_score(get_p1(p2), get_p2(p2), get_p3(p2)) == 0

    #try to remove a score for a participant that is not in the list

    try:
        remove_scores(participant_list, '67')
        assert False
    except ValueError:
        assert True

    #try to remove scores when the end position is not in the list
    try:
        remove_score_complex('5', '78', participant_list)
        assert False
    except ValueError:
        assert True


def test_insert_scores():
    participant_list = []
    test_init(participant_list)
    listlength = len(participant_list)

    insert_scores(participant_list, '5', 1, 4, 5)
    index = find_by_position(participant_list, '5')
    assert get_p1(participant_list[index]) == 1 and get_p2(participant_list[index]) == 4 and get_p3(participant_list[index]) == 5 and len(participant_list) == listlength + 1

    insert_scores(participant_list, '7', 10, 3, 7)
    index = find_by_position(participant_list, '7')
    assert get_p1(participant_list[index]) == 10 and get_p2(participant_list[index]) == 3 and get_p3(participant_list[index]) == 7 and len(participant_list) == listlength + 2

    #try to insert on a non-existent position

    try:
        insert_scores(participant_list, '34', 5, 6, 7)
        assert False
    except ValueError:
        assert True

    #try to insert an invalid score
    try:
        insert_scores(participant_list, '7', 56, 6, 7)
    except ValueError:
        assert True


def test_add_participant():
    participant_list = []
    test_init(participant_list)
    listlength = len(participant_list)

    add_participant(participant_list, 3, 4, 5, '-1')
    index = listlength
    assert get_p1(participant_list[index]) == 3 and get_p2(participant_list[index]) == 4 and get_p3(participant_list[index]) == 5 and listlength + 1 == len(participant_list)

    add_participant(participant_list, 10, 9, 7, '-1')
    index = listlength+1
    assert get_p1(participant_list[index]) == 10 and get_p2(participant_list[index]) == 9 and get_p3(participant_list[index]) == 7 and listlength + 2 == len(participant_list)

    #try to add a participant with an invalid problem score
    try:
        add_participant(participant_list, 5, 67, 8, '-1')
        assert False
    except ValueError:
        assert True


def test_replace_score():
    participant_list = []
    test_init(participant_list)

    replace_score_participant(participant_list, '5', 5, 'p3')
    index = find_by_position(participant_list, '5')
    assert get_p3(participant_list[index]) == 5

    replace_score_participant(participant_list, '7', 10, 'p1')
    index = find_by_position(participant_list, '7')
    assert get_p1(participant_list[index]) == 10

    #try to replace with a problem score that is not in [0,10]

    try:
        replace_score_participant(participant_list, '7', 56, 'p2')
        assert False
    except ValueError:
        assert True

    #try to replace with an invalid problem id

    try:
        replace_score_participant(participant_list, '5', 5, 'p5')
        assert False
    except ValueError:
        assert True

    #try to replace the score of a participant that is not in the list
    try:
        replace_score_participant(participant_list, '56', 5, 'p3')
        assert False
    except ValueError:
        assert True


def test_create_participant():
    participant_list = []
    test_init(participant_list)
    length_list = len(participant_list)

    participant = create_participant(5, 6, 7, str(length_list))
    assert get_p1(participant) == 5 and get_p2(participant) == 6 and get_p3(participant) == 7

    participant = create_participant(3, 10, 9, str(length_list))
    assert get_p1(participant) == 3 and get_p2(participant) == 10 and get_p3(participant) == 9

    try:
        create_participant(104, 5, 6, '54')
        assert False
    except ValueError:
        assert True


def test_find_by_position():
    participant_list = []
    test_init(participant_list)

    index = find_by_position(participant_list, '5')
    assert get_position(participant_list[index]) == '5'

    index = find_by_position(participant_list, '67')
    assert index == -1


def test_possibility_to_insert():
    participant_list = []
    test_init(participant_list)

    assert possibility_to_insert(participant_list, '5') == 1
    assert possibility_to_insert(participant_list, '67') == 0


def test_sort_by_position():
    participant_list = []
    test_init(participant_list)
    sort_participant_list_by_position(participant_list)

    for index in range(len(participant_list)-1):
        assert int(get_position(participant_list[index]))<int(get_position(participant_list[index+1]))


def test_sort_by_average_score():
    participant_list = []
    test_init(participant_list)
    sort_participant_list_by_average_score(participant_list)

    for index in range(len(participant_list) - 1):
        assert average_score(get_p1(participant_list[index]), get_p2(participant_list[index]), get_p3(participant_list[index])) >= average_score(get_p1(participant_list[index+1]), get_p2(participant_list[index+1]), get_p3(participant_list[index+1]))


def test_undo():
    operation_list = []
    participant_list = []
    test_init(participant_list)

    #try to undo with no operations done on the list
    try:
        undo(operation_list, participant_list)
        assert False
    except ValueError:
        assert True

    #try to undo some operations
    add_participant(participant_list, 10, 10, 10, -1)
    aux_list = copy.deepcopy(participant_list)
    operation = create_operation('add', aux_list)
    operation_list.append(operation)

    remove_scores(participant_list, '5')
    aux_list = copy.deepcopy(participant_list)
    operation = create_operation('remove', aux_list)
    operation_list.append(operation)

    undo(operation_list, participant_list)
    index = find_by_position(participant_list, '5')
    participant = participant_list[index]
    assert len(participant_list) == 11 and get_p1(participant) == 1 and get_p2(participant) == 6 and get_p3(participant) == 8 and len(operation_list) == 1

    undo(operation_list, participant_list)
    index = find_by_position(participant_list, '9')
    participant = participant_list[index]
    assert len(participant_list) == 10 and get_p1(participant) == 9 and get_p2(participant) == 9 and get_p3(participant) == 9 and len(operation_list) == 0

    try:
        undo(operation_list, participant_list)
        assert False
    except ValueError:
        assert True


def test_avg():
    participant_list = []
    test_init(participant_list)

    try:
        compute_average(participant_list, -1, 5)
        assert False
    except ValueError:
        assert True

    try:
        compute_average(participant_list, 10, 5)
        assert False
    except ValueError:
        assert True


    average = compute_average(participant_list,1,5)
    average = round(average, 2)
    assert average == 7.27

    average = compute_average(participant_list,7,9)
    average = round(average, 2)
    assert average == 8.44


def test_lowest_avg():
    participant_list = []
    test_init(participant_list)

    try:
        lowest_average_score(participant_list, 67, 7)
        assert False
    except ValueError:
        assert True

    average = lowest_average_score(participant_list, 3 ,7)
    average = round(average, 2)
    assert average == 4.33


def test_init(participant_list):
    participant_list.append(create_participant(10, 10, 10, '0'))
    participant_list.append(create_participant(9, 10, 10, '2'))
    participant_list.append(create_participant(10, 8, 10, '1'))
    participant_list.append(create_participant(7, 0, 6, '3'))
    participant_list.append(create_participant(8, 6, 10, '4'))
    participant_list.append(create_participant(1, 6, 8, '5'))
    participant_list.append(create_participant(3, 7, 10, '7'))
    participant_list.append(create_participant(10, 9, 10, '8'))
    participant_list.append(create_participant(10, 10, 10, '6'))
    participant_list.append(create_participant(9, 9, 9, '9'))



