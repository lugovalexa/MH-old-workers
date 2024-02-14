import numpy as np


def greece_age(row):
    # Wave 4
    if row["wave"] == 4:
        # Female
        if row["gender"] == "Female":
            if row["yrscontribution"] + 60 - row["age"] >= 15:
                return 60
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Male
        else:
            if row["yrscontribution"] + 65 - row["age"] >= 15:
                return 65
            else:
                return row["age"] + 15 - row["yrscontribution"]
    # Wave 6
    else:
        if row["yrscontribution"] + 67 - row["age"] >= 15:
            return 67
        else:
            return row["age"] + 15 - row["yrscontribution"]


def greece_age_early(row):
    # Wave 4
    if row["wave"] == 4:
        if row["age"] + 37 - row["yrscontribution"] < row["retirement_age"]:
            return row["age"] + 37 - row["yrscontribution"]
        elif row["yrscontribution"] + 60 - row["age"] >= 35:
            return 60
        elif row["age"] + 35 - row["yrscontribution"] < row["retirement_age"]:
            return row["age"] + 35 - row["yrscontribution"]
        else:
            return np.nan
    # Wave 6
    else:
        if row["age"] + 37 - row["yrscontribution"] < row["retirement_age"]:
            return row["age"] + 37 - row["yrscontribution"]
        elif row["yrscontribution"] + 62 - row["age"] >= 35:
            return 62
        elif row["age"] + 35 - row["yrscontribution"] < row["retirement_age"]:
            return row["age"] + 35 - row["yrscontribution"]
        else:
            return np.nan
