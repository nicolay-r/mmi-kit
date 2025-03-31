import json


class JsonService(object):

    @staticmethod
    def from_filepath(filepath):
        with open(filepath) as json_data:
            return json.load(json_data)

    @staticmethod
    def write(filepath, data, sort_keys=True, indent=4, ensure_ascii=False):
        with open(filepath, 'w') as out_file:
            json.dump(data, out_file, sort_keys=sort_keys, indent=indent, ensure_ascii=ensure_ascii)
