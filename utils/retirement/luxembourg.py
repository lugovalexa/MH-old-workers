import numpy as np


def luxembourg_age(row):
    if row["yrscontribution"] + 65 - row["age"] >= 10:
        return 65
    else:
        return row["age"] + 10 - row["yrscontribution"]


def luxembourg_age_early(row):
    # Female
    if row["gender"] == "Female":
        if row["yrscontribution"] + 57 - row["age"] >= 40:
            return 57
        elif row["age"] + 40 - row["yrscontribution"] < row["retirement_age"]:
            return row["age"] + 40 - row["yrscontribution"]
        else:
            return np.nan
    # Male
    else:
        if row["yrscontribution"] + 60 - row["age"] >= 40:
            return 60
        elif row["age"] + 40 - row["yrscontribution"] < row["retirement_age"]:
            return row["age"] + 40 - row["yrscontribution"]
        else:
            return np.nan
