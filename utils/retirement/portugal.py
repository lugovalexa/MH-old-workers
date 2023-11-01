def portugal_age(row):
    # Waves 1-5
    if row["wave"] < 6:
        if row["yrscontribution"] + 65 - row["age"] >= 15:
            return 65
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Waves 6-8
    else:
        if row["yrscontribution"] + 66 - row["age"] >= 15:
            return 66
        else:
            return row["age"] + 15 - row["yrscontribution"]


def portugal_change(row):
    # Wave 6
    if row["wave"] == 6:
        if row["yrscontribution"] + 66 - row["age"] >= 15:
            return 1
        else:
            return 0
    else:
        return 0
