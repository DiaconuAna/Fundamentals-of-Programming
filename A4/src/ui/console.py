"""
This is the user interface module. These functions call functions from the domain and functions module.
"""

from src.functions.functions import *
import copy


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
   elif len(tokens) == 2:
       remove_average_scores(participant_list, tokens[0], int(tokens[1]))
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


def display_list_positions(new_list):
    """
    Display the participant list by its participants' position
    :param new_list: List of participants
    :return: -
    """
    sort_participant_list_by_position(new_list)
    display_list(new_list)


def display_list(participant_list):
    """
    Display the participant list as given
    :param participant_list: List of participants
    :return: -
    """
    for index in range(len(participant_list)):
        print(to_str_participant(participant_list[index]))


def display_list_sorted(new_list):
    """
    Display the participant list in decreasing order of average score
    :param new_list: List of participants
    :return: -
    """
    sort_participant_list_by_average_score(new_list)
    for index in range(len(new_list)):
        print(to_str_participant(new_list[index]))


def display_list_equal(new_list, value):
    """
    Display participants with an average score = <value>
    :param new_list: List of participants
    :param value: Value taken into account when displaying participants
    :return: -
    """
    tmp_list = []
    list_equal_aux(new_list, tmp_list, value)
    if len(tmp_list) == 0:
        raise ValueError("There are no average scores that are equal to the given value.")

    for index in range(len(tmp_list)):
        participant = new_list[tmp_list[index]]
        print(to_str_participant(participant))


def display_list_less_than(new_list, value):
    """
    Display participants with an average score < <value>
    :param new_list: List of participants
    :param value: Value taken into account when displaying participants
    :return: -
    """
    tmp_list = []
    list_less_than_aux(new_list, tmp_list, value)
    if len(tmp_list) == 0:
        raise ValueError("There are no average scores that are less than the given value.")

    for index in range(len(tmp_list)):
        participant = new_list[tmp_list[index]]
        print(to_str_participant(participant))


def display_list_larger_than(new_list, value):
    """
    Display participants with an average score > <value>
    :param new_list: List of participants
    :param value: Value taken into account when displaying participants
    :return: -
    """
    tmp_list = []
    list_larger_than_aux(new_list, tmp_list, value)
    if len(tmp_list) == 0:
        raise ValueError("There are no average scores that are larger than the given value.")

    for index in range(len(tmp_list)):
        participant = new_list[tmp_list[index]]
        print(to_str_participant(participant))


def display_list_aux(participant_list, condition, value):
    """
    Selects the participants with average scores that have the given property
    :param participant_list:
    :param condition:
    :param value:
    :return:
    """
    if condition == '=':
        display_list_equal(participant_list, value)
    elif condition == '<':
        display_list_less_than(participant_list, value)
    elif condition == '>':
        display_list_larger_than(participant_list, value)
    else:
        raise ValueError("Invalid input !")


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
        display_list_aux(participant_list, tokens[0], int(tokens[1]))
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


def display_average(participant_list, cmd_params):
    """
    Display the average of the average scores for participants between two given position
    :param participant_list: -
    :param cmd_params: -
    :return: -
    """
    tokens = cmd_params.split(' ')
    if len(tokens) != 3:
        raise ValueError("Invalid number of parameters!")

    average = compute_average(participant_list, tokens[0], tokens[2])
    print("The average of average scores for participants between ", tokens[0], " and ", tokens[2], "is: ", round(average, 2))


def lowest_avg_ui(participant_list, cmd_params):
    """
    Determines the lowest average score of the participants between two given position and displays it
    :param participant_list: -
    :param cmd_params: -
    :return: -
    """
    tokens = cmd_params.split(' ')
    if len(tokens) != 3:
        raise ValueError("Invalid number of parameters!")

    lowest_average = lowest_average_score(participant_list, tokens[0], tokens[2])
    print("The lowest average score of the participants between ", tokens[0], " and ", tokens[2], "is: ", round(lowest_average, 2))


def top_list_ui(participant_list, cmd_params):
    """

    :param participant_list:
    :param cmd_params:
    :return:
    """
    tokens = cmd_params.split(" ")
    if len(tokens) == 1:
        top_avg_list_ui(participant_list, int(tokens[0]))
    elif len(tokens) == 2:
        top_score_ui(participant_list, int(tokens[0]), tokens[1])
    else:
        raise ValueError("Invalid number of parameters. ")


def top_avg_list_ui(participant_list, number):
    """
    Display the top 'number' of participants having the highest average score
    :param participant_list: List of participants
    :param number: Number of participants in the top
    :return: -
    """

    average_list = []
    top_list(participant_list, average_list, number)
    display_list(average_list)


def top_score_ui(participant_list, number, problem_id):
    """
    Display the top participants who obtained the highest score for a problem identified by its id
    :param participant_list: List of participants
    :param number: Number of participants in the top
    :param problem_id: P1,P2 or P3
    :return: -
    """

    score_list = []
    top_list_number(participant_list, score_list, number, problem_id)
    display_list(score_list)


def undo_ui(operation_list, participant_list):
    """
    Undo the last operation
    :param operation_list:
    :param participant_list:
    :return:
    """
    if len(operation_list) == 0:
        raise ValueError("No more operations to be undone.")
    else:
        operation = operation_list[-1]
        print("Your last command was ", get_command(operation))
        print("Do you still want to undo it? >> YES /// NO <<<")
        command = input().lower()
        if command == 'yes':
            undo(operation_list, participant_list)
        elif command == 'no':
            print("Come back if you change your mind! :D")
        else:
            raise ValueError("You're an indecisive one, I see...")


def print_menu():
    print()
    print("add <P1 score> <P2 score> <P3 score>")
    print("insert <P1 score> <P2 score> <P3 score> at <position>")
    print("remove <position>")
    print("remove <start position> to <end position")
    print("replace <old score> <P1 | P2 | P3> with <new score>")
    print("list")
    print("list sorted")
    print("list [ < | = | > ] <score>")
    print("avg <start position> to <end position>")
    print("min <start position> to <end position>")
    print("top <number>")
    print("top <number> <P1 | P2 | P3>")
    print("remove [ < | = | > ] <score>")
    print("undo")
    print()


def command_menu_ui():
   operation_list = []
   participant_list = []
   test_init(participant_list)
   command_dict = {'add': add_scores_cmd_ui, 'list': display_scores_cmd_ui, 'insert': insert_scores_cmd_ui, 'remove': remove_scores_cmd_ui, 'replace': replace_score_cmd_ui, 'avg': display_average, 'min': lowest_avg_ui, 'top': top_list_ui}
   undo_list = ['add', 'insert', 'remove', 'replace']
   is_it_over = False

   while not is_it_over:
       print_menu()
       command = input("Your command>")
       cmd_word, cmd_params = split_command(command)

       if cmd_word in command_dict:
           try:
               command_dict[cmd_word](participant_list, cmd_params)
               if cmd_word in undo_list:
                   create_element(operation_list, command, participant_list)
           except ValueError as val_error:
               print(str(val_error))
       elif cmd_word == 'undo':
           try:
               undo_ui(operation_list, participant_list)
           except ValueError as val_error:
               print(str(val_error))
       elif cmd_word == 'exit':
           is_it_over = True
           print("Come back soon !")
       else:
           print('Invalid command. Please try again :") ')


