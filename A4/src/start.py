"""
Assemble the program and start the user interface here
"""

from src.ui.console import *

test_sort_by_position()
test_find_by_position()
test_create_participant()
test_remove_participant()
test_add_participant()
test_insert_scores()
test_split_command()
test_replace_score()
test_sort_by_average_score()
test_undo()
test_avg()
test_lowest_avg()


if __name__ == "__main__":
   command_menu_ui()
