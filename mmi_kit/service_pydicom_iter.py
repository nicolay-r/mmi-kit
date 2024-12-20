from mmi_kit.service_os import OsService
from mmi_kit.service_pydicom import PyDicomService


class DirFilesDicomIterator:
    """ This is a default type of iterator at file-system level,
        which is simply walks over the whole set of nested files
        for the given root directory (dir_path).
    """

    @staticmethod
    def get_iterator(dir_path):
        assert (isinstance(dir_path, str))
        return OsService.iter_dir_filepaths(from_dir=dir_path, filter_full_path=PyDicomService.is_dicom_filepath)


def iter_filtered(series_key, filepath_it, filter_func):
    assert (callable(filter_func) or filter_func is None)

    for filepath in filepath_it:
        if filter_func is not None and not filter_func(series_key, filepath):
            continue
        yield filepath
