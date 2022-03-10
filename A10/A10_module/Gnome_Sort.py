

def gnome_sort(sort_list, sorting_key):
    index = 0
    while index < len(sort_list):
        if index == 0:
            index += 1
        elif not sorting_key(sort_list[index], sort_list[index-1]):
            index += 1
        else:
            temp = sort_list[index]
            sort_list[index] = sort_list[index-1]
            sort_list[index-1] = temp
            index -= 1
