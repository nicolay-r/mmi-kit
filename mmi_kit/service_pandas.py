import tarfile

import pandas as pd
from tqdm import tqdm


class PandasService(object):

    def __init__(self, df):
        self.df = df

    @classmethod
    def from_csv(cls, target, **df_read_kwargs):
        df = pd.read_csv(filepath_or_buffer=target, **df_read_kwargs)
        return cls(df)

    @classmethod
    def from_json(cls, target, **df_read_kwargs):
        df = pd.read_json(path_or_buf=target, **df_read_kwargs)
        return cls(df)

    @classmethod
    def create_empty(cls, columns):
        df = pd.DataFrame(columns=columns)
        return cls(df)

    @classmethod
    def from_excel(cls, target, rows_range, cols_range):
        assert (isinstance(rows_range, tuple) or rows_range is None)
        assert (isinstance(cols_range, tuple) or cols_range is None)
        df = pd.read_excel(target)
        if rows_range is not None and cols_range is not None:
            df = df.iloc[rows_range[0]:rows_range[1], cols_range[0]:cols_range[1]]
        return cls(df)

    @classmethod
    def concat(cls, a, b):
        return cls(pd.concat([a.df, b.df]))

    @classmethod
    def from_dict(cls, d):
        assert (isinstance(d, dict))
        return cls(pd.DataFrame(d))

    @classmethod
    def from_list(cls, list_data, columns):
        return cls(pd.DataFrame(list_data, columns=columns))

    @classmethod
    def from_tar_csv(cls, target, subfile=None, **df_read_kwargs):
        if subfile is None:
            return cls.from_csv(target=target, **df_read_kwargs)

        with tarfile.open(target, mode='r:gz') as tar:
            content = tar.extractfile(subfile)
            return cls.from_csv(target=content, **df_read_kwargs)

    def iter_rows_as_dict(self, tqdm_disable=False, tqdm_desc=None):
        for _, data in tqdm(self.df.iterrows(), total=len(self.df), disable=tqdm_disable, desc=tqdm_desc):
            yield data.to_dict()

    def sort(self, columns, ascending=None):
        assert (isinstance(ascending, list) or ascending is None)
        if ascending is None:
            ascending = [False] * len(columns)
        self.df = self.df.sort_values(by=columns, ascending=ascending)

    def iter_rows_as_list(self, cols=None):
        cols = self.df.columns if cols is None else cols
        for data_dict in self.iter_rows_as_dict():
            yield [data_dict[c] for c in cols]

    def group_by_columns(self, cols):
        return self.df.groupby(cols)

    def show_top_rows(self, count):
        return self.df.head(count)

    def drop_columns(self, cols_range):
        columns_to_drop = self.df.columns[cols_range[0]:cols_range[1]]
        self.df = self.df.drop(columns=columns_to_drop)

    def append_row(self, row_dict, **kwargs):
        self.df = self.df._append(row_dict, **kwargs)

    def iter_df_series(self, group_cols):
        """ NOTE: This iteration includes empty groups.
        """
        assert (isinstance(group_cols, list) or group_cols is None)
        # Case of the absence of any grouping.
        if group_cols is None:
            # Then we just return all the data as-it-is.
            yield None, self.df
        else:
            # Perform grouping.
            for key, df_series in self.group_by_columns(cols=group_cols):
                yield key, df_series

    def __len__(self):
        return len(self.df)
