def austria_age(row):
    # Male
    if row["gender"] == "Male":
        if row["yrscontribution"] + 65 - row["age"] >= 45:
            return 65
        else:
            return row["age"] + 45 - row["yrscontribution"]

    # Female
    else:
        if row["yrscontribution"] + 60 - row["age"] >= 45:
            return 60
        else:
            return row["age"] + 45 - row["yrscontribution"]
