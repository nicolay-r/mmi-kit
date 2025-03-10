from mmi_kit.service_convert import dicom_to_nifti
from mmi_kit.service_nifti import NiftiService
from pydicom.data.data_manager import get_testdata_file

for ind, s in enumerate(NiftiService.iter_slices(filepath="data/512.nii.gz")):
    ds = dicom_to_nifti(s, dcm_template_filepath=get_testdata_file("CT_small.dcm"))
    ds.save_as(f"out.dcm")
    break
