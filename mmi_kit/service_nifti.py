import nibabel as nib
import numpy as np


class NiftiService(object):
    """ This Service class represent a wrapper over nibabel and numpy functionality.
    """

    @staticmethod
    def __read_data(filepath, **kwargs):
        nifti_img = nib.load(filepath, **kwargs)
        return nifti_img.get_fdata()

    @staticmethod
    def read_image(filepath, **kwargs):
        return NiftiService.__read_data(filepath, **kwargs)


    @staticmethod
    def iter_slices(filepath, handle_func=None, handle_kwargs=dict()):
        assert (isinstance(filepath, str))

        nifti_data = NiftiService.__read_data(filepath, **handle_kwargs)

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
    def save_image(array_slices, filename, **kwargs):
        assert (isinstance(array_slices, np.ndarray))
        img = nib.Nifti1Image(array_slices, affine=np.eye(4))
        nib.save(img, filename=filename, **kwargs)