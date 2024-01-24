def germany_age(row):
    # Wave 4
    if row["wave"] == 4:
        if row["yrscontribution"] + 65 - row["age"] >= 5:
            return 65
        else:
            return row["age"] + 5 - row["yrscontribution"]
    # Wave 6
    else:
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
