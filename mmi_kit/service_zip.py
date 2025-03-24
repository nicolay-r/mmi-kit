import io
import zipfile
from fnmatch import fnmatch


class ZipService(object):

    @staticmethod
    def __open(zip_filepath):
        return zipfile.ZipFile(zip_filepath, 'r')

    @staticmethod
    def read_inner_file(zip_filepath, file_name):
        with ZipService.__open(zip_filepath) as zip_file:
            with zip_file.open(file_name, mode="r") as file:
                return io.BytesIO(file.read())

    @staticmethod
    def __iter_zip_contents(zip_filepath, filter_func):
        with ZipService.__open(zip_filepath) as zip_file:
            for file_name in zip_file.namelist():
                if filter_func(file_name):
                    yield file_name

    @staticmethod
    def iter_zip_contents(**kwargs):
        return ZipService.__iter_zip_contents(filter_func=lambda _: True, **kwargs)

    @staticmethod
    def iter_zip_contents_pattern(pattern, **kwargs):
        return ZipService.__iter_zip_contents(filter_func=lambda filename: fnmatch(filename, pattern), **kwargs)
