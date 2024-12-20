import os
from os.path import dirname, exists, join


class OsService(object):

    @staticmethod
    def replace_extension_with(filepath, ext):
        assert ('.' not in ext)
        return "{f}.{ext}".format(f=".".join(filepath.split('.')[:-1]), ext=ext)

    @staticmethod
    def iter_dir_filepaths(from_dir, filter_full_path=None):
        assert (isinstance(from_dir, str))

        for root, _, files in os.walk(from_dir):
            for file in files:
                full_path = os.path.join(root, file)
                if filter_full_path is not None:
                    if not filter_full_path(full_path):
                        continue
                yield full_path

    @staticmethod
    def create_dir_if_not_exists(filepath, is_dir=False):
        dir = dirname(filepath) if not is_dir else filepath

        # Check whether string is empty.
        if not dir:
            return

        if not exists(dir):
            os.makedirs(dir)

    @staticmethod
    def check_path_exist(filepath):
        return os.path.exists(filepath)

    @staticmethod
    def iter_rooted_files(root_dir, filepath_it):
        assert (isinstance(root_dir, str))
        for filepath in filepath_it:
            yield join(root_dir, filepath)
