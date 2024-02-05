import numpy as np


def austria_age(row):
    # Male
    if row["gender"] == "Male":
        if row["yrscontribution"] + 65 - row["age"] >= 15:
            return 65
        else:
            return row["age"] + 15 - row["yrscontribution"]

    # Female
    else:
        if row["yrscontribution"] + 60 - row["age"] >= 15:
            return 60
        else:
            return row["age"] + 15 - row["yrscontribution"]


def austria_age_early(row):
    # Wave 4
    if row["wave"] == 4:
        # Male
        if row["gender"] == "Male":
            if row["yrscontribution"] + 62 - row["age"] >= 15:
                return 62
            elif row["age"] + 15 - row["yrscontribution"] < 65:
                return row["age"] + 15 - row["yrscontribution"]
            else:
                return np.nan

        # Female
        else:
            if row["yrscontribution"] + 57 - row["age"] >= 15:
                return 57
            elif row["age"] + 15 - row["yrscontribution"] < 60:
                return row["age"] + 15 - row["yrscontribution"]
            else:
                return np.nan
    # Wave 6
    else:
        # Male
        if row["gender"] == "Male":
            if row["yrscontribution"] + 64 - row["age"] >= 15:
                return 64
            elif row["age"] + 15 - row["yrscontribution"] < 65:
                return row["age"] + 15 - row["yrscontribution"]
            else:
                return np.nan

        # Female
        else:
            if row["yrscontribution"] + 59 - row["age"] >= 15:
                return 59
            elif row["age"] + 15 - row["yrscontribution"] < 60:
                return row["age"] + 15 - row["yrscontribution"]
            else:
                return np.nan
