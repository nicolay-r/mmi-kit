import io
import zipfile


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
    def iter_zip_contents(zip_filepath):
        with ZipService.__open(zip_filepath) as zip_file:
            for file_name in zip_file.namelist():
                yield file_name
