def estonia_age(row):
    # Male
    if row["gender"] == "Male":
        # Waves 1-6
        if row["wave"] < 7:
            if row["yrscontribution"] + 63 - row["age"] >= 15:
                return 63
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Wave 7
        elif row["wave"] == 7:
            if row["yrscontribution"] + 63.25 - row["age"] >= 15:
                return 63.25
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Wave 8
        else:
            if row["yrscontribution"] + 63.75 - row["age"] >= 15:
                return 63.75
            else:
                return row["age"] + 15 - row["yrscontribution"]

    # Female
    else:
        # Wave 1
        if row["wave"] == 1:
            if row["yrscontribution"] + 59 - row["age"] >= 15:
                return 59
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Wave 2
        elif row["wave"] == 2:
            if row["yrscontribution"] + 60 - row["age"] >= 15:
                return 60
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Wave 4
        elif row["wave"] == 4:
            if row["yrscontribution"] + 61 - row["age"] >= 15:
                return 61
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Wave 5
        elif row["wave"] == 5:
            if row["yrscontribution"] + 62 - row["age"] >= 15:
                return 62
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Wave 6
        elif row["wave"] == 6:
            if row["yrscontribution"] + 62.5 - row["age"] >= 15:
                return 62.5
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Wave 7
        elif row["wave"] == 7:
            if row["yrscontribution"] + 63.25 - row["age"] >= 15:
                return 63.25
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Wave 8
        else:
            if row["yrscontribution"] + 63.75 - row["age"] >= 15:
                return 63.75
            else:
                return row["age"] + 15 - row["yrscontribution"]


def estonia_change(row):
    # Male
    if row["gender"] == "Male":
        # Waves 1-6
        if row["wave"] == 7:
            if row["yrscontribution"] + 63.25 - row["age"] >= 15:
                return 0.25
            else:
                return 0
        # Wave 8
        elif row["wave"] == 8:
            if row["yrscontribution"] + 63.75 - row["age"] >= 15:
                return 0.5
            else:
                return 0
        else:
            return 0
    # Female
    else:
        # Wave 2
        if row["wave"] == 2:
            if row["yrscontribution"] + 60 - row["age"] >= 15:
                return 1
            else:
                return 0
        # Wave 4
        elif row["wave"] == 4:
            if row["yrscontribution"] + 61 - row["age"] >= 15:
                return 1
            else:
                return 0
        # Wave 5
        elif row["wave"] == 5:
            if row["yrscontribution"] + 62 - row["age"] >= 15:
                return 1
            else:
                return 0
        # Wave 6
        elif row["wave"] == 6:
            if row["yrscontribution"] + 62.5 - row["age"] >= 15:
                return 0.5
            else:
                return 0
        # Wave 7
        elif row["wave"] == 7:
            if row["yrscontribution"] + 63.25 - row["age"] >= 15:
                return 0.75
            else:
                return 0
        # Wave 8
        elif row["wave"] == 8:
            if row["yrscontribution"] + 63.75 - row["age"] >= 15:
                return 0.5
            else:
                return 0
        else:
            return 0
