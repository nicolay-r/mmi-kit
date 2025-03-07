from os.path import dirname, join, realpath

import pydicom
from pydicom.uid import ImplicitVRLittleEndian


current_dir = dirname(realpath(__file__))
TEST_DATA_DIR = join(current_dir, "data")


def dicom_to_nifti(arr):

    ds = pydicom.dcmread(join(TEST_DATA_DIR, f"MR_small.dcm"))

    arr = arr.astype('uint16')

    # Patient related info setup
    ds.PatientName = "Anonymous"
    ds.PatientID = "123456"
    ds.Modality = "MR"
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.StudyInstanceUID = pydicom.uid.generate_uid()

    ds.file_meta.TransferSyntaxUID = ImplicitVRLittleEndian
    ds.Rows = arr.shape[0]
    ds.Columns = arr.shape[1]
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.SamplesPerPixel = 1
    ds.BitsStored = 16
    ds.BitsAllocated = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 1
    ds.PixelData = arr.tobytes()

    return ds
