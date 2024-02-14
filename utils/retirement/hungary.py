import numpy as np


def hungary_age(row):
    # Born before 1952
    if row["yrbirth"] < 1952:
        if row["yrscontribution"] + 62 - row["age"] >= 15:
            return 62
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Born in 1952
    if row["yrbirth"] == 1952:
        if row["yrscontribution"] + 62.5 - row["age"] >= 15:
            return 62.5
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Born in 1953
    elif row["yrbirth"] == 1953:
        if row["yrscontribution"] + 63 - row["age"] >= 15:
            return 63
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Born in 1954
    elif row["yrbirth"] == 1954:
        if row["yrscontribution"] + 63.5 - row["age"] >= 15:
            return 63.5
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Born in 1955
    elif row["yrbirth"] == 1955:
        if row["yrscontribution"] + 64 - row["age"] >= 15:
            return 64
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Born in 1956
    elif row["yrbirth"] == 1956:
        if row["yrscontribution"] + 64.5 - row["age"] >= 15:
            return 64.5
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Born in 1957 or after
    else:
        if row["yrscontribution"] + 65 - row["age"] >= 15:
            return 65
        else:
            return row["age"] + 15 - row["yrscontribution"]


def hungary_age_early(row):
    # Female
    if row["gender"] == "Female":
        # 40 years of contributions
        if row["age"] + 40 - row["yrscontribution"] < row["retirement_age"]:
            return row["age"] + 40 - row["yrscontribution"]
        # 37 years of contributions
        # Born before 1958
        elif (
            (row["yrbirth"] < 1958)
            and (row["age"] + 37 - row["yrscontribution"] < row["retirement_age"])
            and (row["age"] + 37 - row["yrscontribution"] >= row["retirement_age"] - 3)
        ):
            return row["age"] + 37 - row["yrscontribution"]
        elif (
            (row["yrbirth"] < 1958)
            and (row["age"] + 37 - row["yrscontribution"] < row["retirement_age"])
            and (row["age"] + 37 - row["yrscontribution"] < row["retirement_age"] - 3)
        ):
            return row["retirement_age"] - 3
        # Born in 1958
        elif (
            (row["yrbirth"] == 1958)
            and (row["age"] + 37 - row["yrscontribution"] < row["retirement_age"])
            and (
                row["age"] + 37 - row["yrscontribution"] >= row["retirement_age"] - 2.5
            )
        ):
            return row["age"] + 37 - row["yrscontribution"]
        elif (
            (row["yrbirth"] == 1958)
            and (row["age"] + 37 - row["yrscontribution"] < row["retirement_age"])
            and (row["age"] + 37 - row["yrscontribution"] < row["retirement_age"] - 2.5)
        ):
            return row["retirement_age"] - 2.5
        # Born after 1958
        elif (
            (row["yrbirth"] > 1958)
            and (row["age"] + 37 - row["yrscontribution"] < row["retirement_age"])
            and (row["age"] + 37 - row["yrscontribution"] >= row["retirement_age"] - 2)
        ):
            return row["age"] + 37 - row["yrscontribution"]
        elif (
            (row["yrbirth"] > 1958)
            and (row["age"] + 37 - row["yrscontribution"] < row["retirement_age"])
            and (row["age"] + 37 - row["yrscontribution"] < row["retirement_age"] - 2)
        ):
            return row["retirement_age"] - 2
        else:
            return np.nan
    # Male
    else:
        # 40 years of contributions
        if row["yrscontribution"] + 60 - row["age"] >= 40:
            return 60
        elif row["age"] + 40 - row["yrscontribution"] < row["retirement_age"]:
            return row["age"] + 40 - row["yrscontribution"]
        # 37 years of contributions
        elif (row["age"] + 37 - row["yrscontribution"] < row["retirement_age"]) and (
            row["age"] + 37 - row["yrscontribution"] >= row["retirement_age"] - 2
        ):
            return row["age"] + 37 - row["yrscontribution"]
        elif (row["age"] + 37 - row["yrscontribution"] < row["retirement_age"]) and (
            row["age"] + 37 - row["yrscontribution"] < row["retirement_age"] - 2
        ):
            return row["retirement_age"] - 2
        # 42 years of contributions
        # Born in 1952
        elif (
            (row["yrbirth"] == 1952)
            and (row["age"] + 42 - row["yrscontribution"] < row["retirement_age"])
            and (
                row["age"] + 42 - row["yrscontribution"] >= row["retirement_age"] - 2.5
            )
        ):
            return row["age"] + 42 - row["yrscontribution"]
        elif (
            (row["yrbirth"] == 1952)
            and (row["age"] + 42 - row["yrscontribution"] < row["retirement_age"])
            and (row["age"] + 42 - row["yrscontribution"] < row["retirement_age"] - 2.5)
        ):
            return row["retirement_age"] - 2.5
        # Born in 1953-1954
        elif (
            ((row["yrbirth"] == 1953) or (row["yrbirth"] == 1954))
            and (row["age"] + 42 - row["yrscontribution"] < row["retirement_age"])
            and (row["age"] + 42 - row["yrscontribution"] >= row["retirement_age"] - 3)
        ):
            return row["age"] + 42 - row["yrscontribution"]
        elif (
            ((row["yrbirth"] == 1953) or (row["yrbirth"] == 1954))
            and (row["age"] + 42 - row["yrscontribution"] < row["retirement_age"])
            and (row["age"] + 42 - row["yrscontribution"] < row["retirement_age"] - 3)
        ):
            return row["retirement_age"] - 3
        else:
            return np.nan
