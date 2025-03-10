from mmi_kit.service_convert import nifti_to_dicom
from mmi_kit.service_nifti import NiftiService

for ind, s in enumerate(NiftiService.iter_slices(filepath="data/512.nii.gz")):
    ds = nifti_to_dicom(s, modality="CT")
    ds.save_as(f"out.dcm")
    break
