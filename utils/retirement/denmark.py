import numpy as np


def denmark_age(row):
    if (row["yrbirth"] == 1932 and row["mobirth"] < 7) or (row["yrbirth"] < 1932):
        return 67
    else:
        return 65


def denmark_age_early(row):
    return np.nan
