import numpy as np


def slovenia_age(row):
    # Wave 4
    if row["wave"] == 4:
        if row["yrscontribution"] + 63 - row["age"] >= 15:
            return 63
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Wave 6
    else:
        if row["yrscontribution"] + 65 - row["age"] >= 15:
            return 65
        else:
            return row["age"] + 15 - row["yrscontribution"]


def slovenia_age_early(row):
    # Wave 4
    if row["wave"] == 4:
        if row["gender"] == "Male":
            if row["yrscontribution"] + 58 - row["age"] >= 40:
                return 58
            elif row["age"] + 40 - row["yrscontribution"] < 63:
                return row["age"] + 40 - row["yrscontribution"]
            elif row["yrscontribution"] + 63 - row["age"] >= 20:
                return 63
            elif row["age"] + 20 - row["yrscontribution"] < row["retirement_age"]:
                return row["age"] + 20 - row["yrscontribution"]
            else:
                return np.nan
        else:
            if row["yrscontribution"] + 58 - row["age"] >= 38:
                return 58
            elif row["age"] + 38 - row["yrscontribution"] < 61:
                return row["age"] + 38 - row["yrscontribution"]
            elif row["yrscontribution"] + 61 - row["age"] >= 20:
                return 61
            elif row["age"] + 20 - row["yrscontribution"] < row["retirement_age"]:
                return row["age"] + 20 - row["yrscontribution"]
            else:
                return np.nan
    else:
        if row["yrscontribution"] + 60 - row["age"] >= 40:
            return 60
        elif row["age"] + 40 - row["yrscontribution"] < row["retirement_age"]:
            return row["age"] + 40 - row["yrscontribution"]
        else:
            return np.nan
