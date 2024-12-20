import nibabel as nib


class NiftiService(object):

    @staticmethod
    def iter_slices(filepath, handle_func=None, handle_kwargs=dict()):
        assert (isinstance(filepath, str))

        nifti_img = nib.load(filepath)
        nifti_data = nifti_img.get_fdata()

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
