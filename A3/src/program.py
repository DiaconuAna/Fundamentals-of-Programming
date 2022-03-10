#
# Write the implementation for A3 in this file
#

"""
Assignment 3, 2.Contest. Conventions:
  - all consecutive positions must be occupied
   eg. you cannot fill position 5 unless position 4 has been filled beforehand
   Insertion: adding a new element between two existent elements
   Position is a string
   --Average score is an integer
"""

#
# domain section is here (domain = numbers, transactions, expenses, etc.)
# getters / setters
# No print or input statements in this section
# Specification for all non-trivial functions (trivial usually means a one-liner)


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


def average_score(p1, p2, p3):
    """
    Computes the average score of a participant
    :param p1: P1 score
    :param p2: P2 score
    :param p3: P3 score
    :return: (p1+p2+p3)/3
    """
    return float((p1+p2+p3)/3)

# Functionalities section (functions that implement required features)
# No print or input statements in this section
# Specification for all non-trivial functions (trivial usually means a one-liner)
# Each function does one thing only
# Functions communicate using input parameters and their return values

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


def shift_participants(participant_list, position):
    """
    Makes room to insert a new participant at the given position by incrementing other participant's positions who have positions bigger than the given one, by one
    :param participant_list: list of participants
    :param position: -
    :return: -
    """
    for index in range(len(participant_list)):
        participant = participant_list[index]
        if int(get_position(participant)) >= int(position):
         set_position(participant, int(get_position(participant))+1)


def to_str_participant(participant):
    """
    Build the string representation of the given participant
    :param participant: -
    :return: -
    """
    return str(get_position(participant)).rjust(2) + ". " + str(get_p1(participant)).ljust(2) + " " + str(get_p2(participant)).ljust(2) + " " + str(get_p3(participant)).ljust(2)


def sort_participant_list_by_position(participant_list):
    """
    Sorts the list of participants by position, in increasing order
    :param participant_list: list of participants
    :return: -
    """
    for index1 in range(len(participant_list)-1):
        for index2 in range(index1+1, len(participant_list)):
            participant1 = participant_list[index1]
            participant2 = participant_list[index2]
            if int(get_position(participant1)) > int(get_position(participant2)):
                aux = participant_list[index1]
                participant_list[index1] = participant_list[index2]
                participant_list[index2] = aux


def sort_participant_list_by_average_score(participant_list):
    """
    Sorts the list of participants by average score, in decreasing order
    :param participant_list: List of participants
    :return: -
    """
    for index1 in range(len(participant_list)-1):
        for index2 in range(index1+1, len(participant_list)):
            participant2 = participant_list[index2]
            avg2 = average_score(get_p1(participant2), get_p2(participant2), get_p3(participant2))
            participant1 = participant_list[index1]
            avg1 = average_score(get_p1(participant1), get_p2(participant1), get_p3(participant1))

            if avg2 >= avg1:
                aux = participant_list[index1]
                participant_list[index1] = participant_list[index2]
                participant_list[index2] = aux


def insert_participant(participant_list, position, p1, p2, p3):
    """
    Insert a participant at a given position
    :param participant_list: List of participants
    :param position: Position of insertion
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


def add_participant(participant_list, p1, p2, p3, position):
   """
   Add a new participant to the list
   :param participant_list: List of participants
   :param p1: P1 score
   :param p2: P2 score
   :param p3: P3 score
   :param position: participant's position- length of list if default
   :return: -
   """
   if position == '-1':
       position = len(participant_list)

   participant = create_participant(int(p1), int(p2), int(p3), position)
   participant_list.append(participant)


def insert_scores(participant_list, position, p1, p2, p3):
    """
    Inserts new score at given position
    :param participant_list: List of participants
    :param position: Insertion position
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

def list_equal_aux(participant_list,new_list,value):
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
        if average_score(p1,p2,p3) == value:
            new_list.append(index)


def list_less_than_aux(participant_list,new_list,value):
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
        if average_score(p1,p2,p3) < value:
            new_list.append(index)


def list_larger_than_aux(participant_list,new_list,value):
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
        if average_score(p1,p2,p3) > value:
            new_list.append(index)

def display_list_aux(participant_list,condition,value):
    """
    Selects the participants with average scores that have the given property
    :param participant_list:
    :param condition:
    :param value:
    :return:
    """
    new_list=[]
    if condition == '=':
        list_equal_aux(participant_list,new_list,value)
    elif condition == '<':
        list_less_than_aux(participant_list,new_list,value)
    elif condition == '>':
        list_larger_than_aux(participant_list,new_list,value)
    else:
        raise ValueError("Invalid input !")




# UI section
# (all functions that have input or print statements, or that CALL functions with print / input are  here).
# Ideally, this section should not contain any calculations relevant to program functionalities

def replace_score_cmd_ui(participant_list, cmd_params):
    """
    Replace the score of a problem obtained by the participant at the given position with a new value
    :param participant_list: List of participants
    :param cmd_params: Command parameters
    :return: -
    """

    tokens = cmd_params.split(' ')
    for i in range(len(tokens)):
        tokens[i] = tokens[i].strip()

    if len(tokens) < 4:
        raise ValueError("Too few parameters")
    elif len(tokens) > 4:
        raise ValueError("Too many parameters")
    else:
        replace_score_participant(participant_list, tokens[0], int(tokens[3]), tokens[1])


def remove_scores_cmd_ui(participant_list, cmd_params):
   """
   Remove scores based on command parameters
   :param participant_list: List of participants
   :param cmd_params: Command parameters
   :return: -
   """
   tokens = cmd_params.split(' ')
   for i in range(len(tokens)):
       tokens[i] = tokens[i].strip()

   if len(tokens) == 1:
       remove_scores(participant_list, tokens[0])
   elif len(tokens) == 3:
       remove_score_complex(tokens[0], tokens[2], participant_list)
   else:
       raise ValueError("The number of parameters is invalid")


def insert_scores_cmd_ui(participant_list, cmd_params):
    """
    Insert participant at given position if possible
    :param participant_list: List of participants
    :param cmd_params: Command parameters
    :return:
    """
    tokens = cmd_params.split(' ')
    for i in range(len(tokens)):
        tokens[i] = tokens[i].strip()

    if len(tokens) > 5:
        raise ValueError("Too many parameters")
    elif len(tokens) < 5:
        raise ValueError("Too few parameters")
    insert_scores(participant_list, tokens[4], tokens[0], tokens[1], tokens[2])


def display_list(participant_list):
    """
    Display the participant list
    :param participant_list: List of participants
    :return: -
    """
    sort_participant_list_by_position(participant_list)
    for index in range(len(participant_list)):
        print(to_str_participant(participant_list[index]))


def display_list_sorted(participant_list):
    """
    Display the participant list in decreasing order of average score
    :param participant_list: List of participants
    :return: -
    """
    sort_participant_list_by_average_score(participant_list)
    for index in range(len(participant_list)):
        print(to_str_participant(participant_list[index]))


def display_list_aux(participant_list,condition,value):
    """
    Selects the participants with average scores that have the given property
    :param participant_list:
    :param condition:
    :param value:
    :return:
    """
    if condition == '=':
        display_list_equal(participant_list,value)
    elif condition == '<':
        display_list_less_than(participant_list,value)
    elif condition == '>':
        display_list_larger_than(participant_list,value)
    elif condition not in condition_dict:
        raise ValueError("Invalid input !")

def display_list_equal(participant_list, value):
    """
    Display participants with an average score = <value>
    :param participant_list: List of participants
    :param value: Value taken into account when displaying participants
    :return: -
    """
    new_list = []
    list_equal_aux(participant_list,new_list,value)
    if len(new_list) == 0:
        raise ValueError("There are no average scores equal to the given value.")

    for index in range(len(new_list)):
        participant = participant_list[new_list[index]]
        print(to_str_participant(participant))

def display_list_less_than(participant_list, value):
    """
    Display participants with an average score < <value>
    :param participant_list: List of participants
    :param value: Value taken into account when displaying participants
    :return: -
    """
    new_list = []
    list_less_than_aux(participant_list, new_list, value)
    if len(new_list) == 0:
        raise ValueError("There are no average scores that are less than the given value.")

    for index in range(len(new_list)):
        participant = participant_list[new_list[index]]
        print(to_str_participant(participant))


def display_list_larger_than(participant_list, value):
    """
    Display participants with an average score > <value>
    :param participant_list: List of participants
    :param value: Value taken into account when displaying participants
    :return: -
    """
    new_list = []
    list_larger_than_aux(participant_list,new_list,value)
    if len(new_list) == 0:
        raise ValueError("There are no average scores that are larger than the given value.")

    for index in range(len(new_list)):
        participant = participant_list[new_list[index]]
        print(to_str_participant(participant))


def display_scores_cmd_ui(participant_list, cmd_params):
    """
    Displays participant scores according to a given command
    :param participant_list: List of participants
    :param cmd_params: Command parameters
    :return: -
    """
    tokens = cmd_params.split(' ')
    for i in range(len(tokens)):
        tokens[i] = tokens[i].strip()

    sort_participant_list_by_position(participant_list)

    if len(tokens) == 1:
        if tokens[0] == '-':
            display_list(participant_list)
        elif tokens[0] == 'sorted':
            display_list_sorted(participant_list)
        else:
            raise ValueError("Invalid input")
    elif len(tokens) == 2:
        display_list_aux(participant_list,tokens[0],int(tokens[1]))
    else:
        raise ValueError("Invalid number of parameters !")


def add_scores_cmd_ui(participant_list, cmd_params):
    """
    Adds the scores of a new participant to the list
    :param participant_list: the list of participants
    :param cmd_params: Parameters of the command
    :return: -
    """
    tokens = cmd_params.split(' ')
    if len(tokens) > 3:
        raise ValueError("Too many parameters")
    elif len(tokens) < 3:
        raise ValueError("Too few parameters")
    else:
        for i in range(len(tokens)):
            tokens[i] = tokens[i].strip()
    add_participant(participant_list, tokens[0], tokens[1], tokens[2], '-1')


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


def command_menu_ui():
   participant_list = []
   test_init(participant_list)
   command_dict = {'add': add_scores_cmd_ui, 'list': display_scores_cmd_ui, 'insert': insert_scores_cmd_ui, 'remove': remove_scores_cmd_ui, 'replace': replace_score_cmd_ui}
   is_it_over = False

   while not is_it_over:
       command = input("Your command>")
       cmd_word, cmd_params = split_command(command)

       if cmd_word in command_dict:
           try:
               command_dict[cmd_word](participant_list, cmd_params)
           except ValueError as val_error:
               print(str(val_error))
       elif cmd_word == 'exit':
           is_it_over = True
           print("Goodbye !")
       else:
           print('Invalid command. Please try again :") ')


# Test functions go here
#
# Test functions:
#   - no print / input
#   - great friends with assert

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

    add_participant(participant_list, 3, 4 , 5, '-1')
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
    assert get_p1(participant_list[index]) == 7

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
        participant = create_participant(104, 5 , 6 ,'54')
        assert False
    except ValueError:
        assert True


def test_find_by_position():
    participant_list = []
    test_init(participant_list)

    index = find_by_position(participant_list,'5')
    assert get_position(participant_list[index]) == '5'

    index = find_by_position(participant_list,'67')
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
        assert average_score(get_p1(participant_list[index]),get_p2(participant_list[index]),get_p3(participant_list[index])) >= average_score(get_p1(participant_list[index+1]),get_p2(participant_list[index+1]),get_p3(participant_list[index+1]))


test_sort_by_position()
test_find_by_position()
test_create_participant()
test_add_participant()
test_insert_scores()
test_remove_participant()
test_split_command()

if __name__ == "__main__":
   command_menu_ui()