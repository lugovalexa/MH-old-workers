import numpy as np


def belgium_age(row):
    return 65


def belgium_age_early(row):
    # Wave 4
    if row["wave"] == 4:
        if row["yrscontribution"] + 60 - row["age"] >= 35:
            return 60
        elif row["age"] + 35 - row["yrscontribution"] < 65:
            return row["age"] + 35 - row["yrscontribution"]
        else:
            return np.nan
    # Wave 5
    elif row["wave"] == 5:
        if row["yrscontribution"] + 60 - row["age"] >= 40:
            return 60
        elif row["age"] + 40 - row["yrscontribution"] < 60.5:
            return row["age"] + 40 - row["yrscontribution"]
        elif row["yrscontribution"] + 60.5 - row["age"] >= 38:
            return 60.5
        elif row["age"] + 38 - row["yrscontribution"] < 65:
            return row["age"] + 38 - row["yrscontribution"]
        else:
            return np.nan
    # Wave 6
    else:
        if row["yrscontribution"] + 60 - row["age"] >= 41:
            return 60
        elif row["age"] + 41 - row["yrscontribution"] < 61.5:
            return row["age"] + 41 - row["yrscontribution"]
        elif row["yrscontribution"] + 61.5 - row["age"] >= 40:
            return 61.5
        elif row["age"] + 40 - row["yrscontribution"] < 65:
            return row["age"] + 40 - row["yrscontribution"]
        else:
            return np.nan
