def estonia_age(row):
    # Male
    if row["gender"] == "Male":
        if row["yrscontribution"] + 63 - row["age"] >= 15:
            return 63
        else:
            return row["age"] + 15 - row["yrscontribution"]

    # Female
    else:
        # Wave 4
        if row["wave"] == 4:
            if row["yrscontribution"] + 61 - row["age"] >= 15:
                return 61
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Wave 6
        else:
            if row["yrscontribution"] + 62.5 - row["age"] >= 15:
                return 62.5
            else:
                return row["age"] + 15 - row["yrscontribution"]
