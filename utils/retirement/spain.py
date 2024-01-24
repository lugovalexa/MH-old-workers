def spain_age(row):
    # Wave 4
    if row["wave"] == 4:
        if row["yrscontribution"] + 65 - row["age"] >= 15:
            return 65
        else:
            return row["age"] + 15 - row["yrscontribution"]
    # Wave 6
    else:
        if row["yrscontribution"] + 65 - row["age"] >= 35.75:
            return 65
        elif row["yrscontribution"] + 65.25 - row["age"] >= 15:
            return 65.25
        else:
            return row["age"] + 15 - row["yrscontribution"]
