def spain_age(row):
    # Waves 1-4
    if row["wave"] < 5:
        if row["yrscontribution"] + 65 - row["age"] >= 15:
            return 65
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Wave 5
    elif row["wave"] == 5:
        if row["yrscontribution"] + 65 - row["age"] >= 35.25:
            return 65
        elif row["yrscontribution"] + 65.08 - row["age"] >= 15:
            return 65.08
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Wave 6
    elif row["wave"] == 6:
        if row["yrscontribution"] + 65 - row["age"] >= 35.75:
            return 65
        elif row["yrscontribution"] + 65.25 - row["age"] >= 15:
            return 65.25
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Wave 7
    elif row["wave"] == 7:
        if row["yrscontribution"] + 65 - row["age"] >= 36.25:
            return 65
        elif row["yrscontribution"] + 65.42 - row["age"] >= 15:
            return 65.42
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Wave 8
    else:
        if row["yrscontribution"] + 65 - row["age"] >= 37:
            return 65
        elif row["yrscontribution"] + 65.83 - row["age"] >= 15:
            return 65.83
        else:
            return row["age"] + 15 - row["yrscontribution"]


def spain_change(row):
    # Wave 5
    if row["wave"] == 5:
        if row["yrscontribution"] + 65 - row["age"] >= 35.25:
            return 0
        elif row["yrscontribution"] + 65.08 - row["age"] >= 15:
            return 0.08
        else:
            return 0
    # Wave 6
    elif row["wave"] == 6:
        if row["yrscontribution"] + 65 - row["age"] >= 35.75:
            return 0
        elif row["yrscontribution"] + 65.25 - row["age"] >= 15:
            return 0.17
        else:
            return 0
    # Wave 7
    elif row["wave"] == 7:
        if row["yrscontribution"] + 65 - row["age"] >= 36.25:
            return 0
        elif row["yrscontribution"] + 65.42 - row["age"] >= 15:
            return 0.17
        else:
            return 0
    # Wave 8
    elif row["wave"] == 8:
        if row["yrscontribution"] + 65 - row["age"] >= 37:
            return 0
        elif row["yrscontribution"] + 65.83 - row["age"] >= 15:
            return 0.41
        else:
            return 0
    else:
        return 0
