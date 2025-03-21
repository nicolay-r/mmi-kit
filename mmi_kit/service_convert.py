import numpy as np
import pydicom
from pydicom import DataElement
from pydicom.data import get_testdata_file
from pydicom.uid import ImplicitVRLittleEndian

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


def nifti_to_dicom(patient_id, patient_name, modality, image_matrix, age,
                   study_description="", series_description="",
                   frame_of_reference_uid=None,
                   series_instance_uid=None, sop_instance_uid=None, study_instance_uid=None):
    """ This is experimental approach. Not recommended to use.
        The actual implementation is more difficult that this.
    """

    assert (isinstance(age, int) and age > 0)
    assert (isinstance(patient_name, str))
    assert (isinstance(patient_id, str))
    assert (isinstance(modality, str))
    assert (modality in ["CT", "MR"])

    templates = {
        "CT": get_testdata_file("CT_small.dcm"),
        "MR": get_testdata_file("MR_small.dcm")
    }

    ds = pydicom.dcmread(templates[modality.upper()])

    image_matrix = image_matrix.astype('uint16')

    # Patient related info setup
    ds.PatientName = patient_name
    ds.PatientID = patient_id
    ds.Modality = modality
    ds.SeriesInstanceUID = pydicom.uid.generate_uid() if series_instance_uid is None else series_instance_uid
    ds.SOPInstanceUID = pydicom.uid.generate_uid() if sop_instance_uid is None else sop_instance_uid
    ds.StudyInstanceUID = pydicom.uid.generate_uid() if study_instance_uid is None else study_instance_uid
    ds.FrameOfReferenceUID = pydicom.uid.generate_uid() if frame_of_reference_uid is None else study_instance_uid

    ds.add(DataElement(0x00081030, 'LO', study_description))
    ds.add(DataElement(0x0008103E, 'LO', series_description))

    ds.PatientAge = str(age).rjust(3, "0") + "Y"
    ds.file_meta.TransferSyntaxUID = ImplicitVRLittleEndian
    ds.Rows = image_matrix.shape[0]
    ds.Columns = image_matrix.shape[1]
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.SamplesPerPixel = 1
    ds.BitsStored = 16
    ds.BitsAllocated = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 1
    ds.PixelData = image_matrix.tobytes()

    return ds