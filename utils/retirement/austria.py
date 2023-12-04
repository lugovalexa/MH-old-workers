def austria_age(row):
    # Male
    if row["gender"] == "Male":
        if row["yrscontribution"] + 65 - row["age"] >= 15:
            return 65
        else:
            return row["age"] + 15 - row["yrscontribution"]

    # Female
    else:
        if row["yrscontribution"] + 60 - row["age"] >= 15:
            return 60
        else:
            return row["age"] + 15 - row["yrscontribution"]


def austria_change(row):
    return 0


def austria_change1(row):
    return 0
