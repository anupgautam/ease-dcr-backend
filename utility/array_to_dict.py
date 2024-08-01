def array_of_dict_id(array):
    return_dict = {}
    for i in array:
        if return_dict.get(i.id):
            return_dict[i.id] += 1
        else:
            return_dict[i.id] = 1
    return return_dict

def array_of_dict_group_id(array):
    return_dict = {}
    for i in array:
        if return_dict.get(i.group_id.id):
            return_dict[i.group_id.id] += 1
        else:
            return_dict[i.group_id.id] = 1
    return return_dict