class DictionaryService:

    @staticmethod
    def init_list(d, key):
        if key not in d:
            d[key] = []

    @staticmethod
    def try_get(d, path, default=None):
        for p in path:
            if p in d:
                d = d[p]
            else:
                return default
        return d

    @staticmethod
    def register_path(d, path, value_if_not_exist=None):

        # register path.
        target = d
        for p in path[:-1]:
            if p not in target:
                target[p] = dict()
            target = target[p]

        # register value only if the latter is not presented.
        if path[-1] not in target:
            target[path[-1]] = value_if_not_exist

        # Returning the value that is related to the provided path.
        return target[path[-1]]


    @staticmethod
    def init_dict(d, key):
        if key not in d:
            d[key] = {}

    @staticmethod
    def copy_with_keys(d, keys):
        assert (isinstance(d, dict))
        assert (isinstance(keys, set) or isinstance(keys, list))
        keys = set(keys)
        return {k: v for k, v in d.items() if k in keys}

    @staticmethod
    def get_key_by_entry_in_list_values(d, val):
        for k, v in d.items():
            assert (isinstance(v, list))
            if val in v:
                return k