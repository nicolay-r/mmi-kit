import pydicom
from pydicom.data import get_testdata_file
from pydicom.uid import ImplicitVRLittleEndian


def nifti_to_dicom(arr, modality):
    assert (isinstance(modality, str))
    assert (modality in ["CT", "MR"])

    templates = {
        "CT": get_testdata_file("CT_small.dcm"),
        "MR": get_testdata_file("MR_small.dcm")
    }

    ds = pydicom.dcmread(templates[modality.upper()])

    arr = arr.astype('uint16')

    # Patient related info setup
    ds.PatientName = "Anonymous"
    ds.PatientID = "123456"
    ds.Modality = modality
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
