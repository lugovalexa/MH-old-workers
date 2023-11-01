def poland_age(row):
    # Male
    if row["gender"] == "Male":
        # Waves 1-5
        if row["wave"] < 6:
            if row["yrscontribution"] + 65 - row["age"] >= 25:
                return 65
            else:
                return row["age"] + 25 - row["yrscontribution"]
        # Wave 6
        else:
            if row["yrscontribution"] + 65.75 - row["age"] >= 25:
                return 65.75
            else:
                return row["age"] + 25 - row["yrscontribution"]

    # Female
    else:
        # Waves 1-5
        if row["wave"] < 6:
            if row["yrscontribution"] + 60 - row["age"] >= 20:
                return 60
            else:
                return row["age"] + 20 - row["yrscontribution"]
        # Wave 6
        else:
            if row["yrscontribution"] + 60.75 - row["age"] >= 20:
                return 60.75
            else:
                return row["age"] + 20 - row["yrscontribution"]


def poland_change(row):
    # Male
    if row["gender"] == "Male":
        # Wave 6
        if row["wave"] == 6:
            if row["yrscontribution"] + 65.75 - row["age"] >= 25:
                return 0.75
            else:
                return 0
        else:
            return 0

    # Female
    else:
        # Wave 6
        if row["wave"] == 6:
            if row["yrscontribution"] + 60.75 - row["age"] >= 20:
                return 0.75
            else:
                return 0
        else:
            return 0
