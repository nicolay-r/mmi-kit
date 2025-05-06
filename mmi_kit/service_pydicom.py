import io
import warnings
import pydicom


class PyDicomService(object):

    @staticmethod
    def _try_extract_pixel_data(ds):
        try:
            return ds.pixel_array
        except AttributeError:
            return None
        except ValueError:
            # This is related to the #7 issue of size mismatching here:
            # https://github.com/nicolay-r/NLP-MMI-resources/issues/7
            # Therefore we skip the related cases for now.
            return None

    @staticmethod
    def __read_dataset(filepath, **kwargs):
        return pydicom.dcmread(filepath)

    @staticmethod
    def read_dataset(filepath, **kwargs):
        return PyDicomService.__read_dataset(filepath)

    @staticmethod
    def dataset_modify_study(ds, study_uid):
        ds.StudyInstanceUID = study_uid  # Assign the same Study Instance UID

    @staticmethod
    def dataset_to_bytes(ds):
        with io.BytesIO() as bytes_io:
            ds.save_as(bytes_io)
            return bytes_io.getvalue()

    @staticmethod
    def dataset_iter_frames(ds):
        if hasattr(ds, 'NumberOfFrames'):
            # Attempting to extract pixel data.
            pixel_data = PyDicomService._try_extract_pixel_data(ds)
            if pixel_data is not None:
                for i in range(ds.NumberOfFrames):
                    yield pixel_data[i]
        else:
            # Single image.
            pixel_data = PyDicomService._try_extract_pixel_data(ds)
            if pixel_data is not None:
                yield pixel_data

    @staticmethod
    def iter_frames(filepaths, **kwargs):
        assert (isinstance(filepaths, list))
        for filepath in filepaths:
            dicom_dataset = PyDicomService.__read_dataset(filepath, **kwargs)
            pixel_arrays_it = PyDicomService.dataset_iter_frames(dicom_dataset)
            for ind, pixel_array in enumerate(pixel_arrays_it):
                yield filepath, ind, pixel_array

    @staticmethod
    def dataset_get_image_aspect_ratio(ds):
        if 'PixelSpacing' in ds:
            pixel_spacing = ds.PixelSpacing
            row_spacing = float(pixel_spacing[0])
            col_spacing = float(pixel_spacing[1])
            aspect_ratio = col_spacing / row_spacing
            return aspect_ratio
        else:
            raise ValueError("PixelSpacing attribute not found in the DICOM dataset.")

    @staticmethod
    def _dataset_iter_metadata_recursive(ds, suppress_wa=False):

        with warnings.catch_warnings():

            # Optionally supress WA.
            # See the github issue #6 which still could not be covered even with fw_file package.
            # https://github.com/nicolay-r/NLP-MMI-resources/issues/6
            # I believe there is no serious as well as important in VR UI content of the DICOM.
            if suppress_wa:
                warnings.simplefilter("ignore")

            for elem in ds:
                # Check if the element is a sequence (which can contain nested datasets)
                if elem.VR == "SQ":
                    for i, seq_item in enumerate(elem.value):
                        PyDicomService._dataset_iter_metadata_recursive(seq_item, suppress_wa=suppress_wa)
                elif isinstance(elem.value, bytes):
                    continue
                else:
                    yield elem

    @staticmethod
    def dataset_iter_metadata_recursive(ds, suppress_wa=False):
        for elem in PyDicomService._dataset_iter_metadata_recursive(ds=ds, suppress_wa=suppress_wa):
            yield elem

    @staticmethod
    def iter_metadata_recursive(filepath, suppress_wa=False, **kwargs):
        for elem in PyDicomService._dataset_iter_metadata_recursive(
                ds=PyDicomService.__read_dataset(filepath, **kwargs),
                suppress_wa=suppress_wa):
            yield elem
