import numpy as np
import pydicom

from mmi_kit.service_pillow import PillowService
from mmi_kit.service_pydicom import PyDicomService


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
