import collections


def is_dictionary_empty(dictionary):
    if dictionary == []:
        return True

    if type(dictionary) is not dict:
        return False

    for k, v in dictionary.items():
        if v == []:
            continue
        elif type(v) is dict:
            if not is_dictionary_empty(v):
                return False
        else:
            return False
    return True


def flatten_dict(d, parent_key='', sep='/'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
