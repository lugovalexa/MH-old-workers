import numpy as np


def netherlands_age(row):
    # Wave 4
    if row["wave"] == 4:
        return 65
    # Wave 6
    else:
        return 65.25


def netherlands_age_early(row):
    return np.nan
