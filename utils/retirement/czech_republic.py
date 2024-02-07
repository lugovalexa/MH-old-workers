import numpy as np


def czech_republic_age(row):
    # Male
    if row["gender"] == "Male":
        # Wave 4
        if row["wave"] == 4:
            if row["yrscontribution"] + 62.17 - row["age"] >= 27:
                return 62.17
            elif row["age"] + 27 - row["yrscontribution"] < 65:
                return row["age"] + 27 - row["yrscontribution"]
            elif row["yrscontribution"] + 65 - row["age"] >= 17:
                return 65
            else:
                return row["age"] + 17 - row["yrscontribution"]
        # Wave 5
        elif row["wave"] == 5:
            if row["yrscontribution"] + 62.5 - row["age"] >= 29:
                return 62.5
            elif row["age"] + 29 - row["yrscontribution"] < 65:
                return row["age"] + 29 - row["yrscontribution"]
            elif row["yrscontribution"] + 65 - row["age"] >= 19:
                return 65
            else:
                return row["age"] + 19 - row["yrscontribution"]
        # Wave 6
        else:
            if row["yrscontribution"] + 62.83 - row["age"] >= 31:
                return 62.83
            elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                return row["age"] + 31 - row["yrscontribution"]
            elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                return 62.83 + 5
            else:
                return row["age"] + 20 - row["yrscontribution"]

    # Female
    else:
        # Wave 4
        if row["wave"] == 4:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 61 - row["age"] >= 27:
                    return 61
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return row["age"] + 27 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 17:
                    return 65
                else:
                    return row["age"] + 17 - row["yrscontribution"]
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 60 - row["age"] >= 27:
                    return 60
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return row["age"] + 27 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 17:
                    return 65
                else:
                    return row["age"] + 17 - row["yrscontribution"]
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 59 - row["age"] >= 27:
                    return 59
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return row["age"] + 27 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 17:
                    return 65
                else:
                    return row["age"] + 17 - row["yrscontribution"]
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 58 - row["age"] >= 27:
                    return 58
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return row["age"] + 27 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 17:
                    return 65
                else:
                    return row["age"] + 17 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 57 - row["age"] >= 27:
                    return 57
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return row["age"] + 27 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 17:
                    return 65
                else:
                    return row["age"] + 17 - row["yrscontribution"]
        # Wave 6
        else:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 62 - row["age"] >= 31:
                    return 62
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return row["age"] + 31 - row["yrscontribution"]
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 61 - row["age"] >= 31:
                    return 61
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return row["age"] + 31 - row["yrscontribution"]
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 60 - row["age"] >= 31:
                    return 60
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return row["age"] + 31 - row["yrscontribution"]
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 59 - row["age"] >= 31:
                    return 59
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return row["age"] + 31 - row["yrscontribution"]
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 58 - row["age"] >= 31:
                    return 58
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return row["age"] + 31 - row["yrscontribution"]
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]


def czech_republic_age_early(row):
    # Wave 4
    if row["wave"] == 4:
        if (row["age"] + 27 - row["yrscontribution"] < row["retirement_age"]) and (
            row["age"] + 27 - row["yrscontribution"] >= row["retirement_age"] - 3
        ):
            return row["age"] + 27 - row["yrscontribution"]
        elif (row["age"] + 27 - row["yrscontribution"] < row["retirement_age"]) and (
            row["age"] + 27 - row["yrscontribution"] < row["retirement_age"] - 3
        ):
            return row["retirement_age"] - 3
        else:
            return np.nan
    # Wave 6
    else:
        if row["retirement_age"] < 63:
            if (
                (row["age"] + 31 - row["yrscontribution"] < row["retirement_age"])
                and (
                    row["age"] + 31 - row["yrscontribution"]
                    >= row["retirement_age"] - 3
                )
                and (row["age"] + 31 - row["yrscontribution"] >= 60)
            ):
                return row["age"] + 31 - row["yrscontribution"]
            else:
                return np.nan
        else:
            if (
                (row["age"] + 31 - row["yrscontribution"] < row["retirement_age"])
                and (
                    row["age"] + 31 - row["yrscontribution"]
                    >= row["retirement_age"] - 5
                )
                and (row["age"] + 31 - row["yrscontribution"] >= 60)
            ):
                return row["age"] + 31 - row["yrscontribution"]
            else:
                return np.nan
