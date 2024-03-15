import numpy as np


def germany_age(row):
    # Wave 4
    if row["wave"] == 4:
        if row["yrscontribution"] + 65 - row["age"] >= 5:
            return 65
        else:
            return row["age"] + 5 - row["yrscontribution"]
    # Wave 5
    elif row["wave"] == 5:
        if row["yrbirth"] >= 1963:
            if row["yrscontribution"] + 67 - row["age"] >= 5:
                return 67
            else:
                return row["age"] + 5 - row["yrscontribution"]
        else:
            if row["yrscontribution"] + 65.08 - row["age"] >= 5:
                return 65.08
            else:
                return row["age"] + 5 - row["yrscontribution"]
    # Wave 6
    else:
        if row["yrbirth"] >= 1963:
            if row["yrscontribution"] + 67 - row["age"] >= 5:
                return 67
            else:
                return row["age"] + 5 - row["yrscontribution"]
        else:
            if row["yrscontribution"] + 65.17 - row["age"] >= 5:
                return 65.17
            else:
                return row["age"] + 5 - row["yrscontribution"]


def germany_age_early(row):
    if (row["gender"] == "Female") and (row["yrbirth"] < 1952):
        if row["yrscontribution"] + 60 - row["age"] >= 15:
            return 60
        elif row["age"] + 15 - row["yrscontribution"] < 65:
            return row["age"] + 15 - row["yrscontribution"]
        else:
            return np.nan
    else:
        if row["yrscontribution"] + 63 - row["age"] >= 35:
            return 63
        elif row["age"] + 35 - row["yrscontribution"] < 65:
            return row["age"] + 35 - row["yrscontribution"]
        else:
            return np.nan
