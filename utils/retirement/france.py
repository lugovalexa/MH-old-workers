import numpy as np


def france_age(row):
    # Wave 4
    if row["wave"] == 4:
        if (row["yrbirth"] == 1951 and row["mobirth"] < 7) or (row["yrbirth"] <= 1951):
            if row["yrscontribution"] + 60 - row["age"] >= 40:
                return 60
            elif row["age"] + 40 - row["yrscontribution"] >= 65:
                return 65
            else:
                return row["age"] + 40 - row["yrscontribution"]
        elif row["yrbirth"] == 1951 and row["mbirth"] >= 7:
            if row["yrscontribution"] + 60.33 - row["age"] >= 40:
                return 60.33
            elif row["age"] + 40 - row["yrscontribution"] >= 65.33:
                return 65.33
            else:
                return row["age"] + 40 - row["yrscontribution"]
        elif row["yrbirth"] == 1952:
            if row["yrscontribution"] + 60.67 - row["age"] >= 41:
                return 60.67
            elif row["age"] + 41 - row["yrscontribution"] >= 65.67:
                return 65.67
            else:
                return row["age"] + 41 - row["yrscontribution"]
        elif row["yrbirth"] == 1953:
            if row["yrscontribution"] + 61 - row["age"] >= 41:
                return 61
            elif row["age"] + 41 - row["yrscontribution"] >= 66:
                return 66
            else:
                return row["age"] + 41 - row["yrscontribution"]
        elif row["yrbirth"] == 1954:
            if row["yrscontribution"] + 61.33 - row["age"] >= 41:
                return 61.33
            elif row["age"] + 41 - row["yrscontribution"] >= 66.33:
                return 66.33
            else:
                return row["age"] + 41 - row["yrscontribution"]
        elif row["yrbirth"] == 1955:
            if row["yrscontribution"] + 61.67 - row["age"] >= 41:
                return 61.67
            elif row["age"] + 41 - row["yrscontribution"] >= 66.67:
                return 66.67
            else:
                return row["age"] + 41 - row["yrscontribution"]
        else:
            if row["yrscontribution"] + 62 - row["age"] >= 41:
                return 62
            elif row["age"] + 41 - row["yrscontribution"] >= 67:
                return 67
            else:
                return row["age"] + 41 - row["yrscontribution"]
    # Wave 6
    else:
        if (row["yrbirth"] == 1951 and row["mobirth"] < 7) or (row["yrbirth"] <= 1951):
            if row["yrscontribution"] + 60 - row["age"] >= 41:
                return 60
            elif row["age"] + 41 - row["yrscontribution"] >= 65:
                return 65
            else:
                return row["age"] + 41 - row["yrscontribution"]
        elif row["yrbirth"] == 1951 and row["mbirth"] >= 7:
            if row["yrscontribution"] + 60.42 - row["age"] >= 41:
                return 60.42
            elif row["age"] + 41 - row["yrscontribution"] >= 65.42:
                return 65.42
            else:
                return row["age"] + 41 - row["yrscontribution"]
        elif row["yrbirth"] == 1952:
            if row["yrscontribution"] + 60.83 - row["age"] >= 41:
                return 60.83
            elif row["age"] + 41 - row["yrscontribution"] >= 65.83:
                return 65.83
            else:
                return row["age"] + 41 - row["yrscontribution"]
        elif row["yrbirth"] == 1953:
            if row["yrscontribution"] + 61.25 - row["age"] >= 41.25:
                return 61.25
            elif row["age"] + 41.25 - row["yrscontribution"] >= 66.25:
                return 66.25
            else:
                return row["age"] + 41.25 - row["yrscontribution"]
        elif row["yrbirth"] == 1954:
            if row["yrscontribution"] + 61.67 - row["age"] >= 41.25:
                return 61.67
            elif row["age"] + 41.25 - row["yrscontribution"] >= 66.67:
                return 66.67
            else:
                return row["age"] + 41.25 - row["yrscontribution"]
        else:
            if row["yrscontribution"] + 62 - row["age"] >= 41.5:
                return 62
            elif row["age"] + 41.5 - row["yrscontribution"] >= 67:
                return 67
            else:
                return row["age"] + 41.5 - row["yrscontribution"]


def france_age_early(row):
    return np.nan
