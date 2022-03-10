
def filter_function(filter_list, key):
    filtered_list = []
    for index in range(len(filter_list)):
        obj = filter_list[index]
        if key(obj):
            filtered_list.append(obj)
    return filtered_list