import pyreadstat


def import_stata(file_path):
    df, meta = pyreadstat.read_dta(file_path)
    return df, meta
