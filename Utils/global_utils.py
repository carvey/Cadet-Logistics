import collections


def sort_queryset(queryset, key, n=None):
    """
    This should sort the given queryset by the value of 'key'
    :param queryset: the queryset to be sorted
    :param key: the attribute to sort each item in the queryset by
    :type key: str
    :return: a dict of the format {item.__dict__[key]: item}
    """
    mapping = {}
    for item in queryset:
        update_merge_dict(mapping, item.__dict__[key], item)
    return order_dict(mapping=mapping, n=n)


def order_dict(mapping, n=None):
    """
    Order a dict by keys, with an option arg to limit the number of top keys to get
    :param mapping:
    :param n: optional number of top args to get
    :return: An ordered dict
    """
    top_items = collections.OrderedDict()
    length = n or len(mapping)
    for count in range(0, length):
        if not mapping:
            break
        largest_item = max(mapping)
        top_items.update({largest_item: mapping[largest_item]})
        mapping.pop(largest_item)
    return top_items


def update_merge_dict(mapping, key, value):
    """
    Inserts an item into a dict. If that key is already present, a list
    stores more than one value at that key
    :param mapping: the mapping to insert the key-value pair into
    :param key: the key to use
    :param value: the value to be inserted
    :return:
    """
    if key in mapping:
        if isinstance(mapping[key], list):
            mapping[key].append(value)
        else:
            mapping[key] = [mapping[key], value]
    else:
        mapping.update({key: value})