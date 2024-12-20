def iter_handled_filepath_series(series_func, handlers, return_filepath=False, keep_first_fp_only=True):
    """ This function is for handling series of files.
        Series represent a concept of the related framework.
        Each filepath series iterates over files in the particular directory.
    """
    assert (callable(series_func))

    for series_key, s_it in series_func():
        for filepath in s_it:

            content = [series_key, [h(filepath) for h in handlers]]

            # Setup the set of returning parameters.
            if return_filepath:
                content.append(filepath)
            yield content

            # Breaking handling process in the case if we need only the first filepath mention.
            if keep_first_fp_only:
                break
