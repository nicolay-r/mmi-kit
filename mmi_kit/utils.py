import hashlib

from numpy import dot
from numpy.linalg import norm

degree = ['b', "kb", "mb", "gb", 'tb']


def convert_from_bytes(bytes_size, unit_type, round_digit=2):
    assert (isinstance(bytes_size, int))
    unit_type = unit_type.lower()
    return round(float(bytes_size) / (1024 ** degree.index(unit_type)), round_digit)


def convert_to_bytes(size, unit_type):
    unit_type = unit_type.lower()
    return size * (1024 ** degree.index(unit_type))


def iter_limit(data_it, limit=None):
    passed = 0
    for item in data_it:
        passed += 1
        if limit is not None and passed > limit:
            break
        yield item


def iter_to_iterator(items_it, iter_item_func=None):
    for item in items_it:
        item_it = iter_item_func(item) if iter_item_func is not None else item
        for item_elem in item_it:
            yield item_elem


def group_iter(dict_it, col_id):
    """ This method performs grouping of the elements.
    """

    patient_id = None
    buffer = []

    for d in dict_it:

        cur_pid = d[col_id]

        # Collect patient locally in the case when `patient_id` is not defined.
        if patient_id is None:
            patient_id = cur_pid

        # Similar to one then just append and go to the next item
        if patient_id == cur_pid:
            buffer.append(d)
            continue

        yield buffer

        # Collect the existed one.
        buffer = [d]
        patient_id = cur_pid

    # release the remaining content.
    if len(buffer) > 0:
        yield buffer


def calc_file_hash(filepath):
    return hashlib.md5(open(filepath, 'rb').read()).hexdigest()


def cos_sim(a, b):
    return dot(a, b)/(norm(a)*norm(b))


def seek_pattern(text, ordered_patterns, return_mode=None):
    assert (isinstance(ordered_patterns, list))

    assert (return_mode in ["ind_aft", None])
    f = None
    for p in ordered_patterns:
        if p in text:
            f = p
            break

    if return_mode is None:
        return f is not None
    elif return_mode == "ind_aft":
        return text.index(f) + len(f) if f is not None else -1