import io
import zipfile
from fnmatch import fnmatch


class ZipService(object):

    @staticmethod
    def __open(zip_filepath):
        return zipfile.ZipFile(zip_filepath, 'r')

    @staticmethod
    def __read_inner_file(zip_file, file_name):
        with zip_file.open(file_name, mode="r") as file:
            return io.BytesIO(file.read())

    @staticmethod
    def read_inner_file(zip_filepath, file_name):
        with ZipService.__open(zip_filepath) as zip_file:
            return ZipService.__read_inner_file(zip_file=zip_file, file_name=file_name)

    @staticmethod
    def __iter_zip_contents(zip_file, filter_func, skip_dir=True):
        for file_name in zip_file.namelist():
            if skip_dir and zip_file.getinfo(file_name).is_dir():
                continue
            if filter_func(file_name):
                yield file_name

    @staticmethod
    def __iter_zip_contents_pattern(zip_file, pattern, **kwargs):
        return ZipService.__iter_zip_contents(zip_file=zip_file,
                                              filter_func=lambda filename: fnmatch(filename, pattern),
                                              **kwargs)

    @staticmethod
    def iter_inner_files(zip_filepath, **kwargs):
        with ZipService.__open(zip_filepath) as zip_file:
            for file_name in ZipService.__iter_zip_contents_pattern(zip_file=zip_file, **kwargs):
                yield file_name, ZipService.__read_inner_file(zip_file=zip_file, file_name=file_name)

    @staticmethod
    def iter_zip_contents(zip_filepath, **kwargs):
        with ZipService.__open(zip_filepath) as zip_file:
            return ZipService.__iter_zip_contents(zip_file=zip_file, filter_func=lambda _: True, **kwargs)

    @staticmethod
    def iter_zip_contents_pattern(zip_filepath, **kwargs):
        with ZipService.__open(zip_filepath) as zip_file:
            return ZipService.__iter_zip_contents_pattern(zip_file=zip_file, **kwargs)