import numpy as np


def portugal_age(row):
    # Wave 4
    if row["wave"] == 4:
        if row["yrscontribution"] + 65 - row["age"] >= 15:
            return 65
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Wave 6
    else:
        if row["yrscontribution"] + 66 - row["age"] >= 15:
            return 66
        else:
            return row["age"] + 15 - row["yrscontribution"]


def portugal_age_early(row):
    # Wave 4
    if row["wave"] == 4:
        if row["yrscontribution"] + 55 - row["age"] >= 30:
            return 55
        elif row["age"] + 30 - row["yrscontribution"] < row["retirement_age"]:
            return row["age"] + 30 - row["yrscontribution"]
        else:
            return np.nan
    # Wave 6
    else:
        if row["yrscontribution"] + 60 - row["age"] >= 40:
            return 60
        elif row["age"] + 40 - row["yrscontribution"] < row["retirement_age"]:
            return row["age"] + 40 - row["yrscontribution"]
        else:
            return np.nan
