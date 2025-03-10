from mmi_kit.service_convert import nifti_to_dicom
from mmi_kit.service_nifti import NiftiService

for ind, arr in enumerate(NiftiService.iter_slices(filepath="data/512.nii.gz")):
    ds = nifti_to_dicom(image_matrix=arr, modality="CT", patient_id="1", patient_name="Anonymous")
    ds.save_as(f"out.dcm")
    break