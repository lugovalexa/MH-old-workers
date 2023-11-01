def luxembourg_age(row):
    # Waves 1-4
    if row["wave"] < 5:
        if row["yrscontribution"] + 65 - row["age"] >= 10:
            return 65
        else:
            return row["age"] + 10 - row["yrscontribution"]
    # Wave 5
    elif row["wave"] == 5:
        if row["yrscontribution"] + 65.08 - row["age"] >= 10:
            return 65.08
        else:
            return row["age"] + 10 - row["yrscontribution"]
    # Wave 6
    elif row["wave"] == 6:
        if row["yrscontribution"] + 65.25 - row["age"] >= 10:
            return 65.25
        else:
            return row["age"] + 10 - row["yrscontribution"]
    # Wave 7
    elif row["wave"] == 7:
        if row["yrscontribution"] + 65.75 - row["age"] >= 10:
            return 65.75
        else:
            return row["age"] + 10 - row["yrscontribution"]
    # Wave 8
    else:
        if row["yrscontribution"] + 66.33 - row["age"] >= 10:
            return 66.33
        else:
            return row["age"] + 10 - row["yrscontribution"]


def luxembourg_change(row):
    # Wave 5
    if row["wave"] == 5:
        if row["yrscontribution"] + 65.08 - row["age"] >= 10:
            return 0.08
        else:
            return 0
    # Wave 6
    elif row["wave"] == 6:
        if row["yrscontribution"] + 65.25 - row["age"] >= 10:
            return 0.17
        else:
            return 0
    # Wave 7
    elif row["wave"] == 7:
        if row["yrscontribution"] + 65.75 - row["age"] >= 10:
            return 0.5
        else:
            return 0
    # Wave 8
    elif row["wave"] == 8:
        if row["yrscontribution"] + 66.33 - row["age"] >= 10:
            return 0.58
        else:
            return 0
    else:
        return 0
