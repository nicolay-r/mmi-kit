import pydicom
from pydicom import DataElement
from pydicom.data import get_testdata_file
from pydicom.uid import ImplicitVRLittleEndian


def nifti_to_dicom(patient_id, patient_name, modality, image_matrix, age,
                   study_description="", ohif_description="",
                   frame_of_reference_uid=None,
                   series_instance_uid=None, sop_instance_uid=None, study_instance_uid=None):
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
    ds.add(DataElement(0x0008103E, 'LO', ohif_description))

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