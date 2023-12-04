def slovenia_age(row):
    # Male
    if row["gender"] == "Male":
        # Waves 1-4
        if row["wave"] < 5:
            if row["yrscontribution"] + 58 - row["age"] >= 40:
                return 58
            elif row["age"] + 40 - row["yrscontribution"] < 63:
                return row["age"] + 40 - row["yrscontribution"]
            elif row["yrscontribution"] + 63 - row["age"] >= 20:
                return 63
            elif row["age"] + 20 - row["yrscontribution"] == 64:
                return 64
            elif row["yrscontribution"] + 65 - row["age"] >= 15:
                return 65
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Waves 5-8
        else:
            if row["yrscontribution"] + 60 - row["age"] >= 40:
                return 60
            elif row["age"] + 40 - row["yrscontribution"] < 65:
                return row["age"] + 40 - row["yrscontribution"]
            elif row["yrscontribution"] + 65 - row["age"] >= 15:
                return 65
            else:
                return row["age"] + 15 - row["yrscontribution"]

    # Female
    else:
        # Waves 1-4
        if row["wave"] < 5:
            if row["yrscontribution"] + 58 - row["age"] >= 38:
                return 58
            elif row["age"] + 38 - row["yrscontribution"] < 61:
                return row["age"] + 38 - row["yrscontribution"]
            elif row["yrscontribution"] + 61 - row["age"] >= 20:
                return 61
            elif row["age"] + 20 - row["yrscontribution"] == 62:
                return 62
            elif row["yrscontribution"] + 63 - row["age"] >= 15:
                return 63
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Waves 5-8
        else:
            if row["yrscontribution"] + 60 - row["age"] >= 40:
                return 60
            elif row["age"] + 40 - row["yrscontribution"] < 65:
                return row["age"] + 40 - row["yrscontribution"]
            elif row["yrscontribution"] + 65 - row["age"] >= 15:
                return 65
            else:
                return row["age"] + 15 - row["yrscontribution"]


def slovenia_change(row):
    # Male
    if row["gender"] == "Male":
        # Wave 5
        if row["wave"] == 5:
            if row["yrscontribution"] + 60 - row["age"] >= 40:
                return 2
            elif row["age"] + 40 - row["yrscontribution"] < 65:
                return 0
            elif row["yrscontribution"] + 63 - row["age"] >= 20:
                return 2
            elif row["age"] + 20 - row["yrscontribution"] == 64:
                return 1
            elif row["yrscontribution"] + 65 - row["age"] >= 15:
                return 0
            else:
                return 0
        else:
            return 0

    # Female
    else:
        # Wave 5
        if row["wave"] == 5:
            if row["yrscontribution"] + 60 - row["age"] >= 40:
                return 2
            elif row["age"] + 40 - row["yrscontribution"] < 65:
                return 2
            elif row["yrscontribution"] + 61 - row["age"] >= 20:
                return 4
            elif row["age"] + 20 - row["yrscontribution"] == 62:
                return 3
            elif row["yrscontribution"] + 65 - row["age"] >= 15:
                return 0
            else:
                return 0
        else:
            return 0


def slovenia_change1(row):
    # Male
    if row["gender"] == "Male":
        # Wave 5
        if row["wave"] == 5:
            if row["yrscontribution"] + 60 - row["age"] >= 40:
                return 2
            elif row["age"] + 40 - row["yrscontribution"] < 65:
                return 0
            elif row["yrscontribution"] + 63 - row["age"] >= 20:
                return 2
            elif row["age"] + 20 - row["yrscontribution"] == 64:
                return 1
            elif row["yrscontribution"] + 65 - row["age"] >= 15:
                return 0
            else:
                return 0
        else:
            return 0

    # Female
    else:
        # Wave 5
        if row["wave"] == 5:
            if row["yrscontribution"] + 60 - row["age"] >= 40:
                return 2
            elif row["age"] + 40 - row["yrscontribution"] < 65:
                return 2
            elif row["yrscontribution"] + 61 - row["age"] >= 20:
                return 4
            elif row["age"] + 20 - row["yrscontribution"] == 62:
                return 3
            elif row["yrscontribution"] + 65 - row["age"] >= 15:
                return 0
            else:
                return 0
        else:
            return 0
