import numpy as np


def poland_age(row):
    # Wave 4
    if row["wave"] == 4:
        # Born before 1949
        if row["yrbirth"] < 1949:
            # Female
            if row["gender"] == "Female":
                if row["yrscontribution"] + 60 - row["age"] >= 15:
                    return 60
                else:
                    return row["age"] + 15 - row["yrscontribution"]
            # Male
            else:
                if row["yrscontribution"] + 65 - row["age"] >= 20:
                    return 65
                else:
                    return row["age"] + 20 - row["yrscontribution"]
        # Born after 1949
        else:
            # Female
            if row["gender"] == "Female":
                return 60
            # Male
            else:
                return 65
    # Wave 5
    elif row["wave"] == 5:
        # Female
        if row["gender"] == "Female":
            # Born after 1953
            if row["yrbirth"] >= 1953:
                return 60.33
            # Born before 1953
            else:
                if row["yrbirth"] >= 1949:
                    return 60
                else:
                    if row["yrscontribution"] + 60 - row["age"] >= 15:
                        return 60
                    else:
                        return row["age"] + 15 - row["yrscontribution"]
        # Male
        else:
            # Born after 1949
            if row["yrbirth"] >= 1949:
                return 65.33
            # Born before 1949
            else:
                if row["yrscontribution"] + 65 - row["age"] >= 20:
                    return 65
                else:
                    return row["age"] + 20 - row["yrscontribution"]
    # Wave 6
    else:
        # Female
        if row["gender"] == "Female":
            # Born after 1953
            if row["yrbirth"] >= 1953:
                return 61
            # Born before 1953
            else:
                if row["yrbirth"] >= 1949:
                    return 60
                else:
                    if row["yrscontribution"] + 60 - row["age"] >= 15:
                        return 60
                    else:
                        return row["age"] + 15 - row["yrscontribution"]
        # Male
        else:
            # Born after 1949
            if row["yrbirth"] >= 1949:
                return 66
            # Born before 1949
            else:
                if row["yrscontribution"] + 65 - row["age"] >= 20:
                    return 65
                else:
                    return row["age"] + 20 - row["yrscontribution"]


def poland_age_early(row):
    # Wave 4
    if row["wave"] == 4:
        # Female
        if row["gender"] == "Female":
            if row["yrbirth"] < 1949:
                if row["yrscontribution"] + 55 - row["age"] >= 30:
                    return 55
                elif row["age"] + 30 - row["yrscontribution"] < row["retirement_age"]:
                    return row["age"] + 30 - row["yrscontribution"]
                else:
                    return np.nan
            else:
                return np.nan
        # Male
        else:
            return np.nan
    # Waves 5 and 6
    else:
        # Female
        if row["gender"] == "Female":
            if row["yrbirth"] < 1949:
                if row["yrscontribution"] + 55 - row["age"] >= 30:
                    return 55
                elif row["age"] + 30 - row["yrscontribution"] < row["retirement_age"]:
                    return row["age"] + 30 - row["yrscontribution"]
                else:
                    return np.nan
            else:
                return np.nan
        # Male
        else:
            if row["yrbirth"] < 1949:
                if row["yrscontribution"] + 60 - row["age"] >= 35:
                    return 60
                elif row["age"] + 35 - row["yrscontribution"] < row["retirement_age"]:
                    return row["age"] + 35 - row["yrscontribution"]
                else:
                    return np.nan
            else:
                return np.nan
