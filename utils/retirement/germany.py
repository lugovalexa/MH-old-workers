def germany_age(row):
    # Waves 1-4
    if row["wave"] < 5:
        if row["yrscontribution"] + 65 - row["age"] >= 5:
            return 65
        else:
            return row["age"] + 5 - row["yrscontribution"]
    # Wave 5
    elif row["wave"] == 5:
        if row["yrbirth"] >= 1963:
            if row["yrscontribution"] + 67 - row["age"] >= 5:
                return 67
            else:
                return row["age"] + 5 - row["yrscontribution"]
        else:
            if row["yrscontribution"] + 65.08 - row["age"] >= 5:
                return 65.08
            else:
                return row["age"] + 5 - row["yrscontribution"]
    # Wave 6
    elif row["wave"] == 6:
        if row["yrbirth"] >= 1963:
            if row["yrscontribution"] + 67 - row["age"] >= 5:
                return 67
            else:
                return row["age"] + 5 - row["yrscontribution"]
        else:
            if row["yrscontribution"] + 65.17 - row["age"] >= 5:
                return 65.17
            else:
                return row["age"] + 5 - row["yrscontribution"]
    # Wave 7
    elif row["wave"] == 7:
        if row["yrbirth"] >= 1963:
            if row["yrscontribution"] + 67 - row["age"] >= 5:
                return 67
            else:
                return row["age"] + 5 - row["yrscontribution"]
        else:
            if row["yrscontribution"] + 65.25 - row["age"] >= 5:
                return 65.25
            else:
                return row["age"] + 5 - row["yrscontribution"]
    # Wave 8
    else:
        if row["yrbirth"] >= 1963:
            if row["yrscontribution"] + 67 - row["age"] >= 5:
                return 67
            else:
                return row["age"] + 5 - row["yrscontribution"]
        else:
            if row["yrscontribution"] + 65.33 - row["age"] >= 5:
                return 65.33
            else:
                return row["age"] + 5 - row["yrscontribution"]


def germany_change(row):
    # Wave 5
    if row["wave"] == 5:
        if row["yrbirth"] >= 1963:
            if row["yrscontribution"] + 67 - row["age"] >= 5:
                return 2
            else:
                return 0
        else:
            if row["yrscontribution"] + 65.08 - row["age"] >= 5:
                return 0.08
            else:
                return 0
    # Wave 6
    elif row["wave"] == 6:
        if row["yrbirth"] >= 1963:
            return 0
        else:
            if row["yrscontribution"] + 65.17 - row["age"] >= 5:
                return 0.08
            else:
                return 0
    # Wave 7
    elif row["wave"] == 7:
        if row["yrbirth"] >= 1963:
            return 0
        else:
            if row["yrscontribution"] + 65.25 - row["age"] >= 5:
                return 0.08
            else:
                return 0
    # Wave 8
    elif row["wave"] == 8:
        if row["yrbirth"] >= 1963:
            return 0
        else:
            if row["yrscontribution"] + 65.33 - row["age"] >= 5:
                return 0.08
            else:
                return 0
    else:
        return 0
