from mmi_kit.service_convert import dicom_to_nifti
from mmi_kit.service_nifti import NiftiService


for ind, s in enumerate(NiftiService.iter_slices(filepath="data/512.nii.gz")):
    ds = dicom_to_nifti(s)
    ds.save_as(f"out.dcm")
    break
