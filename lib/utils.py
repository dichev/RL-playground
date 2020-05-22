from typing import List

def chunks(lst:list, n:int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def split_by_index(arr, indexes:List[int]):
    assert max(indexes) < len(arr)
    start = 0
    for i in indexes:
        yield arr[start:i+1]
        start = i+1


class AttrDict(dict):
    """ Dictionary subclass whose entries can be accessed by attributes
        (as well as normally).
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def dict_as_object(data:dict) -> AttrDict:
    """ Construct nested AttrDicts from nested dictionaries. """
    if not isinstance(data, dict):
        return data
    else:
        return AttrDict({key: dict_as_object(data[key]) for key in data})