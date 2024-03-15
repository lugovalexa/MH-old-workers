import numpy as np


def spain_age(row):
    # Wave 4
    if row["wave"] == 4:
        if row["yrscontribution"] + 65 - row["age"] >= 15:
            return 65
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Wave 5
    elif row["wave"] == 5:
        if row["yrscontribution"] + 65.08 - row["age"] >= 15:
            return 65.08
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Wave 6
    else:
        if row["yrscontribution"] + 65.25 - row["age"] >= 15:
            return 65.25
        else:
            return row["age"] + 15 - row["yrscontribution"]


def spain_age_early(row):
    # Wave 4
    if row["wave"] < 6:
        return np.nan
    # Wave 6
    else:
        if (row["age"] + 35 - row["yrscontribution"] < row["retirement_age"]) and (
            row["age"] + 35 - row["yrscontribution"] >= row["retirement_age"] - 2
        ):
            return row["age"] + 35 - row["yrscontribution"]
        elif (row["age"] + 35 - row["yrscontribution"] < row["retirement_age"]) and (
            row["age"] + 35 - row["yrscontribution"] < row["retirement_age"] - 2
        ):
            return row["retirement_age"] - 2
        else:
            return np.nan
