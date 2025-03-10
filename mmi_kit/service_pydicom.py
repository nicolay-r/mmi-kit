import warnings

import numpy as np
import pydicom

from mmi_kit.service_pillow import PillowService


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
    def iter_frames_from_dataset(ds):
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
    def iter_frames(filepaths):
        assert (isinstance(filepaths, list))
        for filepath in filepaths:
            dicom_dataset = pydicom.dcmread(filepath)
            pixel_arrays_it = PyDicomService.iter_frames_from_dataset(dicom_dataset)
            for ind, pixel_array in enumerate(pixel_arrays_it):
                yield filepath, ind, pixel_array

    @staticmethod
    def get_image_aspect_ratio(ds):
        if 'PixelSpacing' in ds:
            pixel_spacing = ds.PixelSpacing
            row_spacing = float(pixel_spacing[0])
            col_spacing = float(pixel_spacing[1])
            aspect_ratio = col_spacing / row_spacing
            return aspect_ratio
        else:
            raise ValueError("PixelSpacing attribute not found in the DICOM dataset.")

    @staticmethod
    def is_dicom_filepath(filepath):
        return filepath.split('.')[-1] in ["dicom", "dcm"]

    @staticmethod
    def _iter_metadata_recursive(ds, suppress_wa=False):

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
                        PyDicomService.iter_metadata_recursive(seq_item)
                elif isinstance(elem.value, bytes):
                    continue
                else:
                    yield elem

    @staticmethod
    def iter_metadata_recursive(ds, suppress_wa=False):
        for data in PyDicomService._iter_metadata_recursive(ds=ds, suppress_wa=suppress_wa):
            yield data

    @staticmethod
    def get_metadata_dict(filepath, suppress_wa=False, **kwargs):
        return {
            elem.description(): elem.value
            for elem in PyDicomService._iter_metadata_recursive(
                ds=pydicom.dcmread(filepath),
                suppress_wa=suppress_wa)
        }

    @staticmethod
    def dicom_to_png(dicom_path, png_path, scale=255.0, extra_brightness=0):

        # Read the DICOM file
        ds = pydicom.dcmread(dicom_path)

        # Extract the pixel array
        # Make sure that we convert to the float type to avoid quality loss during further transformations.
        pixel_array = PyDicomService._try_extract_pixel_data(ds=ds)

        if pixel_array is None:
            raise Exception(f"Image / Pixel Array is not presented for the DICOM: {dicom_path}")

        pixel_array = pixel_array.astype(np.float64)

        # Extracting window center.
        window_center = None
        if 'WindowCenter' in ds:
            window_center = -ds.WindowCenter[0] \
                if isinstance(ds.WindowCenter, pydicom.multival.MultiValue) \
                else -ds.WindowCenter

        # Rescaling back to the original image.
        if window_center is not None and 'RescaleIntercept' in ds:
            intercept = window_center + ds.RescaleIntercept + extra_brightness
            pixel_array += intercept

        # Replace negative values to zero.
        pixel_array = np.maximum(pixel_array, 0)

        # Contract correction via scale parameter.
        image = PillowService.from_grayscale_pixeldata(pixel_array, scale=scale)

        # Save the image as PNG and remove the related object.
        if png_path is not None:
            image.save(png_path)
            image.close()

        return image
