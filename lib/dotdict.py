class dotdict(dict):
    """
    a dictionary that supports dot notation 
    as well as dictionary access notation 
    """
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, item):
        obj = dict.__getitem__(self, item)
        if type(obj) is dict:
            return dotdict(obj)
        return obj