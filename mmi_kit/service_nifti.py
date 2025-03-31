import nibabel as nib
import numpy as np


class NiftiService(object):
    """ This Service class represent a wrapper over nibabel and numpy functionality.
    """

    @staticmethod
    def __read(filepath, **kwargs):
        nifti_img = nib.load(filepath, **kwargs)
        nifti_data = nifti_img.get_fdata()
        return nifti_img, nifti_data

    @staticmethod
    def read_image(filepath, **kwargs):
        return NiftiService.__read(filepath, **kwargs)

    @staticmethod
    def iter_slices(filepath, handle_func=None, handle_kwargs=dict()):
        assert (isinstance(filepath, str))

        _, nifti_data = NiftiService.__read(filepath, **handle_kwargs)

        # Iterate over each slice in the z-dimension (axis 2)
        for slice_ind in range(nifti_data.shape[2]):

            data = nifti_data[:, :, slice_ind]

            # Get the i-th slice
            yield handle_func(data, **handle_kwargs) if handle_func is not None else data

    @staticmethod
    def get_description(filepath):
        assert (isinstance(filepath, str))
        nifti_img = nib.load(filepath)
        header = nifti_img.header
        return header['descrip'].astype(str)

    @staticmethod
    def save_image(array_slices, filename, src_nifti=None, **nifti2img_kwargs):
        assert (isinstance(array_slices, np.ndarray))

        if src_nifti is not None:
            img, _ = NiftiService.__read(src_nifti)
            nifti2img_kwargs["affine"] = img.affine
            nifti2img_kwargs["header"] = img.header

        img = nib.Nifti1Image(array_slices, **nifti2img_kwargs)
        nib.save(img, filename=filename)
